import os

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TOPIC = "syncai_server.public.products"
BATCH_SIZE = 16
