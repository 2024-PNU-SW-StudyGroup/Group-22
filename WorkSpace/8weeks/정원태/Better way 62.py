
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


# 예제 2
import time

def tail_file(handle, interval, write_func):
    while not handle.closed:
        try:
            line = readline(handle)
        except NoNewData:
            time.sleep(interval)
        else:
            write_func(line)


# 예제 3
from threading import Lock, Thread

def run_threads(handles, interval, output_path):
    with open(output_path, 'wb') as output:
        lock = Lock()
        def write(data):
            with lock:
                output.write(data)

        threads = []
        for handle in handles:
            args = (handle, interval, write)
            thread = Thread(target=tail_file, args=args)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


# 예제 4
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
            # 읽기 스레드가 파일을 폴링하기 전에 경로상 파일이 존재하는지 확실히 하자
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


# 예제 5
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
        assert expected_lines == found_lines, \
            f'{expected_lines!r} == {found_lines!r}'

input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

run_threads(handles, 0.1, output_path)

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


# 예제 6
import asyncio

# 윈도우에서는 ProactorEventLoop가 시그널 핸들러를 등록하려고 시도하기 때문에
# 스레드 안에서 ProactorEventLoop를 만들 수 없다.
#
# 대신 SelectEventLoop 정책을 사용하는 방식으로 우회한다.
# 참고: https://bugs.python.org/issue33792
policy = asyncio.get_event_loop_policy()
policy._loop_factory = asyncio.SelectorEventLoop

async def run_tasks_mixed(handles, interval, output_path):
    loop = asyncio.get_event_loop()

    with open(output_path, 'wb') as output:
        async def write_async(data):
            output.write(data)

        def write(data):
            coro = write_async(data)
            future = asyncio.run_coroutine_threadsafe(
                coro, loop)
            future.result()

        tasks = []
        for handle in handles:
            task = loop.run_in_executor(
                None, tail_file, handle, interval, write)
            tasks.append(task)

        await asyncio.gather(*tasks)


# 예제 7
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

asyncio.run(run_tasks_mixed(handles, 0.1, output_path))

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


# 예제 8
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


# 예제 9
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


# 예제 10
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

asyncio.run(run_tasks(handles, 0.1, output_path))

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


# 예제 11
def tail_file(handle, interval, write_func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def write_async(data):
        write_func(data)

    # 맨 마지막에 한번 더 이벤트 루프를 실행해서
    # 다른 이벤트 루프가 stop()에 await하는 경우를 해결한다.
    coro = tail_async(handle, interval, write_async)
    loop.run_until_complete(coro)


# 예제 12
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

run_threads(handles, 0.1, output_path)

confirm_merge(input_paths, output_path)

tmpdir.cleanup()
