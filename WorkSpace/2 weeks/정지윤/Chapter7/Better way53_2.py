def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

from threading import Thread

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))

import time

numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()

threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

# 모든 스레드가 끝날 때까지 기다림
for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')

# 다른 언어는 각 수에 스레드를 하나씩 할당하면 할당하는만큼(한도 내) 속도 향상 됨.
# 파이썬은 아님 <- 표준 CPython 인터프리터에서 프로그램을 사용할 때 GIL을 사용하기 떄문에
# 파이썬도 다중 실행 스레드를 지원하지만 GIL로 인해 여러 스레드 중 어느 하나만 앞으로 진행할 수 있다.

"""
GIL이 있음에도 스레드?

- CPython이 균일하게 각 스레드를 실행 -> 다중 스레드를 통해 여러 함수를 동시에 실행할 수 있다.

- 블로킹 I/O
파이썬은 시스템 콜을 사용해 OS가 자기 대신 외부 환경과 상호작용하도록 의뢰
ex) 파일 쓰기/읽기, 네트워크와 상호작용, 디스플레이 장치와 통신
"""