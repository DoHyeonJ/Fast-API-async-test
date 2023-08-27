from fastapi import FastAPI
import time
import asyncio


app = FastAPI()

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