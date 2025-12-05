from sqlalchemy import Table, Column, Integer, String, JSON
from .db import metadata, engine

sources = Table(
    "sources", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
    Column("type", String),  # postgres, mongo...
    Column("config", JSON)
)

metadata.create_all(engine)
