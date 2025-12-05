import json
import asyncio
from aiokafka import AIOKafkaConsumer
import pinecone
from config import *
from embedder import embed_texts
from processor import build_text, build_metadata

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
index = pinecone.Index(PINECONE_INDEX)

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

            batch.append((data["id"], text, metadata))

            if len(batch) >= BATCH_SIZE:
                await process_batch(batch)
                batch = []

    finally:
        await consumer.stop()

async def process_batch(batch):
    print(f"Processing batch {len(batch)}...")
    ids = [str(x[0]) for x in batch]
    texts = [x[1] for x in batch]
    metas = [x[2] for x in batch]

    vectors = embed_texts(texts)

    items = []
    for i in range(len(vectors)):
        items.append((ids[i], vectors[i], metas[i]))

    index.upsert(vectors=items)
    print(f"Upserted {len(items)} vectors.")

if __name__ == "__main__":
    asyncio.run(consume())
