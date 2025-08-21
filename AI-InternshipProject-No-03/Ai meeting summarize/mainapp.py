from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
from openai import OpenAI
import os
import tempfile

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load Whisper model once
print("Loading Whisper model...")
model = whisper.load_model("base")

# Configure OpenAI (DeepSeek) client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# Route to upload and process audio
@app.route('/api/meeting/mom', methods=['POST'])
def convert_audio_to_mom():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if not file.filename.endswith('.mp3'):
        return jsonify({'error': 'Only .mp3 files are supported'}), 400

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        file.save(temp_audio.name)
        audio_path = temp_audio.name

    try:
        # Transcribe audio
        print("Transcribing audio...")
        result = model.transcribe(audio_path)
        transcribed_text = result["text"]

        # Send to DeepSeek for Minutes of Meeting
        print("Generating Minutes of Meeting...")
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost",  # Replace with your domain if deployed
                "X-Title": "Meeting Summarizer API"
            },
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {
                    "role": "user",
                    "content": f"Convert the following text into professional minutes of meeting:\n\n{transcribed_text}"
                }
            ]
        )
        

        # Return the MoM
        mom_summary = completion.choices[0].message.content
        return jsonify({
            "status": "success",
            "minutes_of_meeting": mom_summary
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
