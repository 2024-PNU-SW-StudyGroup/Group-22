from queue import Queue
from threading import Thread
import time

def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item

class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return   # 스레드를 종료시킨다
                yield item
            finally:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())
# 작업을 모두 넣고 난 후에 close() 함수로 큐의 마지막에 SENTINEL을 넣어준다. -> 큐에서 SENTINEL에 다다르면 스레드 종료
download_queue.close()

download_queue.join() # 작업 완료를 기다린다. 완료되면(= 다음 큐에 모든 작업이 들어갔다면) 동일하게 SENTINEL을 넣는다.
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), '개의 원소가 처리됨')

for thread in threads:
    thread.join()

# join()?? 사용하는 기준??