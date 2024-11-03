import select
import socket
import time

def slow_systemcall():
    # select: 운영체제에게 0.1초동안 주 실행 스레드를 블록한 다음에 제어를 돌려달라고 요청
    # 블록 되므로 해당 함수가 실행되는 동안 프로그램이 다른 작업 수행 불가
    # 블로킹 I/0 & 계산 동시 수행 -> 시스템 콜을 스레드로 옮긴다.
    select.select([socket.socket()], [], [], 0.1)

start = time.time()

for _ in range(5):
    # 순차적으로 실행 -> 필요한 시간 선형으로 증가
    slow_systemcall()


end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')
