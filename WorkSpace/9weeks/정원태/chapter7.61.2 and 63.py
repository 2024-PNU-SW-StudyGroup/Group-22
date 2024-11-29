
# Copyright 2014-2019 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 원서 코드 github(https://github.com/bslatkin/effectivepython)에서 가져온 코드임
# 원서의 코드 실행 환경 만들기
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# 모든 출력을 임시 디렉터리에 기록함
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# 윈도우에서 프로세스 깔끔하게 종료하기
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# 예제 1
import asyncio

# 윈도우에서는 ProactorEventLoop가 시그널 핸들러를 등록하려고 시도하기 때문에
# 스레드 안에서 ProactorEventLoop를 만들 수 없다.
#
# 대신 SelectEventLoop 정책을 사용하는 방식으로 우회한다.
# 참고: https://bugs.python.org/issue33792
policy = asyncio.get_event_loop_policy()
policy._loop_factory = asyncio.SelectorEventLoop

async def run_tasks(handles, interval, output_path):
    with open(output_path, 'wb') as output:
        async def write_async(data):
            output.write(data)

        tasks = []
        for handle in handles:
            coro = tail_async(handle, interval, write_async)
            task = asyncio.create_task(coro)
            tasks.append(task)

        await asyncio.gather(*tasks)


# 예제 2
import time

async def slow_coroutine():
    time.sleep(0.5)  # 느린 I/O를 시뮬레이션

asyncio.run(slow_coroutine(), debug=True)


# 예제 3
from threading import Thread

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

        # 맨 마지막에 한번 더 이벤트 루프를 실행해서
        # 다른 이벤트 루프가 stop()에 await하는 경우를 해결한다.
        self.loop.run_until_complete(asyncio.sleep(0))


# 예제 4
    async def real_write(self, data):
        self.output.write(data)

    async def write(self, data):
        coro = self.real_write(data)
        future = asyncio.run_coroutine_threadsafe(
            coro, self.loop)
        await asyncio.wrap_future(future)


# 예제 5
    async def real_stop(self):
        self.loop.stop()

    async def stop(self):
        coro = self.real_stop()
        future = asyncio.run_coroutine_threadsafe(
            coro, self.loop)
        await asyncio.wrap_future(future)


# 예제 6
    async def __aenter__(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.start)
        return self

    async def __aexit__(self, *_):
        await self.stop()


# 예제 7
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

async def tail_async(handle, interval, write_func):
    loop = asyncio.get_event_loop()

    while not handle.closed:
        try:
            line = await loop.run_in_executor(
                None, readline, handle)
        except NoNewData:
            await asyncio.sleep(interval)
        else:
            await write_func(line)

async def run_fully_async(handles, interval, output_path):
    async with WriteThread(output_path) as output:
        tasks = []
        for handle in handles:
            coro = tail_async(handle, interval, output.write)
            task = asyncio.create_task(coro)
            tasks.append(task)

        await asyncio.gather(*tasks)


# 예제 8
# 핸들에 쓰는 프로세스를 에뮬레이션하는 코드
import collections
import os
import random
import string
from tempfile import TemporaryDirectory

def write_random_data(path, write_count, interval):
    with open(path, 'wb') as f:
        for i in range(write_count):
            time.sleep(random.random() * interval)
            letters = random.choices(
                string.ascii_lowercase, k=10)
            data = f'{path}-{i:02}-{"".join(letters)}\n'
            f.write(data.encode())
            f.flush()

def start_write_threads(directory, file_count):
    paths = []
    for i in range(file_count):
        path = os.path.join(directory, str(i))
        with open(path, 'w'):
            # Make sure the file at this path will exist when
            # the reading thread tries to poll it.
            pass
        paths.append(path)
        args = (path, 10, 0.1)
        thread = Thread(target=write_random_data, args=args)
        thread.start()
    return paths

def close_all(handles):
    time.sleep(1)
    for handle in handles:
        handle.close()

def setup():
    tmpdir = TemporaryDirectory()
    input_paths = start_write_threads(tmpdir.name, 5)

    handles = []
    for path in input_paths:
        handle = open(path, 'rb')
        handles.append(handle)

    Thread(target=close_all, args=(handles,)).start()

    output_path = os.path.join(tmpdir.name, 'merged')
    return tmpdir, input_paths, handles, output_path


# 예제 9
def confirm_merge(input_paths, output_path):
    found = collections.defaultdict(list)
    with open(output_path, 'rb') as f:
        for line in f:
            for path in input_paths:
                if line.find(path.encode()) == 0:
                    found[path].append(line)

    expected = collections.defaultdict(list)
    for path in input_paths:
        with open(path, 'rb') as f:
            expected[path].extend(f.readlines())

    for key, expected_lines in expected.items():
        found_lines = found[key]
        assert expected_lines == found_lines

input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

