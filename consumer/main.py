import json
import asyncio
from aiokafka import AIOKafkaConsumer
from qdrant_client import QdrantClient, models

from config import *
from embedder import embed_local
from processor import build_text, build_metadata

# Init Qdrant
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Create collection if not exists
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE)
)

async def consume():
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="syncai-consumer"
    )

    await consumer.start()
    print("Consumer started...")

    batch = []

    try:
        async for msg in consumer:
            data = json.loads(msg.value)

            text = build_text(data)
            metadata = build_metadata(data)

            batch.append([data["id"], text, metadata])

            if len(batch) >= BATCH_SIZE:
                await process_batch(batch)
                batch = []

    finally:
        await consumer.stop()

async def process_batch(batch):
    ids = [b[0] for b in batch]
    texts = [b[1] for b in batch]
    metadatas = [b[2] for b in batch]

    embeddings = embed_local(texts)

    points = []
    for i in range(len(embeddings)):
        points.append(
            models.PointStruct(
                id=str(ids[i]),
                vector=embeddings[i],
                payload=metadatas[i]
            )
        )

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Inserted {len(points)} vectors into Qdrant.")

if __name__ == "__main__":
    asyncio.run(consume())
