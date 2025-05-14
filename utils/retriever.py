import openai
import os
from dotenv import load_dotenv
import chromadb

load_dotenv()
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_API_KEY")
openai.api_base = os.getenv("AZURE_API_BASE")
openai.api_version = os.getenv("AZURE_API_VERSION")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="psy_docs")

def retrieve_context(query, k=5):
    query_embedding = openai.Embedding.create(input=query, engine="text-embedding-ada-002")['data'][0]['embedding']
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results['documents'][0] if results['documents'] else []