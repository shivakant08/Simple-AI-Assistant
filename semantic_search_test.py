from openai import OpenAI
import os
import numpy
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
   base_url = os.getenv("BASE_URL"),
   api_key = os.getenv("API_KEY")
)

def get_embeddings(text):

    response=client.embeddings.create(
        model=os.getenv("EMBED_MODEL"),
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(A,B):
    dot_product = numpy.dot(A, B)
    lenA = numpy.linalg.norm(A)
    lenB = numpy.linalg.norm(B)
    return dot_product/ (lenA*lenB)

text1="Python is  a programming language"
text2="Python is used to write AI related code snippets"
text3 = "I love praying and meditation in the morning"

emb1 = get_embeddings(text1)
emb2 = get_embeddings(text2)
emb3 = get_embeddings(text3)

similarity1 = cosine_similarity(emb1, emb2)
similarity2 = cosine_similarity(emb1, emb3)


print(f"Similarity between text1 and text2: {similarity1:.2f}")
print(f"Similarity between text1 and text3: {similarity2:.2f}")
