import streamlit as st
import os
from main import process_audio
from audiorecorder import audiorecorder

st.set_page_config(page_title="Audio AI Agent", layout="centered")
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.block-container {
    padding-top: 2rem;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}
.result-box {
    background-color: #1e1e2f;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🎧 Audio Transcription AI Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Convert audio into insights using AI</p>", unsafe_allow_html=True)
st.divider()
file_path = None
tab1, tab2 = st.tabs(["🎤 Record Audio", "📤 Upload Audio"])

with tab1:
    st.subheader("🎤 Record Audio")

    audio = audiorecorder("Start Recording", "Stop Recording")

    if len(audio) > 0:
        st.audio(audio.export().read())

        with open("recorded.wav", "wb") as f:
            f.write(audio.export().read())

        file_path = "recorded.wav"


with tab2:
    st.subheader("📤 Upload Audio")

    uploaded_file = st.file_uploader("", type=["mp3", "wav"])

    if uploaded_file:
        st.audio(uploaded_file)

        file_path = uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

st.divider()

st.subheader("⚙️ Select Task")
task = st.selectbox(
    "Choose what you want to generate from the  audio:",
    ["Full Transcript", "Summary", "Keywords"]
)

if st.button("🚀 Process Audio"):

    if not file_path:
        st.error("❌ Please upload or record an audio file first.")
    else:
        with st.spinner("Processing... Please wait"):

            try:
                result = process_audio(file_path, task)

                st.success("Processing Completed ✅")

                st.subheader("📄 Result")
                st.markdown(f"<div class='result-box'>{result['output_text']}</div>", unsafe_allow_html=True)

                st.subheader("📊 Performance Metrics")
                col1, col2, col3 = st.columns(3)

                col1.metric("Transcription", f"{result['transcription_time']:.2f} sec")
                col2.metric("Gemini", f"{result['gemini_time']:.2f} sec")
                col3.metric("Tokens", result['token_count'])

                st.download_button(
                    "📥 Download Result",
                    result['output_text'],
                    file_name="output.txt"
                )

            except Exception as e:
                st.error(str(e))