# 1) 디지털 카메라에서 이미지 스트림을 가져오고
# 2) 이미지 크기를 변경하고
# 3) 온라인 포토 갤러리에 저장한다

def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item

from collections import deque
from threading import Lock

class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()

from threading import Thread
import time

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            # 입력 큐가 비어있는 경우 -> 이전 단계가 아직 작업을 완료하지 않음
            # 조립 라인을 일시 중단시키는 것
            except IndexError:
                # 이전 단계가 끝날 때까지 기다린다
                time.sleep(0.01) # 할 일이 없음
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1

download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()

done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

while len(done_queue.items) < 1000:
    # 기다리는 동안 유용한 작업을 수행한다
    pass

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print(f'{processed} 개의 아이템을 처리했습니다, '
      f'이때 폴링을 {polled} 번 했습니다.')
# 작업자 함수의 속도가 달라지면(앞 단계의 작업이 오래 걸리면) 뒤에 있는 단계는 루프를 돌며 새로운 작업이 들어왔는지 자신의 입력 큐를 계속 검사(polling)
# -> 작업자 스레드가 유용하지 않은 일(IndexError 잡아냄)을 하느라 CPU 시간 잡아먹는다.


# 작업이 끝나도 무한대기함. 프로그램을 강제종료시킬것