asyncio.run(run_fully_async(handles, 0.1, output_path))

confirm_merge(input_paths, output_path)

tmpdir.cleanup()

---------------------
# python 3.8 이상에서만 실행됨(walus연산자때문)

class EOFError(Exception):
    pass


class AsyncConnectionBase:
    def __init__(self, reader, writer):  # 변경됨
        self.reader = reader  # 변경됨
        self.writer = writer  # 변경됨

    async def send(self, command):
        line = command + '\n'
        data = line.encode()
        self.writer.write(data)  # 변경됨
        await self.writer.drain()  # 변경됨

    async def receive(self):
        line = await self.reader.readline()  # 변경됨
        if not line:
            raise EOFError('연결 닫힘')
        return line[:-1].decode()

import random

WARMER = '더따뜻함'
COLDER = '더차가움'
UNSURE = '잘모르겠음'
CORRECT = '맞음'

class UnknownCommandError(Exception):
    pass

class AsyncSession(AsyncConnectionBase):  # 변경됨
    def __init__(self, *args):
        super().__init__(*args)
        self._clear_state(None, None)

    def _clear_state(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.secret = None
        self.guesses = []

    async def loop(self):  # 변경됨
        while command := await self.receive():  # 변경됨
            parts = command.split(' ')
            if parts[0] == 'PARAMS':
                self.set_params(parts)
            elif parts[0] == 'NUMBER':
                await self.send_number()  # 변경됨
            elif parts[0] == 'REPORT':
                self.receive_report(parts)
            else:
                raise UnknownCommandError(command)

    def set_params(self, parts):
        assert len(parts) == 3
        lower = int(parts[1])
        upper = int(parts[2])
        self._clear_state(lower, upper)

    def next_guess(self):
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.guesses:
                return guess

    async def send_number(self):
        guess = self.next_guess()
        self.guesses.append(guess)
        await self.send(format(guess))

    def receive_report(self, parts):
        assert len(parts) == 2
        decision = parts[1]
        last = self.guesses[-1]
        if decision == CORRECT:
            self.secret = last

        print(f'서버: {last}는 {decision}')


import contextlib
import math

class AsyncClient(AsyncConnectionBase):
    def __init__(self, *args):
        super().__init__(*args)
        self._clear_state()

    def _clear_state(self):
        self.secret = None
        self.last_distance = None

    @contextlib.asynccontextmanager                         # 변경됨
    async def session(self, lower, upper, secret):          # 변경됨
        print(f'\n{lower}와 {upper} 사이의 숫자를 맞춰보세요!'
              f' 쉿! 그 숫자는 {secret} 입니다.')
        self.secret = secret
        await self.send(f'PARAMS {lower} {upper}')          # 변경됨
        try:
            yield
        finally:
            self._clear_state()
            await self.send('PARAMS 0 -1')                   # 변경됨

    async def request_numbers(self, count):            # 변경됨
        for _ in range(count):
            await self.send('NUMBER')                  # 변경됨
            data = await self.receive()                # 변경됨
            yield int(data)
            if self.last_distance == 0:
                return

    async def report_outcome(self, number):                    # 변경됨
        new_distance = math.fabs(number - self.secret)
        decision = UNSURE

        if new_distance == 0:
            decision = CORRECT
        elif self.last_distance is None:
            pass
        elif new_distance < self.last_distance:
            decision = WARMER
        elif new_distance > self.last_distance:
            decision = COLDER

        self.last_distance = new_distance

        await self.send(f'REPORT {decision}')                  # 변경됨

        # 잠시 대기해서 출력 순서 조정
        await asyncio.sleep(0.01)
        return decision

import asyncio

async def handle_async_connection(reader, writer):
    session = AsyncSession(reader, writer)
    try:
        await session.loop()
    except EOFError:
        pass

async def run_async_server(address):
    server = await asyncio.start_server(
        handle_async_connection, *address)
    async with server:
        await server.serve_forever()

async def run_async_client(address):
    # 서버가 시작될 수 있게 기다려주기
    await asyncio.sleep(0.1)

    streams = await asyncio.open_connection(*address)   # New
    client = AsyncClient(*streams)                      # New

    async with client.session(1, 5, 3):
        results = [(x, await client.report_outcome(x))
                   async for x in client.request_numbers(5)]

    async with client.session(10, 15, 12):
        async for number in client.request_numbers(5):
            outcome = await client.report_outcome(number)
            results.append((number, outcome))

    _, writer = streams                                # 새 기능
    writer.close()                                     # 새 기능
    await writer.wait_closed()                         # 새 기능

    return results

async def main_async():
    address = ('127.0.0.1', 4321)

    server = run_async_server(address)
    asyncio.create_task(server)

    results = await run_async_client(address)
    for number, outcome in results:
        print(f'클라이언트: {number}는 {outcome}')

asyncio.run(main_async())

