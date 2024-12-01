import select
import socket
import time
from threading import Thread

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)

start = time.time()

threads = []
for _ in range(5):
    # 시스템 콜 함수를 여러 스레드에서 따로따로 호출 -> 직렬 포트(헬리콥터)와 통신하면서 주 스레드는 필요한 계산을 수행할 수 있다.
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)

def compute_helicopter_location(index):
    pass

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')

# GIL은 파이썬 프로그램이 병렬로 실행되지 못 하게 막지만, 시스템 콜에는 영향 끼치지 못 한다.
# 파이썬 스레드가 시스템 콜을 하기 전에 GIL을 해제하고 시스템 콜에서 반환되자마자 GIL을 다시 획득하기 때문.