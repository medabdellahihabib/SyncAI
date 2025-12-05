from fastapi import FastAPI
from pydantic import BaseModel
from .crud import list_sources, add_source

app = FastAPI()

class SourceIn(BaseModel):
    name: str
    type: str
    config: dict

@app.get("/sources")
def get_sources():
    return list_sources()

@app.post("/sources")
def create_source(s: SourceIn):
    add_source(s.name, s.type, s.config)
    return {"status": "ok"}
