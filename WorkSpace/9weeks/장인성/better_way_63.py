# 응답성을 최대로 높이려면 asyncio 이벤트 루프를 블록하지 말라

from threading import Thread
import asyncio

# 시스템 콜을 코륀으로 만들면 응답성이 좋아진다.

# 실제 I/O를 수행하는 real_write 메서드를 스레드 안전하게 감싸준다
# 다른 스레드에서 실행되는 코루틴은 이 클래스의 write 메서드를 직접 실행하면서 await할 수 있다.
# Lock을 사용할 필요가 없어진다.
class WriteThread(Thread):
    def __init__(self, output_path):
        super().__init__()
        self.output_path = output_path
        self.output = None
        self.loop = asyncio.new_event_loop()

    
    def run(self):
        asyncio.set_event_loop(self.loop)
        with open(self.output_path, 'wb') as self.output:
            self.loop.run_forever()

    
    async def real_write(self, data):
        self.output.write(data)

    async def write(self, data):
        coro = self.real_write(data)
        future = asyncio.run_coroutine_threadsafe(
            coro, self.loop
        )
        await asyncio.wrap_future(future)

    async def real_stop(self):
        self.loop.stop()

    async def stop(self):
        coro = self.real_stop()
        future = asyncio.run_coroutine_threadsafe(
            coro, self.loop
        )
        await asyncio.wrap_future(future)


# 이 클래스를 with 문과 함께 사용할 수 있게 __aenter__ 와 __aexit__ 메서드를 정의한다.
    async def __aenter__(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.start)
        return self

    async def __aexit__(self, *_):
        await self.stop()