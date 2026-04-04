import os
import faiss
import numpy as np
import PyPDF2
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("gemini_api_key"))
model = SentenceTransformer('all-MiniLM-L6-v2')

def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

print("Reading PDF...")
text = read_pdf("data.pdf")

print("Chunking text...")
chunks = chunk_text(text)

print("Creating embeddings (local model)...")
embeddings = model.encode(chunks)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings).astype("float32"))

print("Vector DB ready!")

def retrieve(query, k=2):
    query_embedding = model.encode([query])

    D, I = index.search(
        np.array(query_embedding).astype("float32"), k
    )

    return [chunks[i] for i in I[0]]

def ask_question(question):
    relevant_chunks = retrieve(question)
    context = "\n".join(relevant_chunks)

    if not context.strip():
        return "I DON'T KNOW"

    prompt = f"""
You are a helpful assistant.

RULES:
- Answer ONLY from the given context.
- If the answer is not in the context, say: I DON'T KNOW.

Context:
{context}

Question:
{question}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

while True:
    user_input = input("\nAsk your question (type 'exit' to quit): ")

    if user_input.lower() == "exit":
        print("Thankyou!")
        break

    if not user_input.strip():
        print("Please enter a valid question.")
        continue

    answer = ask_question(user_input)
    print("\nAnswer:", answer)