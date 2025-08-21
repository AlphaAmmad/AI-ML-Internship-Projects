import os
import io
import csv
import pickle
from datetime import datetime
from typing import Dict, List, Tuple

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np

# Face recognition imports
import face_recognition

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENCODINGS_PATH = os.path.join(BASE_DIR, 'encodings.pkl')
ATTENDANCE_PATH = os.path.join(BASE_DIR, 'attendance.csv')

# Ensure required files/directories exist
os.makedirs(BASE_DIR, exist_ok=True)

# Initialize encodings storage if not present
if not os.path.exists(ENCODINGS_PATH):
    with open(ENCODINGS_PATH, 'wb') as f:
        pickle.dump({"names": [], "encodings": []}, f)

# Initialize attendance CSV with header if not present
if not os.path.exists(ATTENDANCE_PATH):
    with open(ATTENDANCE_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Date', 'Time'])


app = Flask(__name__)
CORS(app)  # Enable CORS for all domains; adjust origins in production


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def load_known_encodings() -> Dict[str, List]:
    """Load known encodings from disk, returning a dict with 'names' and 'encodings'."""
    try:
        with open(ENCODINGS_PATH, 'rb') as f:
            data = pickle.load(f)
            if not isinstance(data, dict) or 'names' not in data or 'encodings' not in data:
                return {"names": [], "encodings": []}
            return data
    except Exception:
        return {"names": [], "encodings": []}


def save_known_encodings(data: Dict[str, List]) -> None:
    with open(ENCODINGS_PATH, 'wb') as f:
        pickle.dump(data, f)


def decode_image_from_request(image_field: str) -> np.ndarray:
    """
    Decode an image sent as base64 data URL or raw base64 string in JSON under key `image_field`.
    Returns a NumPy array in RGB order suitable for face_recognition.
    """
    payload = request.json or {}
    b64 = payload.get(image_field)
    if not b64:
        # Try multipart form (file upload)
        if image_field in request.files:
            file_storage = request.files[image_field]
            image_bytes = file_storage.read()
        else:
            raise ValueError('No image provided')
    else:
        # If data URL, strip header
        if ',' in b64:
            b64 = b64.split(',', 1)[1]
        import base64
        image_bytes = base64.b64decode(b64)

    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return np.array(img)


def decode_images_from_request(images_field: str = 'images') -> List[np.ndarray]:
    """
    Decode multiple images from JSON array under `images_field` or from multipart form list `images`.
    Returns a list of RGB NumPy arrays. If no images provided, returns an empty list.
    """
    payload = request.json or {}
    images_list = payload.get(images_field)
    arrays: List[np.ndarray] = []
    if images_list and isinstance(images_list, list):
        import base64
        for b64 in images_list:
            if not b64:
                continue
            # Strip data URL header if present
            if ',' in b64:
                b64 = b64.split(',', 1)[1]
            try:
                image_bytes = base64.b64decode(b64)
                img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
                arrays.append(np.array(img))
            except Exception:
                continue
        return arrays

    # Multipart fallback: multiple files named 'images'
    if 'images' in request.files:
        files = request.files.getlist('images')
        for fs in files:
            try:
                img = Image.open(io.BytesIO(fs.read())).convert('RGB')
                arrays.append(np.array(img))
            except Exception:
                continue
    return arrays


def log_attendance_once_per_day(name: str) -> None:
    """Append attendance row if the person hasn't been logged today."""
    today = datetime.now().strftime('%Y-%m-%d')
    now_time = datetime.now().strftime('%H:%M:%S')

    # Read existing to check duplicates
    already_logged_today = False
    if os.path.exists(ATTENDANCE_PATH):
        with open(ATTENDANCE_PATH, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Name') == name and row.get('Date') == today:
                    already_logged_today = True
                    break

    if not already_logged_today:
        with open(ATTENDANCE_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, today, now_time])


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------

@app.route('/enroll', methods=['POST'])
def enroll():
    """
    Enroll a person by name with one or more images (multiple angles improve recognition).
    Accepts:
      - JSON: {"name": "Alice", "image": "data:image/jpeg;base64,..."}
      - JSON (multiple): {"name": "Alice", "images": ["data:image/...", "data:image/..."]}
      - Or multipart/form-data with fields 'name' and file 'image' or multiple files 'images'
    """
    try:
        name = None
        if request.is_json:
            name = (request.json or {}).get('name')
        if not name:
            name = request.form.get('name')
        if not name:
            return jsonify({'success': False, 'error': 'Name is required'}), 400

        # Collect one or more images
        images_arrays: List[np.ndarray] = []
        try:
            # Multiple first
            multi = decode_images_from_request('images')
            if multi:
                images_arrays.extend(multi)
        except Exception:
            pass
        # Single fallback
        try:
            single = decode_image_from_request('image')
            if isinstance(single, np.ndarray):
                images_arrays.append(single)
        except Exception:
            pass

        if not images_arrays:
            return jsonify({'success': False, 'error': 'No images provided'}), 400

        # For each image, detect single face and compute encoding
        collected_encodings: List[np.ndarray] = []
        for image_array in images_arrays:
            face_locations = face_recognition.face_locations(image_array, model='hog')
            if len(face_locations) == 0:
                # Skip images without a face
                continue
            # If multiple faces, pick the largest box (assume subject is closest)
            if len(face_locations) > 1:
                def area(box):
                    top, right, bottom, left = box
                    return (bottom - top) * (right - left)
                face_locations = [max(face_locations, key=area)]
            encs = face_recognition.face_encodings(image_array, known_face_locations=face_locations)
            if encs:
                collected_encodings.append(encs[0])

        if not collected_encodings:
            return jsonify({'success': False, 'error': 'No valid face encodings found in provided images'}), 400

        data = load_known_encodings()
        # Store each encoding separately with the same name; recognition will pick nearest
        for enc in collected_encodings:
            data['names'].append(name)
            data['encodings'].append(enc)
        save_known_encodings(data)

        return jsonify({'success': True, 'message': f'Enrolled {name} with {len(collected_encodings)} sample(s)'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/recognize', methods=['POST'])
def recognize():
    """
    Recognize faces in a frame and log attendance once per day.
    Accepts JSON: {"image": "data:image/jpeg;base64,..."}
    Returns JSON with detected boxes and names.
    """
    try:
        image_array = decode_image_from_request('image')  # RGB
        data = load_known_encodings()
        known_encodings = data.get('encodings', [])
        known_names = data.get('names', [])

        # Detect faces
        face_locations = face_recognition.face_locations(image_array, model='hog')
        face_encs = face_recognition.face_encodings(image_array, known_face_locations=face_locations)

        results = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encs):
            name = 'Unknown'
            if known_encodings:
                # Compare to known encodings
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                if len(face_distances) > 0:
                    best_match_index = int(np.argmin(face_distances))
                    if matches[best_match_index]:
                        name = known_names[best_match_index]

            # Log attendance only for recognized faces
            if name != 'Unknown':
                log_attendance_once_per_day(name)

            results.append({
                'name': name,
                'box': {'top': int(top), 'right': int(right), 'bottom': int(bottom), 'left': int(left)}
            })

        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/attendance', methods=['GET'])
def attendance():
    """Return attendance as JSON list of {Name, Date, Time}."""
    try:
        records = []
        if os.path.exists(ATTENDANCE_PATH):
            with open(ATTENDANCE_PATH, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append({'Name': row.get('Name'), 'Date': row.get('Date'), 'Time': row.get('Time')})
        return jsonify({'success': True, 'records': records})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # Tip: Set host='0.0.0.0' to allow LAN access
    app.run(host='127.0.0.1', port=5000, debug=True)

