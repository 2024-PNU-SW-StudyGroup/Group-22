import threading
import time
import select
import socket


def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)


def compute_helicopter_location(index):
    pass


start = time.time()
threads = []

for _ in range(5):
    thread = threading.Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)


for i in range(5):
    compute_helicopter_location(i)


for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f"총 {delta:.3f} 초 걸림")

"""
느린 시스템 콜을 스레드로 옮기자
CPython은 GIL로 인해 CPU 연산이 많을 때 멀티쓰레드의 효과를 볼 수 없음
그러나 I/O 연산에서는 멀티쓰레드의 효과를 볼 수 있다
"""