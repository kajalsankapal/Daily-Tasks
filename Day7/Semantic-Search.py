from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

with open("corpus.txt", "r", encoding="utf-8") as file:
    documents = [line.strip() for line in file.readlines() if line.strip()]

print(f"Loaded {len(documents)} sentences.")
doc_embeddings = model.encode(documents)

while True:
    query = input("\nEnter your search query (or type 'exit'): ")

    if query.lower() == "exit":
        print("Exiting search...")
        break

    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    top_indices = similarities.argsort()[-3:][::-1]

    print("\nTop 3 Results:\n")

    for i in top_indices:
        print(f"Sentence: {documents[i]}")
        print(f"Similarity Score: {similarities[i]:.4f}")
        print("-" * 50)
