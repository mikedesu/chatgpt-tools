import os
import openai
import sys
openai.api_key = os.getenv("OPENAI_API_KEY")

if len(sys.argv) < 2:
    print("Usage: python whisper.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
#print(filename)
audio_file = open(filename, "rb")
print("Transcribing audio file: " + filename)

transcript = openai.Audio.transcribe("whisper-1", audio_file)
#print(transcript)

transcript_text = transcript["text"]

#transcript_text = transcript_text.decode("utf-8")
# print the transcript text
print(transcript_text)
