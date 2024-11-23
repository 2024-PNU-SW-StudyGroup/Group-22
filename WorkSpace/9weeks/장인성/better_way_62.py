# asyncio로 쉽게 옮겨갈 수 있도록 스레드와 코루틴을 함께 사용하라

import time
from threading import Lock, Thread
import asyncio

class NoNewData(Exception):
    pass

def readline(handle):
    offset = handle.tell()
    handle.seek(0, 2)
    length = handle.tell()

    if length == offset:
        raise NoNewData
    
    handle.seek(offset, 0)
    return handle.readline()


def tail_file(handle, interval, write_func):
    while not handle.closed:
        try:
            line = readline(handle)
        except NoNewData:
            time.sleep(interval)
        else:
            write_func(line)


# def run_threads(handles, interval, output_path):
async def run_tasks_mixed(handles, interval, output_path):
    loop = asyncio.get_event_loop()

    with open(output_path, 'wb') as output:
        async def write_async(data):
            output.write(data)
        
        def write(data):
            coro = write_async(data)
            future = asyncio.run_coroutine_threadsafe(
                coro, loop
            )
            future.result()

        tasks = []
        for handle in handles:
            task = loop.run_in_executor(
                None, tail_file, handle, interval, write)
            tasks.append(task)

        await asyncio.gather(*tasks)
        # lock = Lock()
        # def write(data):
        #     with lock:
        #         output.write(data)
        #     threads = []
        #     for handle in handles:
        #         args = (handle, interval, write)
        #         thread = Thread(target=tail_file, args=args)
        #         thread.start()
        #         threads.append(thread)

        #     for thread in threads:
        #         thread.join()

# 하향식 접근
# 1. 최상위 함수가 def 대신 async def를 사용하게 변경하라.
# 2. 최상위 함수가 I/O를 호출하는 모든 부분을 asyncio.run_in_executor로 감싸라.
# 3. run_in_executor 호출이 사용하는 자원이나 콜백이 제대로 동기화됐는지 확인하라.
# 4. 호출 계층의 잎 쪽으로 내려가면서 중간에 있는 함수와 메서드를 코루틴으로 변환하며 get_event_loop와 run_in_executor 호출을 없애려고 시도하라.


# 상향식 접근
# 1. 프로그램에서 잎 부분에 있는, 포팅하려는 함수의 비동기 코루틴 버전을 새로 만들어라.
# 2. 기존 동기 함수를 변경해서 코루틴 버전을 호출하고 실제 동작을 구현하는 대신 이벤트 루프를 실행하게 하라.
# 3. 호출 계층을 한 단계 올려서 다른 코루틴 계층을 만들고, 기존에 동기적 함수를 호출하던 부분을 1단계에서 정의한 코루틴 호출로 바꿔라.
# 4.  이제 비동기 부분을 결합하기 위해 2단계에서 만든 동기적인 래퍼가 더 이상 필요하지 않다. 이를 삭제하라.