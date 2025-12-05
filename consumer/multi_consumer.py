import asyncio, json
from aiokafka import AIOKafkaConsumer
from qdrant_client import QdrantClient, models
from config import *
from embedder import embed_local
from processor import build_text_from_pg, build_text_from_mongo, build_metadata

# init qdrant
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE)
)

async def consume_topics(topics):
    consumer = AIOKafkaConsumer(
        *topics,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="syncai-multi-consumer",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        batch = []
        async for msg in consumer:
            # msg.topic identifies source
            raw = msg.value.decode("utf-8")
            try:
                data = json.loads(raw)
            except Exception:
                # sometimes Debezium wraps differently; try evaluate
                data = json.loads(raw.replace("'", '"'))
            # Debezium unwrap provides 'after' for row state OR direct fields if unwrap true
            record = data.get("after") or data.get("payload") or data

            if msg.topic == TOPIC_PG:
                text = build_text_from_pg(record)
                meta = build_metadata("postgres", record)
                id_ = str(record.get("id"))
            elif msg.topic == TOPIC_MONGO:
                text = build_text_from_mongo(record)
                meta = build_metadata("mongo", record)
                id_ = str(record.get("_id") or record.get("id"))
            else:
                continue

            batch.append((id_, text, meta))

            if len(batch) >= BATCH_SIZE:
                await process_batch(batch)
                batch = []
    finally:
        await consumer.stop()

async def process_batch(batch):
    ids = [b[0] for b in batch]
    texts = [b[1] for b in batch]
    metas = [b[2] for b in batch]

    vectors = embed_local(texts)

    points = []
    for i, vec in enumerate(vectors):
        points.append(models.PointStruct(id=ids[i], vector=vec, payload=metas[i]))

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Upserted {len(points)} points.")

if __name__ == "__main__":
    asyncio.run(consume_topics([TOPIC_PG, TOPIC_MONGO]))
