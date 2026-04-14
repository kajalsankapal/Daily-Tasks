# 🎧 Audio Transcription AI Agent (with UI)

## 📌 Overview

This project is an **AI system** that processes audio files and provides intelligent outputs such as transcription, summary, and keyword extraction.
The system follows a complete pipeline:
•	Audio → Transcription → Cleaning → Validation → Intent Routing → AI Processing → Output

It includes:

* 🧠 AI backend (Whisper + Gemini)
* 🎨 Interactive frontend (Streamlit UI)
* 📊 Performance tracking
* 📝 Logging system

---

## 🚀 Features

### 🎧 Audio Processing

* Convert audio (.mp3 / .wav) into text
* Supports multilingual audio (Hindi, Marathi, English, etc.)
* Optional translation to English

---

### 🧠 Intelligent Processing

* Full Transcript
* Summary generation
* Keyword extraction

---

### 🎨 Streamlit UI

* Upload audio file
* Audio preview player 🎧
* Select task (Transcript / Summary / Keywords)
* Choose translation option
* View results instantly
* Download output as file 📥

---

### 📊 Performance Metrics

* Transcription Time
* Gemini API Response Time
* Approx Token Count

---

### 🛡️ Error Handling

* Empty input detection
* Invalid file format handling
* Noise / short audio filtering
* Gemini failure fallback

---

### 📝 Logging System

* Logs stored in `logs/log.txt`
* Tracks:

  * File name
  * Task performed
  * Tokens
  * Processing time
  * Output preview

---

## 🛠️ Tech Stack

* **Python**
* **OpenAI Whisper** (Speech-to-Text)
* **Google Gemini API** (LLM processing)
* **Streamlit** (Frontend UI)
* **dotenv** (Environment variables)

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone <your-repo-link>
cd Audio-Transcript-Project
```

---

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install openai-whisper torch streamlit google-generativeai python-dotenv
```

---

### 4. Install FFmpeg

Download from:
https://ffmpeg.org/download.html

Add `ffmpeg/bin` to system PATH.

---

### 5. Setup API Key

Create a `.env` file:

```env
gemini_api_key=your_api_key_here
```

---

## ▶️ How to Run

### 🔹 Run Terminal Version

```bash
py -3.10 model-accuracy.py
```

---

### 🔹 Run UI (Recommended)

```bash
streamlit run app.py
```

Then open:

```plaintext
http://localhost:8501
```

---

## 🧠 System Architecture

```plaintext
Audio Input
   ↓
Whisper Transcription
   ↓
Text Cleaning
   ↓
Validation Layer (Day 13)
   ↓
Intent Selection (User)
   ↓
Gemini Processing
   ↓
Output + Metrics + Logs
```

---

## 📊 Example Output

```plaintext
=== SUMMARY ===
This audio explains a transcription system...

--- PERFORMANCE METRICS ---
Transcription Time: 3.21 sec
Gemini Time: 1.12 sec
Approx Tokens: 120
```

---

## 📁 Project Structure

```plaintext
Audio-Transcript-Project/
│
├── app.py                # Streamlit UI
├── model-accuracy.py     # Main backend script
├── .env                  # API key
├── requirements.txt
├── logs/
│   └── log.txt
├── Day11/
├── Day12/
├── Day13/
├── Day14/
├── Day15/
```

---

## 🧪 Testing & Evaluation

| Test Case    | Result     |
| ------------ | ---------- |
| Normal Audio | ✅ Success  |
| Empty Input  | ✅ Handled  |
| Noise Audio  | ✅ Rejected |
| Long Audio   | ✅ Trimmed  |
| Invalid File | ✅ Handled  |

---

## ⚠️ Limitations

* Whisper may normalize output to English in some cases
* Accuracy depends on audio quality
* Base model has limited regional language performance

---

## 🔥 Improvements Implemented

* Added Streamlit UI for better user experience
* Implemented optional translation feature
* Added performance tracking (latency + tokens)
* Introduced logging system
* Improved error handling and robustness

---

## 🎯 Conclusion

This project demonstrates a **complete AI pipeline**, including:

* Data processing (Day 11)
* Intelligent routing (Day 12)
* Robust error handling (Day 13)
* Performance optimization (Day 14)
* UI + final deployment structure (Day 15)

---

## 👩‍💻 Author

Developed as part of AI/ML project tasks.

---

## 📌 Note

This project is designed for **learning and demonstration purposes**, showcasing a real-world AI workflow with minimal complexity.
