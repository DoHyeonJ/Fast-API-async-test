from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists
import databases
import time
import asyncio

app = FastAPI()

DATABASE_URL = "postgresql://jodohyeon:pass@localhost/fastapi"
database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)

@app.on_event("startup")
async def startup():
    await database.connect()
    if not database_exists(engine.url):
        create_database(engine.url)
    async with database.transaction():
        Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# 외부 API라고 가정함
def open_api(data):
    time.sleep(10)
    return {"name": data}

@app.post("/create_item/")
async def create_item(item_name: str):
    value = open_api(item_name)
    query = Item.__table__.insert().values(value)
    last_record_id = await database.execute(query)
    return {"item_name": item_name, "record_id": last_record_id}

@app.get("/")
async def read_root():
    user = await get_user()
    print(user)
    return {"message": "Hello, FastAPI"}

@app.get("/test")
def test():
    user = asyncio.run(get_user())

async def get_user():
    return {"user_id": "test", "password": "pass"}