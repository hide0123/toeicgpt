import dotenv
import openai
import os
import pyttsx3

dotenv.load_dotenv()

# API Key
openai.api_key = os.getenv("API_KEY")

print("Generating script...")

# ChatGPT
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.0,
    messages=[
        {"role": "user", "content": "Generate TOEIC Part 3 example script"}
    ]
)

# Show response
message = response['choices'][0]['message']['content']
# print(message)

engine = pyttsx3.init()

# Voice
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[1].id)

# WPM
engine.setProperty('rate', int(os.getenv("WPM", 180)))

# Say
# engine.say(message)

# Save
engine.save_to_file(message, "voice.mp3")

with open("script.txt", mode="w") as f:
  f.write(message)

# Run and wait
engine.runAndWait()
