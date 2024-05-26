import time
from multiprocessing import Pool
import multiprocessing
import requests
import asyncio, aiohttp, concurrent.futures
from datetime import datetime
import uvloop

# def test_function(index_iterator: int):
#     start_time = time.time()
#     response = requests.get("http://127.0.0.1:8000/3")
#     print(f"response.content: {str(response.content)}")
#     if response.status_code != 200:
#         print("----------------------NOT 200")
#         print(f"response.content: {str(response.content)}")
#     end_time = time.time()
#     elapsed_time = end_time - start_time

mpQ = multiprocessing.Queue()
class UVloopTester():
    def __init__(self,i):
        self.timeout = 10
        self.threads = 1200
        self.totalTime = 0
        self.totalRequests = 0
        self.count = 0
        self.i = i

    @staticmethod
    def timestamp():
        return f'[{datetime.now().strftime("%H:%M:%S")}]'

    async def getCheck(self):
        async with aiohttp.ClientSession() as session:
            match self.i:
                case 1:
                    url = 'http://127.0.0.1:8000/1'
                case 2:
                    url = 'http://127.0.0.1:8000/2'
                case 3:
                    url = 'http://127.0.0.1:8000/3'
                    
            try :
                async with session.get(url, timeout=self.timeout) as response:
                    await response.read()
            except Exception as e:
                raise concurrent.futures._base.TimeoutError()
            return True

    async def multiProcQConsumer(self):
        if mpQ.qsize > 0:
            print(mpQ.get())

    async def testRun(self, id):
        now = datetime.now()
        try:
            if await self.getCheck():
                elapsed = (datetime.now() - now).total_seconds()
                # print(f'{self.timestamp()} Request {id} TTC: {elapsed}')
                self.totalTime += elapsed
                self.totalRequests += 1
        except concurrent.futures._base.TimeoutError:
            self.count =  self.count + 1
            # print(f'{self.timestamp()} Request {id} timed out')

    async def main(self):
        # await asyncio.run_coroutine_threadsafe(self.multiProcQConsumer)
        # async with asyncio.TaskGroup() as tg:
        #     for x in range(self.threads):
        #         await tg.create_task(self.testRun)  
        #     # await tg.create_task(*[asyncio.ensure_future(self.testRun(x)) for x in range(self.threads)])
        #     await tg.create_task(self.multiProcQConsumer())
        await asyncio.gather(*[asyncio.ensure_future(self.testRun(x)) for x in range(self.threads)])

    def start(self):
        # comment these lines to toggle
        # uvloop.install()
        # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(self.main())

        now = datetime.now()
        elapsed = (datetime.now() - now).total_seconds()
        print(f'{self.timestamp()} Main TTC: {elapsed}')
        print()
        # print(f'{self.timestamp()} Average TTC per Request: {self.totalTime / self.totalRequests}')
        print()
        print(f'{self.count} requests timed out in {self.i}')
        print(f'{self.totalRequests} requests done {self.i}')
        # if len(asyncio.Task.all_tasks()) > 0:
        #     for task in asyncio.Task.all_tasks(): task.cancel()
        #     try: loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
        #     except asyncio.CancelledError: pass
        # loop.close()


def run_uvloop_tester(i):
    print(f"Started {i}")
    if i == 2:
        print(f"put msg to queue in {i} func")
        mpQ.put_nowait("Hello")
    elif i ==1:
        if mpQ.qsize() > 0:
            print(f"Got msg from queue {i} func {mpQ.get()}")
    elif i == 3:
        if mpQ.qsize() > 0:
            print(f"Got msg from queue {i} func {mpQ.get()}")
    tester = UVloopTester(i)
    tester.start()

if __name__ == "__main__":
    with Pool(3) as pool:
        pool.map(run_uvloop_tester, range(1,4))

