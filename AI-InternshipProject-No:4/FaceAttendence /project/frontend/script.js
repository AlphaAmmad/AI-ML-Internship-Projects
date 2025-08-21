// Basic tab switching
const tabs = document.querySelectorAll('.tab-btn');
const sections = document.querySelectorAll('.tab');
tabs.forEach(btn => btn.addEventListener('click', () => {
  sections.forEach(s => s.classList.remove('active'));
  document.querySelector(btn.dataset.target).classList.add('active');
}));

// Utilities
function dataUrlFromCanvas(canvas, type = 'image/jpeg', quality = 0.85) {
  return canvas.toDataURL(type, quality);
}

async function postJSON(url, payload) {
  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  return res.json();
}

function drawBoxes(canvas, boxes) {
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.lineWidth = 2;
  ctx.font = '14px system-ui';
  boxes.forEach(item => {
    const { top, right, bottom, left } = item.box;
    const name = item.name;
    ctx.strokeStyle = (name && name !== 'Unknown') ? '#22c55e' : '#ef4444';
    ctx.fillStyle = ctx.strokeStyle;
    ctx.beginPath();
    ctx.roundRect(left, top, right - left, bottom - top, 6);
    ctx.stroke();
    // Label background for readability
    const label = name || 'Unknown';
    const textWidth = ctx.measureText(label).width;
    const labelX = Math.max(0, Math.min(canvas.width - textWidth - 8, left + 6));
    const labelY = top - 8 < 0 ? top + 16 : top - 8;
    ctx.fillRect(labelX - 4, labelY - 12, textWidth + 8, 16);
    ctx.fillStyle = '#0b1220';
    ctx.fillText(label, labelX, labelY);
  });
}

// -------------------- Enroll --------------------
const enrollVideo = document.getElementById('enroll-video');
const enrollCanvas = document.getElementById('enroll-canvas');
const enrollCameraSelect = document.getElementById('enroll-camera-select');
const enrollStartCamBtn = document.getElementById('enroll-start-cam');
const enrollCaptureBtn = document.getElementById('enroll-capture');
const enrollClearBtn = document.getElementById('enroll-clear');
const enrollCaptures = document.getElementById('enroll-captures');
const enrollFile = document.getElementById('enroll-file');
const enrollUploads = document.getElementById('enroll-uploads');
const enrollForm = document.getElementById('enroll-form');
const enrollName = document.getElementById('enroll-name');
const enrollStatus = document.getElementById('enroll-status');

let enrollStream;
let capturedAngles = []; // dataURLs
let uploadedAngles = []; // dataURLs
let availableCameras = [];

async function populateCameraList() {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    availableCameras = devices.filter(d => d.kind === 'videoinput');

    // Populate both dropdowns
    [enrollCameraSelect, cameraSelect].forEach(select => {
      select.innerHTML = '<option value="">Select Camera...</option>';
      availableCameras.forEach((cam, idx) => {
        const option = document.createElement('option');
        option.value = cam.deviceId;
        option.textContent = cam.label || `Camera ${idx + 1}`;
        select.appendChild(option);
      });
    });
  } catch (e) {
    console.warn('Could not enumerate cameras:', e);
  }
}

async function startEnrollCam() {
  try {
    const deviceId = enrollCameraSelect.value;
    const constraints = deviceId ?
      { video: { deviceId: { exact: deviceId }, width: 640, height: 480 } } :
      { video: { facingMode: 'user', width: 640, height: 480 } };

    if (enrollStream) {
      enrollStream.getTracks().forEach(t => t.stop());
    }

    console.log('Starting enroll camera with constraints:', constraints);
    enrollStream = await navigator.mediaDevices.getUserMedia(constraints);
    enrollVideo.srcObject = enrollStream;

    // Force video to play and show
    enrollVideo.muted = true;
    enrollVideo.autoplay = true;
    enrollVideo.playsInline = true;
    await enrollVideo.play();

    console.log('Enroll video started, dimensions:', enrollVideo.videoWidth, 'x', enrollVideo.videoHeight);
    enrollStatus.textContent = 'Camera started. Capture multiple angles for better recognition.';
  } catch (e) {
    alert('Cannot access camera: ' + e.name + ' - ' + e.message + '\nTips:\n• Use http://127.0.0.1:8080 (not file://)\n• Allow camera permission\n• Close other apps using camera');
    console.error('Enroll camera error:', e);
  }
}

enrollStartCamBtn.addEventListener('click', startEnrollCam);

enrollCaptureBtn.addEventListener('click', () => {
  const ctx = enrollCanvas.getContext('2d');
  enrollCanvas.width = enrollVideo.videoWidth || 320;
  enrollCanvas.height = enrollVideo.videoHeight || 240;
  ctx.drawImage(enrollVideo, 0, 0, enrollCanvas.width, enrollCanvas.height);
  const data = dataUrlFromCanvas(enrollCanvas);
  capturedAngles.push(data);
  const img = document.createElement('img');
  img.src = data; img.style.width = '96px'; img.style.height = '72px';
  enrollCaptures.appendChild(img);
});

enrollClearBtn.addEventListener('click', () => {
  capturedAngles = [];
  uploadedAngles = [];
  enrollCaptures.innerHTML = '';
  enrollUploads.innerHTML = '';
});

enrollFile.addEventListener('change', () => {
  uploadedAngles = [];
  enrollUploads.innerHTML = '';
  const files = Array.from(enrollFile.files || []);
  files.forEach(file => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const data = e.target.result;
      uploadedAngles.push(data);
      const img = document.createElement('img');
      img.src = data; img.style.width = '96px'; img.style.height = '72px';
      enrollUploads.appendChild(img);
    };
    reader.readAsDataURL(file);
  });
});

enrollForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = enrollName.value.trim();
  if (!name) { alert('Please enter a name'); return; }

  const images = [...capturedAngles, ...uploadedAngles];
  if (!images.length) { alert('Please capture or upload at least one image'); return; }

  enrollStatus.textContent = 'Submitting...';
  try {
    const resp = await postJSON(`${window.BACKEND_URL}/enroll`, { name, images });
    if (resp.success) {
      enrollStatus.textContent = `Enrolled with ${images.length} angle(s)!`;
    } else {
      enrollStatus.textContent = 'Error: ' + (resp.error || 'Unknown');
    }
  } catch (err) {
    enrollStatus.textContent = 'Network error: ' + err.message;
  }
});

// -------------------- Live Recognition --------------------
const liveVideo = document.getElementById('live-video');
const overlay = document.getElementById('overlay');
const cameraSelect = document.getElementById('camera-select');
const startCamBtn = document.getElementById('start-cam');
const stopCamBtn = document.getElementById('stop-cam');
const recognizedList = document.getElementById('recognized-list');

let liveStream;
let recognizeIntervalId;

async function startLiveCam() {
  try {
    const deviceId = cameraSelect.value;
    const constraints = deviceId ?
      { video: { deviceId: { exact: deviceId }, width: 640, height: 480 } } :
      { video: { width: 640, height: 480, facingMode: 'user' } };

    if (liveStream) {
      liveStream.getTracks().forEach(t => t.stop());
    }

    console.log('Starting live camera with constraints:', constraints);
    liveStream = await navigator.mediaDevices.getUserMedia(constraints);
    liveVideo.srcObject = liveStream;

    // Force video to play and show
    liveVideo.muted = true;
    liveVideo.autoplay = true;
    liveVideo.playsInline = true;
    await liveVideo.play();

    // Adjust overlay size to EXACT video pixels and sync CSS size
    function resizeOverlayToVideo() {
      const vw = liveVideo.videoWidth;
      const vh = liveVideo.videoHeight;
      if (!vw || !vh) return;
      overlay.width = vw;
      overlay.height = vh;
      overlay.style.width = liveVideo.clientWidth + 'px';
      overlay.style.height = liveVideo.clientHeight + 'px';
      console.log('Overlay resized to', vw, 'x', vh, 'display size', liveVideo.clientWidth, 'x', liveVideo.clientHeight);
    }
    liveVideo.onloadedmetadata = resizeOverlayToVideo;
    window.addEventListener('resize', resizeOverlayToVideo);

    // Send a frame every 2 seconds
    if (recognizeIntervalId) clearInterval(recognizeIntervalId);
    recognizeIntervalId = setInterval(captureAndRecognize, 2000);

    console.log('Live camera started successfully');
  } catch (e) {
    alert('Cannot access camera: ' + e.name + ' - ' + e.message + '\nTips:\n• Use http://127.0.0.1:8080 (not file://)\n• Allow camera permission\n• Select a camera from dropdown\n• Close other apps using camera');
    console.error('Live camera error:', e);
  }
}

function stopLiveCam() {
  if (recognizeIntervalId) {
    clearInterval(recognizeIntervalId);
    recognizeIntervalId = null;
  }
  if (liveStream) {
    liveStream.getTracks().forEach(t => t.stop());
    liveStream = null;
  }
}

async function captureAndRecognize() {
  if (!liveVideo.videoWidth) return;
  const tempCanvas = document.createElement('canvas');
  tempCanvas.width = liveVideo.videoWidth;
  tempCanvas.height = liveVideo.videoHeight;
  const ctx = tempCanvas.getContext('2d');
  ctx.drawImage(liveVideo, 0, 0, tempCanvas.width, tempCanvas.height);
  const image = dataUrlFromCanvas(tempCanvas, 'image/jpeg', 0.8);

  try {
    const resp = await postJSON(`${window.BACKEND_URL}/recognize`, { image });
    if (resp.success) {
      drawBoxes(overlay, resp.results || []);
      // Update live list of names
      recognizedList.innerHTML = '';
      (resp.results || []).forEach(item => {
        const li = document.createElement('li');
        li.textContent = item.name;
        li.style.color = (item.name && item.name !== 'Unknown') ? '#22c55e' : '#ef4444';
        recognizedList.appendChild(li);
      });
    }
  } catch (e) {
    console.error('recognize error', e);
  }
}

startCamBtn.addEventListener('click', startLiveCam);
stopCamBtn.addEventListener('click', stopLiveCam);

// -------------------- Attendance Log --------------------
const refreshLogBtn = document.getElementById('refresh-log');
const tableBody = document.querySelector('#attendance-table tbody');

async function loadAttendance() {
  try {
    const res = await fetch(`${window.BACKEND_URL}/attendance`);
    const data = await res.json();
    if (data.success) {
      tableBody.innerHTML = '';
      (data.records || []).forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${r.Name}</td><td>${r.Date}</td><td>${r.Time}</td>`;
        tableBody.appendChild(tr);
      });
    }
  } catch (e) {
    console.error('attendance fetch error', e);
  }
}

refreshLogBtn.addEventListener('click', loadAttendance);

// Load attendance on first visit to the log tab
Array.from(tabs).forEach(btn => {
  btn.addEventListener('click', () => {
    if (btn.dataset.target === '#log') loadAttendance();
  });
});

// Initialize camera list on page load
populateCameraList();

