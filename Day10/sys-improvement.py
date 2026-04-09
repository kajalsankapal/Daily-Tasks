import os
import time
import re
from dotenv import load_dotenv
from google import genai
import PyPDF2

load_dotenv()
api_key = os.getenv("gemini_api_key")

if not api_key:
    raise ValueError("API key not found. Check your .env file.")

client = genai.Client(api_key=api_key)

class InputValidator:
    def validate(self, query):
        if len(query) > 300:
            return False
        if not query.strip():
            return False
        if not re.search(r"[a-zA-Z0-9]", query):
            return False
        return True

def read_pdf(file):
    text = ""
    with open(file, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def chunk_text(text, size=600, overlap=100):
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunks.append(text[i:i + size])
    return chunks

def retrieve(query, chunks):
    start = time.time()

    best_chunk = ""
    best_score = 0

    for chunk in chunks:
        score = 0
        for word in query.lower().split():
            if word in chunk.lower():
                score += 2

        if score > best_score:
            best_score = score
            best_chunk = chunk

    retrieval_time = (time.time() - start) * 1000
    return best_chunk, retrieval_time

def generate(context, query):
    start = time.time()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are a strict assistant.

Answer ONLY from the given context.
If answer is not present, say: I DON'T KNOW.

Context:
{context}

Question:
{query}
"""
        )

        answer = response.text

    except Exception as e:
        print("REAL ERROR:", e)
        return None, 0

    generation_time = (time.time() - start) * 1000
    return answer, generation_time

def run_test(chunks, questions):
    results = []

    validator = InputValidator()

    for q in questions:

        if not validator.validate(q):
            print("Invalid Query")
            continue

        context, r_time = retrieve(q, chunks)
        answer, g_time = generate(context, q)

        if answer is None:
            answer = "Service temporarily unavailable"

        print("\nQ:", q)
        print("Answer:", answer)

        score = int(input("Enter groundedness score (1-5): "))
        results.append(score)

    return results
if __name__ == "__main__":

    print("Loading PDF...")
    text = read_pdf("data.pdf")

    questions = [
        "I'm seeing Error XV-505 in my terminal. What is the root cause and how do I fix it?",
        "My system is extremely laggy. Which shards should I be worried about and what is the specific command to reset them?",
        "Can I bypass the Theta-Sync requirement to install this on my old i7 laptop?",
        "How does the OS handle user login now that passwords and 2FA are deprecated?",
        "I have a MAC address that was black-holed by the Wraith Firewall. Can I unblock it using the Galactic-Relay?"
    ]

    print("\n--- BEFORE TUNING ---")
    chunks_small = chunk_text(text, size=200, overlap=50)
    before_scores = run_test(chunks_small, questions)

    print("\n--- AFTER TUNING ---")
    chunks_large = chunk_text(text, size=600, overlap=100)
    after_scores = run_test(chunks_large, questions)

    print("\n=== FINAL COMPARISON ===")
    print(f"{'Q.No':<10}{'Before':<10}{'After':<10}")

    for i in range(len(questions)):
        print(f"{i+1:<10}{before_scores[i]:<10}{after_scores[i]:<10}")

    print("\nAverage Before:", sum(before_scores)/len(before_scores))
    print("Average After :", sum(after_scores)/len(after_scores))
