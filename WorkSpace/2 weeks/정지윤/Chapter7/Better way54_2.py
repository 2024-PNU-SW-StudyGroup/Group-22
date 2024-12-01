from threading import Thread
import select
import socket
import time

from threading import Lock

# 다중 스레드로 인한 데이터 경합을 막기 위해 락을 사용한다. -> 한 번에 하나의 스레드만 락을 획득

class LockingCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock: # 락을 획득하고 해제한다.
            self.count += offset

def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        # 센서를 읽는다
        counter.increment(1)

from threading import Thread

how_many = 10**5
counter = LockingCounter()

start = time.time()

threads = []
for i in range(5):
    thread = Thread(target=worker,
                    args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'카운터 값은 {expected}여야 하는데, 실제로는 {found} 입니다')

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')
