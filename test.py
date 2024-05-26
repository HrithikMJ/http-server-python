import asyncio, aiohttp, concurrent.futures
from datetime import datetime
import uvloop


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
            response = await session.get('http://127.0.0.1:8000/2', timeout=self.timeout)
            response.close()
        await session.close()
        return True

    async def testRun(self, id):
        now = datetime.now()
        try:
            if await self.getCheck():
                elapsed = (datetime.now() - now).total_seconds()
                print(f'{self.timestamp()} Request {id} TTC: {elapsed}')
                self.totalTime += elapsed
                self.totalRequests += 1
        except concurrent.futures._base.TimeoutError:
            self.count =  self.count + 1
            print(f'{self.timestamp()} Request {id} timed out')

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
        print(f'{self.timestamp()} Average TTC per Request: {self.totalTime / self.totalRequests}')
        print()
        print(f'{self.count} requests timed out')
        # if len(asyncio.Task.all_tasks()) > 0:
        #     for task in asyncio.Task.all_tasks(): task.cancel()
        #     try: loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
        #     except asyncio.CancelledError: pass
        # loop.close()


test = UVloopTester()
test.start()