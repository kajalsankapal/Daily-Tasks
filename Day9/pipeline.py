import os
import time
import re
from dotenv import load_dotenv
from google import genai
import PyPDF2

load_dotenv()
client = genai.Client(api_key=os.getenv("gemini_api_key"))

class InputValidator:

    def validate(self, query: str):
        if len(query) > 300:
            return False, "Query too long! Max 300 characters allowed."

        if not query.strip():
            return False, "Query cannot be empty."

        if not re.search(r"[a-zA-Z0-9]", query):
            return False, "Query must contain meaningful text."

        return True, "Valid"

def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def chunk_text(text, chunk_size=300):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

def retrieve_context(query, chunks):
    start_time = time.time()

    # Simple keyword matching (basic RAG)
    best_chunk = ""
    max_score = 0

    for chunk in chunks:
        score = sum(word.lower() in chunk.lower() for word in query.split())
        if score > max_score:
            max_score = score
            best_chunk = chunk

    retrieval_time = (time.time() - start_time) * 1000
    return best_chunk, retrieval_time

def generate_response(context, query):
    start_time = time.time()

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Context: {context}\n\nQuestion: {query}"
        )

        answer = response.text

    except Exception:
        return None, "API Error", 0

    generation_time = (time.time() - start_time) * 1000
    return answer, None, generation_time

def log_performance(retrieval_time, generation_time):
    with open("performance.log", "a") as f:
        f.write(
            f"retrieval_time_ms={retrieval_time:.2f}, "
            f"generation_time_ms={generation_time:.2f}\n"
        )

def run_pipeline(query, chunks):

    validator = InputValidator()

    # Step 1: Validate
    is_valid, message = validator.validate(query)
    if not is_valid:
        return f"{message}"
    context, retrieval_time = retrieve_context(query, chunks)
    answer, error, generation_time = generate_response(context, query)

    if error:
        return " Service temporarily unavailable. Please try again in 30 seconds."

    log_performance(retrieval_time, generation_time)
    return answer

if __name__ == "__main__":

    print(" Loading PDF...")
    pdf_text = read_pdf("data.pdf")

    print(" Chunking text...")
    chunks = chunk_text(pdf_text)

    print(" System Ready! Ask your questions\n")

    while True:
        user_query = input("Enter your query (or type 'exit'): ")

        if user_query.lower() == "exit":
            break

        result = run_pipeline(user_query, chunks)
        print("\nResponse:\n", result)
        print("\n" + "-"*50)