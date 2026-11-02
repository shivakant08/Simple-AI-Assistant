import os
import json
from dotenv import load_dotenv
from semantic_search_test import get_embeddings, cosine_similarity
load_dotenv()

KB_FOLDER = os.getenv("KB_FOLDER") 
VECTOR_STORE_FILE=os.getenv("VECTOR_STORE_FILE") 

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


def add_embeddings(chunks):
    for chunk in chunks:
        vector = get_embeddings(chunk["text"])
        chunk["vector"] = vector
    return chunks
  

def search(query, chunks,top_k=3):
    query_vector = get_embeddings(query)
    results = []

    for chunk in chunks:
        score = cosine_similarity(query_vector, chunk["vector"])
        results.append({
            "score": float(score),
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "size": len(chunk["text"]),
            "text": chunk["text"]
        })

    results.sort(key = lambda x: x["score"], reverse=True)
    return results[:top_k]

def chunk_document(document):
    chunks=[]
    chunk_id = 0

    for part in document["text"].split("\n\n"):
        part = part.strip()
        if part:
            chunks.append({
                "source": document["source"],
                "chunk_id": chunk_id,
                "text": part
            })
            chunk_id += 1
    return chunks

def create_chunk():
    documents = load_documents()
    chunks=[]
    for doc in documents:
        chunks.extend(chunk_document(doc))
    return chunks

def test_search():
    chunks=[]
    if os.path.exists(VECTOR_STORE_FILE):
        chunks = load_vector_store()
        print(f"Loaded {len(chunks)} chunks from vector store.")
    else:
        chunks = create_chunk()
        chunks = add_embeddings(chunks)
        save_vector_store(chunks)
        print(f"Created and saved {len(chunks)} chunks to vector store.")
    
    query = "What are the benefits of Maternity Leave?"
    results = search(query, chunks)

    for result in results:
        print(f"Score: {result['score']:.4f}, Source: {result['source']}, Chunk ID: {result['chunk_id']}, Size: {result['size']} characters")
        print(f"Text: {result['text']}\n")

def save_vector_store(chunks):
    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4)

def load_vector_store():
    with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    test_search()