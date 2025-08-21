# Face Recognition Attendance System

A complete offline Face Recognition Attendance System built with Flask (Python) and a simple HTML/CSS/JS frontend.

## Features
- Enroll people with a name and face image (webcam capture or upload)
- Start Attendance: live webcam detection & recognition
- Green box for recognized faces, red for unknown
- Attendance logged to CSV (Name, Date, Time) — one entry per person per day
- CORS enabled; no cloud services required

## Folder Structure
```
project/
├─ backend/
│   ├─ app.py
│   ├─ encodings.pkl        # created automatically
│   └─ attendance.csv       # created automatically
├─ frontend/
│   ├─ index.html
│   ├─ style.css
│   └─ script.js
└─ README.md
```

## Setup (Local)
1. Python 3.9+ recommended. Create and activate a virtual environment.
2. Install dependencies (face_recognition requires dlib; see notes below):
```
pip install flask flask-cors pillow numpy face_recognition
```
On some systems, you may need OS-level build tools for `dlib`. See the face_recognition docs for platform-specific steps.

3. Run the backend:
```
python project/backend/app.py
```
It starts on http://127.0.0.1:5000

4. Open the frontend:
- Simply open `project/frontend/index.html` in your browser, or
- Serve it locally (e.g., using VS Code Live Server). The backend has CORS enabled.

## Usage
- Enroll tab: enter a name, capture from webcam or upload an image, then submit.
- Start Attendance: start camera; the app sends a frame every 2s to the backend. Recognized faces get a green border and are logged once per day.
- Attendance Log: shows the CSV content via the `/attendance` endpoint.

## Notes
- Performance: The frontend sends one frame every 2 seconds to reduce load. You can tweak this in `script.js`.
- Model: Using HOG detector for CPU-only environments. For better accuracy and if you have a GPU-enabled dlib, switch to `cnn` in `app.py` face_locations.
- Privacy: All processing is local; no cloud calls.

## Example Screenshots
Add screenshots or a short GIF of:
- Enrolling a user
- Live recognition with overlay
- Attendance log table


