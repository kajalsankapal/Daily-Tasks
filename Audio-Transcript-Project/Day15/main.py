import os
import time
from datetime import datetime
import whisper
from dotenv import load_dotenv
from google import genai

load_dotenv(dotenv_path="../../.env")

api_key = os.getenv("gemini_api_key")
client = genai.Client(api_key=api_key)
model = whisper.load_model("small")

os.makedirs("logs", exist_ok=True)


def transcribe_audio(file_path, task_type="transcribe"):
    return model.transcribe(file_path, task=task_type)


def clean_text(text):
    text = text.strip()
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


def call_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text


def save_log(entry):
    with open("logs/log.txt", "a") as f:
        f.write(entry + "\n")


def process_audio(file_path, task, language=None):
    start_transcribe = time.time()
    
    if language:
        result = model.transcribe(file_path, language=language)
    else:
        result = model.transcribe(file_path)
    end_transcribe = time.time()
    transcription_time = end_transcribe - start_transcribe

    cleaned = clean_text(result["text"])
    if not cleaned.strip():
        raise ValueError("No valid speech detected.")

    if len(cleaned.split()) < 3:
        raise ValueError("Audio too short or unclear.")

    cleaned = cleaned[:1000]
    token_count = len(cleaned.split())
    gemini_time = 0

    if task == "Full Transcript":
        output_text = cleaned
    else:
        prompt = f"Summarize:\n{cleaned}" if task == "Summary" else f"Keywords:\n{cleaned}"
        start_gemini = time.time()
        output_text = call_gemini(prompt)
        end_gemini = time.time()
        gemini_time = end_gemini - start_gemini

    log_entry = f"""
Time: {datetime.now()}
File: {file_path}
Task: {task}
Tokens: {token_count}
Transcription Time: {transcription_time:.2f}sec
Gemini Time: {gemini_time:.2f}sec
Output: {output_text[:100]}...
----------------------------------------
"""
    save_log(log_entry)

    return {
        "transcript_text": cleaned,
        "output_text": output_text,
        "transcription_time": transcription_time,
        "gemini_time": gemini_time,
        "token_count": token_count,
    }
