from typing import Union
import asyncio
import concurrent.futures
from fastapi import FastAPI
import time
import uvicorn
from starlette.concurrency import run_in_threadpool
app = FastAPI()
import anyio
from contextlib import asynccontextmanager
from anyio.lowlevel import RunVar
from anyio import CapacityLimiter
import os
count = 0

import asyncio

def sighandler():
    print(os.getpid())
@asynccontextmanager
async def startup(app: FastAPI):
    global count
    try:
        print(f"started with {os.getpid()}")
        RunVar("_default_thread_limiter").set(CapacityLimiter(2000))
        yield
        print(f"exiting with {count} requests handled")
    except KeyboardInterrupt as e:pass
    

try:
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(sig=2,callback=sighandler)
    app = FastAPI(lifespan=startup)
except KeyboardInterrupt as e:
    pass

@app.get("/1")
async def read_root():
    global count
    print("Hello")
    await asyncio.sleep(2)
    print("ball")
    count = count +1
    return {"Hello": "World"}

@app.get("/2")
def read_root():
    global count
    print("Hello")
    time.sleep(2)
    print("World")
    count = count +1
    return {"Hello": "World"}

@app.get("/3")
async def read_root():
    global count
    print("Hello")
    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     future = executor.submit(blocking)
    await run_in_threadpool(blocking)
    count = count +1
    return {"Hello": "World"}

def blocking():
    time.sleep(2)
    print("World")
    

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=False,
#                 workers=2)