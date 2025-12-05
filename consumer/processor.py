def build_text(record):
    return (record.get("name", "") + " " + record.get("description", "")).strip()

def build_metadata(record):
    return {
        "id": record["id"],
        "name": record["name"],
        "updated_at": record["updated_at"]
    }
