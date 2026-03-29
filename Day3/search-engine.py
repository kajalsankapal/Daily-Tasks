import re
STOP_WORDS = {"the", "is", "at", "in", "on", "and", "a", "an", "to", "of"}

SYNONYMS = {
    "ai": ["artificial", "intelligence"],
    "ml": ["machine", "learning"],
    "happy": ["joyful", "glad"],
    "llm": ["large", "language", "model"],
    "nlp": ["natural", "language", "processing"]
}

def preprocess_text(text):
    text = text.lower()  
    text = re.sub(r'[^\w\s]', '', text)  
    words = text.split()
    words = [word for word in words if word not in STOP_WORDS]
    return words

def expand_query(query_words):
    expanded = list(query_words)
    
    for word in query_words:
        if word in SYNONYMS:
            expanded.extend(SYNONYMS[word])
    
    return expanded

def jaccard_similarity(query, sentence):
    set1 = set(query)
    set2 = set(sentence)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    if len(union) == 0:
        return 0
    
    return len(intersection) / len(union)
    
def load_corpus(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    sentences = [re.sub(r'^\d+\.\s*', '', line.strip()) for line in lines if line.strip()]
    return sentences
    
def search(query, sentences):
    query_words = preprocess_text(query)
    query_words = expand_query(query_words)  
    results = []
    
    for sentence in sentences:
        processed_sentence = preprocess_text(sentence)
        score = jaccard_similarity(query_words, processed_sentence)
        results.append((sentence, score))
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results

if __name__ == "__main__":
    file_path = "corpus.txt"
    sentences = load_corpus(file_path)
    
    user_query = input("Enter your search query: ")
    
    if user_query.strip() == "":
        print("Please enter a valid query")
    else:
        results = search(user_query, sentences)
        
        print("\nTop Results:\n")
        
        for sentence, score in results[:5]:  
            print(f"Score: {score:.2f} | {sentence}")
