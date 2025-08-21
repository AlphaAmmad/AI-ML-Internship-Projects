import whisper

# Load Whisper model (base is a good balance between speed and accuracy)
model = whisper.load_model("base")

# Path to your audio file
audio_path = "/home/shahzaibkhan/projects/Ammad Stuff/Ai Project 3/Ai meeting summarize/Sec Growth DataScience staff meeting Sep 14 2022.mp3"

# Transcribe the audio
print("Transcribing...")
result = model.transcribe(audio_path)

# Store the transcribed text in a variable
transcribed_text = result["text"]

# Output
print("\n📝 Transcribed Text: \n\n", transcribed_text)

from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="deepseek/deepseek-r1-0528:free",
  messages=[
    {
      "role": "user",
      "content": "convert the following text into minutes of meeting ${transcribed_text}"
    }
  ]
)
print(completion.choices[0].message.content)
