from sqlalchemy import select, insert
from .db import engine
from .models import sources

def list_sources():
    with engine.connect() as conn:
        res = conn.execute(select([sources]))
        return [dict(row) for row in res]

def add_source(name, typ, config):
    with engine.connect() as conn:
        stmt = insert(sources).values(name=name, type=typ, config=config)
        conn.execute(stmt)
