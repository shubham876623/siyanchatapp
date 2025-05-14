import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_API_KEY")
openai.api_base = os.getenv("AZURE_API_BASE")
openai.api_version = os.getenv("AZURE_API_VERSION")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="psy_docs")

def embed_document(text, file_name):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    ids = [f"{file_name}_{i}" for i in range(len(chunks))]
    embeddings = [
        openai.Embedding.create(input=chunk, engine="text-embedding-ada-002")['data'][0]['embedding']
        for chunk in chunks
    ]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=[{"source": file_name}] * len(chunks))