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

    embeddings = [embeddinges for items in item['data']]
    return embeddings 
    
x_mean= np.mean(x)
y_mean=np.mean(y)
a=np.sum((x-x_mean)*(y-y_mean))
b=np.sum((x-x_mean)**2)
num=a/b
den=y_mean - a*x_mean
