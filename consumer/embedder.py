import requests
import json

def embed_local(texts):
    if isinstance(texts, str):
        texts = [texts]

    payload = {
        "model": "nomic-embed-text",
        "input": texts
    }

    r = requests.post("http://localhost:11434/api/embeddings", json=payload)
    data = r.json()

    embeddings = [item["embedding"] for item in data["data"]]
    return embeddings
