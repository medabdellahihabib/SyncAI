def build_text_from_pg(record):
    # record is Debezium unwrap: contains fields directly (id,name,description)
    name = record.get("name","")
    desc = record.get("description","")
    return f"{name} {desc}".strip()

def build_text_from_mongo(record):
    # mongo document fields
    title = record.get("title","")
    body = record.get("body","")
    return f"{title} {body}".strip()

def build_metadata(source, record):
    meta = {"source": source}
    if "id" in record:
        meta["id"] = record["id"]
    if "_id" in record:
        meta["id"] = str(record["_id"])
    return meta
