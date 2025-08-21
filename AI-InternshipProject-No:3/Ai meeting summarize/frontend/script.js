// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFile = document.getElementById('removeFile');
const processBtn = document.getElementById('processBtn');

// Sections
const uploadSection = document.getElementById('uploadSection');
const processingSection = document.getElementById('processingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

// Processing steps
const step1 = document.getElementById('step1');
const step2 = document.getElementById('step2');
const step3 = document.getElementById('step3');

// Results elements
const minutesContent = document.getElementById('minutesContent');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const newMeetingBtn = document.getElementById('newMeetingBtn');

// Error elements
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');

// Toast container
const toastContainer = document.getElementById('toastContainer');

// Global variables
let selectedFile = null;
let generatedMinutes = '';

// API Configuration
const API_BASE_URL = 'http://localhost:5000'; // Adjust this to match your Flask server

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    // Upload area events
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Remove file
    removeFile.addEventListener('click', clearSelectedFile);
    
    // Process button
    processBtn.addEventListener('click', processAudioFile);
    
    // Results buttons
    copyBtn.addEventListener('click', copyMinutes);
    downloadBtn.addEventListener('click', downloadMinutes);
    newMeetingBtn.addEventListener('click', resetToUpload);
    
    // Retry button
    retryBtn.addEventListener('click', resetToUpload);
}

// Drag and drop handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelection(files[0]);
    }
}

// File selection handlers
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFileSelection(file);
    }
}

function handleFileSelection(file) {
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.mp3')) {
        showToast('Please select an MP3 file only.', 'error');
        return;
    }
    
    // Validate file size (100MB limit)
    const maxSize = 100 * 1024 * 1024; // 100MB in bytes
    if (file.size > maxSize) {
        showToast('File size must be less than 100MB.', 'error');
        return;
    }
    
    selectedFile = file;
    displayFileInfo(file);
    processBtn.disabled = false;
}

function displayFileInfo(file) {
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';
    uploadArea.style.display = 'none';
}

function clearSelectedFile() {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    uploadArea.style.display = 'block';
    processBtn.disabled = true;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Processing functions
async function processAudioFile() {
    if (!selectedFile) {
        showToast('Please select a file first.', 'error');
        return;
    }
    
    // Show processing section
    showSection('processing');
    
    // Reset processing steps
    resetProcessingSteps();
    
    try {
        // Step 1: Upload file
        setActiveStep(1);
        
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        // Step 2: Transcribing
        setActiveStep(2);
        
        const response = await fetch(`${API_BASE_URL}/api/meeting/mom`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to process the file');
        }
        
        // Step 3: Generating minutes
        setActiveStep(3);
        
        const result = await response.json();
        
        if (result.status === 'success') {
            generatedMinutes = result.minutes_of_meeting;
            displayResults(generatedMinutes);
        } else {
            throw new Error('Failed to generate meeting minutes');
        }
        
    } catch (error) {
        console.error('Processing error:', error);
        showError(error.message);
    }
}

function resetProcessingSteps() {
    [step1, step2, step3].forEach(step => step.classList.remove('active'));
}

function setActiveStep(stepNumber) {
    resetProcessingSteps();
    const steps = [step1, step2, step3];
    if (stepNumber <= steps.length) {
        steps[stepNumber - 1].classList.add('active');
    }
}

// Results functions
function displayResults(minutes) {
    minutesContent.textContent = minutes;
    showSection('results');
    showToast('Meeting minutes generated successfully!', 'success');
}

async function copyMinutes() {
    try {
        await navigator.clipboard.writeText(generatedMinutes);
        showToast('Minutes copied to clipboard!', 'success');
    } catch (error) {
        console.error('Copy failed:', error);
        showToast('Failed to copy to clipboard.', 'error');
    }
}

function downloadMinutes() {
    const blob = new Blob([generatedMinutes], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `meeting-minutes-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Minutes downloaded successfully!', 'success');
}

// Error handling
function showError(message) {
    errorMessage.textContent = message;
    showSection('error');
}

// Navigation functions
function showSection(sectionName) {
    // Hide all sections
    uploadSection.style.display = 'none';
    processingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Show selected section
    switch (sectionName) {
        case 'upload':
            uploadSection.style.display = 'block';
            break;
        case 'processing':
            processingSection.style.display = 'block';
            break;
        case 'results':
            resultsSection.style.display = 'block';
            break;
        case 'error':
            errorSection.style.display = 'block';
            break;
    }
}

function resetToUpload() {
    clearSelectedFile();
    generatedMinutes = '';
    showSection('upload');
}

// Toast notification system
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
    
    toast.innerHTML = `
        <i class="${icon}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // Remove toast after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 4000);
}

// Add slideOut animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
