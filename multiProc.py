import time
from multiprocessing import Pool, Manager
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


class UVloopTester():
    def __init__(self):
        self.timeout = 10
        self.threads = 500
        self.totalTime = 0
        self.totalRequests = 0
        self.count = 0

    @staticmethod
    def timestamp():
        return f'[{datetime.now().strftime("%H:%M:%S")}]'

    async def getCheck(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/2', timeout=self.timeout) as response:
                await response.read()
            return True

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
        print(f'{self.count} requests timed out')
        print(f'{self.totalRequests} requests done')
        # if len(asyncio.Task.all_tasks()) > 0:
        #     for task in asyncio.Task.all_tasks(): task.cancel()
        #     try: loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
        #     except asyncio.CancelledError: pass
        # loop.close()


def run_uvloop_tester(i):
    print(f"Started {i}")
    tester = UVloopTester()
    tester.start()

if __name__ == "__main__":
    with Pool(10) as pool:
        pool.map(run_uvloop_tester, range(1))
