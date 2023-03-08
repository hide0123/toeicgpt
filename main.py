import dotenv
import ffmpeg
import openai
import os
import pyttsx3
import tempfile

dotenv.load_dotenv()

CHATGPT = True

# Settings
MALE_VOICE = int(os.getenv("MALE_VOICE"))
FEMALE_VOICE = int(os.getenv("FEMALE_VOICE"))
WPM = int(os.getenv("WPM"))

# API key
openai.api_key = os.getenv("API_KEY")

print("Generating a script...")

message = "I am a man.\nI am a woman."

# Generate a script
if CHATGPT:
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      temperature=1,
      messages=[
          {"role": "user", "content": "Generate TOEIC Part 3 conversation in about 60 words"}
      ]
  )

  # Set a response
  message = response["choices"][0]["message"]["content"]
  message = "\n".join(filter(lambda x: x.strip(), message.split("\n")))

# print(message)

# Save a script
with open("script.txt", mode="w") as f:
  f.write(message)

# pyttsx3
engine = pyttsx3.init()

# Voices
voices = engine.getProperty("voices")
voice =[voices[MALE_VOICE].id, voices[FEMALE_VOICE].id]

# WPM
engine.setProperty("rate", WPM)

mp3 = []
lines = message.split("\n")

# Judge the speaker
if True:
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      temperature=0,
      messages=[
          {"role": "system", "content": "Answer yes or no"},
          {"role": "user", "content": '"' + lines[0] + '" Is the speaker a woman?'},
      ]
  )
  
  # Set a response
  message = response["choices"][0]["message"]["content"]
  
  if "Yes" in message:
    voice[0], voice[1] = voice[1], voice[0]

with tempfile.TemporaryDirectory() as tmpdir:
  for i, line in enumerate(lines):
    engine.setProperty("voice", voice[i % 2])
    colon =line.find(":")
    # engine.say(line[colon+2:])
    
    # Save a voice
    file = tmpdir + "/voice" + str(i) + ".mp3"
    engine.save_to_file(line[colon+2:], file)
    engine.runAndWait()
    mp3.append(ffmpeg.input(file))

  # Concat
  (
    ffmpeg.concat(*mp3, v=0, a=1)
          .output("voice.mp3")
          .run(quiet=True, overwrite_output=True)
  )
