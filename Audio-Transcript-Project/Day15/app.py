import streamlit as st
import whisper
from google import genai
from dotenv import load_dotenv
import os
import time
from datetime import datetime

load_dotenv(dotenv_path="../../.env")
api_key = os.getenv("gemini_api_key")
client = genai.Client(api_key=api_key)
model = whisper.load_model("medium")

# Create logs folder
os.makedirs("logs", exist_ok=True)

#Transcription
def transcribe_audio(file_path, task_type="transcribe"):
    return model.transcribe(file_path, task=task_type)

# Clean text
def clean_text(text):
    text = text.strip()
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

# Gemini
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

st.set_page_config(page_title="Audio AI Agent", layout="centered")
st.title("🎧 Audio Transcription AI Agent")
st.markdown("Convert audio into transcript, summary, or keywords using AI")

#FILE UPLOAD
st.subheader("📤 Upload Audio")
uploaded_file = st.file_uploader("Upload .mp3 or .wav file", type=["mp3", "wav"])

# AUDIO PLAYER
if uploaded_file is not None:
    st.subheader("🎧 Audio Preview")
    st.audio(uploaded_file)
    st.write(f"File Name: {uploaded_file.name}")

# OPTIONS
# st.subheader("⚙️ Settings")

col1, col2 = st.columns(2)

with col1:
    translate = st.radio("Translate to English?", ["No", "Yes"])

with col2:
    task = st.selectbox(
        "Select Task",
        ["Full Transcript", "Summary", "Keywords"]
    )

#PROCESS BUTTON
if st.button("🚀 Process Audio"):
    if uploaded_file is None:
        st.error("Please upload an audio file")
    else:
        file_path = uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        try:
            with st.spinner("Processing audio..."):

                #Transcription
                start_transcribe = time.time()
                if translate == "Yes":
                    result = transcribe_audio(file_path, "translate")
                else:
                    result = transcribe_audio(file_path, "transcribe")
                end_transcribe = time.time()
                transcription_time = end_transcribe - start_transcribe
                cleaned = clean_text(result["text"])

                #VALIDATION
                if not cleaned.strip():
                    st.error("No valid speech detected.")
                    st.stop()

                if len(cleaned.split()) < 3:
                    st.error("Audio too short or unclear.")
                    st.stop()

                cleaned = cleaned[:1000]
                token_count = len(cleaned.split())
                gemini_time = 0
                output_text = ""

                if task == "Full Transcript":
                    output_text = cleaned
                else:
                    if task == "Summary":
                        prompt = f"Summarize:\n{cleaned}"
                    else:
                        prompt = f"Keywords:\n{cleaned}"

                    start_gemini = time.time()
                    output_text = call_gemini(prompt)
                    end_gemini = time.time()
                    gemini_time = end_gemini - start_gemini

            #RESULT
            st.subheader("📄 Result")
            st.success("Processing complete!")
            st.write(output_text)

            #DOWNLOAD BUTTON 
            st.download_button(
                label="📥 Download Output",
                data=output_text,
                file_name="output.txt",
                mime="text/plain"
            )

            #METRICS
            st.subheader("📊 Performance Metrics")

            col1, col2, col3 = st.columns(3)

            col1.metric("Transcription Time", f"{transcription_time:.2f}s")

            if task != "Full Transcript":
                col2.metric("Gemini Time", f"{gemini_time:.2f}s")
            else:
                col2.metric("Gemini Time", "N/A")
            col3.metric("Tokens", token_count)

            #LOG
            log_entry = f"""
Time: {datetime.now()}
File: {file_path}
Task: {task}
Translation: {translate}
Tokens: {token_count}
Transcription Time: {transcription_time:.2f}
Gemini Time: {gemini_time:.2f}
Output: {output_text[:100]}...
----------------------------------------
"""
            save_log(log_entry)

        except Exception as e:
            st.error(str(e))