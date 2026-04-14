import whisper
from datetime import datetime
from google import genai
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="../../.env")

api_key = os.getenv("gemini_api_key")
client = genai.Client(api_key=api_key)

# Load Whisper
model = whisper.load_model("base")

#Transcription
def transcribe_audio(file_path):
    return model.transcribe(file_path)

# Clean text
def clean_text(text):
    text = text.strip()
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

# Intent Router
def route_intent():
    print("\nWhat do you want?")
    print("1. Full Transcript")
    print("2. Summary")
    print("3. Keywords")

    choice = input("Enter choice (1/2/3): ")

    if choice == "1":
        return "transcript"
    elif choice == "2":
        return "summary"
    elif choice == "3":
        return "keywords"
    else:
        print("Invalid choice, defaulting to transcript")

# Gemini Processing
def call_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# MAIN
if __name__ == "__main__":

    file_name = input("Enter audio file name (e.g., sample.mp3): ")

    try:
        # Step 1: Transcribe
        result = transcribe_audio(file_name)

        # Step 2: Clean
        cleaned = clean_text(result["text"])

        # Step 3: Route Intent
        intent = route_intent()

        # Step 4: Process based on intent
        if intent == "transcript":
            print("\n=== FULL TRANSCRIPT ===")
            print(cleaned)

        elif intent == "summary":
            prompt = f"Summarize this text:\n{cleaned}"
            output = call_gemini(prompt)

            print("\n=== SUMMARY ===")
            print(output)

        elif intent == "keywords":
            prompt = f"Extract important keywords from this text:\n{cleaned}"
            output = call_gemini(prompt)

            print("\n=== KEYWORDS ===")
            print(output)

    except Exception as e:
        print("Error:", str(e))