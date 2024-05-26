from typing import Union
import asyncio
import concurrent.futures
from fastapi import FastAPI
import time
from starlette.concurrency import run_in_threadpool
app = FastAPI()
import anyio
from contextlib import asynccontextmanager
from anyio.lowlevel import RunVar
from anyio import CapacityLimiter

@asynccontextmanager
async def startup(app: FastAPI):
    print("start")
    RunVar("_default_thread_limiter").set(CapacityLimiter(80))
    yield
    print("exiting")
    
app = FastAPI(lifespan=startup)
@app.get("/1")
async def read_root():
    print("Hello")
    await asyncio.sleep(1)
    print("ball")
    return {"Hello": "World"}

@app.get("/2")
def read_root():
    print("Hello")
    time.sleep(2)
    print("World")
    return {"Hello": "World"}

@app.get("/3")
async def read_root():
    print("Hello")
    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     future = executor.submit(blocking)
    await run_in_threadpool(blocking)
    return {"Hello": "World"}

def blocking():
    time.sleep(2)
    print("World")
    

