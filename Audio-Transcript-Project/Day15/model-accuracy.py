import whisper
from datetime import datetime
from google import genai
from dotenv import load_dotenv
import os
import time

#Load API Key
load_dotenv(dotenv_path="../../.env")
api_key = os.getenv("gemini_api_key")
client = genai.Client(api_key=api_key)
model = whisper.load_model("medium")

#Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

#Transcription
def transcribe_audio(file_path,task_type="transcribe"):
    return model.transcribe(file_path,task=task_type)

#Clean text
def clean_text(text):
    text = text.strip()
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

#Intent Router
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
        return "transcript"

#Gemini Processing
def call_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

#Save logs
def save_log(entry):
    with open("logs/log.txt", "a") as f:
        f.write(entry + "\n")

#MAIN
if __name__ == "__main__":

    file_name = input("Enter audio file name (e.g., sample.mp3): ").strip()

    #Input validations
    if not file_name:
        print("Error: No file name provided.")
        exit()

    if not os.path.exists(file_name):
        print("Error: File not found.")
        exit()

    if not file_name.endswith((".mp3", ".wav")):
        print("Error: Invalid file format.")
        exit()

    try:
        translate_choice = input("Do you want translation to English? (yes/no): ").lower()

        if translate_choice not in ["yes", "no"]:
            print("Invalid choice, defaulting to no translation")
            translate_choice = "no"

        start_transcribe = time.time()

        if translate_choice == "yes":
            result = model.transcribe(file_name, task_type="translate")
        else:
            result = transcribe_audio(file_name, task_type="transcribe")

        end_transcribe = time.time()

        transcription_time = end_transcribe - start_transcribe

        #Clean text
        cleaned = clean_text(result["text"])

        if not cleaned.strip():
            print("No valid speech detected in audio.")
            exit()

        if len(cleaned.split()) < 3:
            print("Audio not clear or too short.")
            exit()
        cleaned = cleaned[:1000]

        #Token count
        token_count = len(cleaned.split())

        # Intent
        intent = route_intent()
        gemini_time = 0
        output_text = ""

        #Transcript
        if intent == "transcript":
            print("\n=== FULL TRANSCRIPT ===")
            print(cleaned)
            output_text = cleaned

        #Gemini tasks
        elif intent in ["summary", "keywords"]:
            if intent == "summary":
                prompt = f"Summarize:\n{cleaned}"
            else:
                prompt = f"Keywords:\n{cleaned}"

            #Gemini timing
            start_gemini = time.time()
            output = call_gemini(prompt)
            end_gemini = time.time()

            gemini_time = end_gemini - start_gemini

            if intent == "summary":
                print("\n=== SUMMARY ===")
            else:
                print("\n=== KEYWORDS ===")

            print(output)
            output_text = output

        #PERFORMANCE METRICS
        print("\n--- PERFORMANCE METRICS ---")
        print(f"Transcription Time: {transcription_time:.2f} sec")
        if intent in ["summary", "keywords"]:
            print(f"Gemini Time: {gemini_time:.2f} sec")
        print(f"Approx Tokens: {token_count}")

        #SAVE LOG
        log_entry = f"""
Time: {datetime.now()}
File: {file_name}
Translation: {translate_choice}
Intent: {intent}
Tokens: {token_count}
Transcription Time: {transcription_time:.2f}
Gemini Time: {gemini_time:.2f}
Output: {output_text[:100]}...
----------------------------------------
"""
        save_log(log_entry)

    except Exception as e:
        print("Error:", str(e))