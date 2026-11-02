import os
from openai import OpenAI
from dotenv import load_dotenv
from semantic_search_test import get_embeddings, cosine_similarity
load_dotenv()

client= OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key = os.getenv("API_KEY")
)

EMBEDDING_MODEL = os.getenv("EMBED_MODEL")
KB_FOLDER = os.getenv("KB_FOLDER")  

def load_documents(folder=KB_FOLDER):
    documents = []

    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            documents.append({
                "source": filename,
                "text": f.read()
            })
    return documents


def add_embeddings(documents):
    for doc in documents:
        vector = get_embeddings(doc["text"]) 
        doc["vector"] = vector

    return documents

def search(query, documents,top_k=3):
    query_vector = get_embeddings(query)
    results = []

    for doc in documents:
        score = cosine_similarity(query_vector, doc["vector"])
        results.append({
            "score": score,
            "source": doc["source"],
            "size": len(doc["text"])
        })

    results.sort(key = lambda x: x["score"], reverse=True)
    return results[:top_k]


def test_search():
    documents = load_documents()
    documents = add_embeddings(documents)
    query = "How many days will i get for maternity leave?"
    results = search(query, documents)

    for result in results:
        print(f"Score: {result['score']:.2f}, Source: {result['source']}, Size: {result['size']}")


test_search()