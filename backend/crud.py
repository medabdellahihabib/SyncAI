from sqlalchemy import select, insert
from db import engine
from models import Source





















def list_sources():
    with engine.connect() as conn:
        res = conn.execute(select(Source))
        return [dict(row) for row in res.mappings()]


def add_source(name, typ, config):
    with engine.connect() as conn:
        stmt = insert(Source).values(name=name, type=typ, config=config)
        conn.execute(stmt)
