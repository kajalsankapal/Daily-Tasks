import whisper
from datetime import datetime
import os

# Load Whisper model
model = whisper.load_model("base")

# Step 1: Transcribe
def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result


# Step 2: Clean text
def clean_text(text):
    text = text.strip()
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


# Step 3: Structure output
def structure_output(result):
    text = result.get("text", "")
    
    return {
        "transcript": text,
        "language": result.get("language", "unknown"),
        "length": len(text),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# MAIN EXECUTION
if __name__ == "__main__":
    
    file_name = input("Enter audio file name (e.g., sample.mp3): ")
    file_path = os.path.join(os.getcwd(), file_name)

    try:
        # Step 1
        result = transcribe_audio(file_path)

        # Step 2
        cleaned_text = clean_text(result["text"])
        result["text"] = cleaned_text

        # Step 3
        structured = structure_output(result)

        # Final Output
        print("\n=== TRANSCRIPTION RESULT ===")
        print("Transcript:", structured["transcript"])
        print("Language:", structured["language"])
        print("Length:", structured["length"])
        print("Timestamp:", structured["timestamp"])

    except Exception as e:
        print("Error:", str(e))