from threading import Thread
import select
import socket
import time

# GIL 스레드 병렬 실행 X
# 그렇다고해서 데이터 구조 동시 접근 막아주는 것은 아니다 -> 동시 접근 시에 데이터 값 이상해질 수 있다.

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset

def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        # 센서를 읽는다
        counter.increment(1)

from threading import Thread

how_many = 10**5
counter = Counter()

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
# 실제 값은 더 작아지는 경우 존재 ex) 481384
print(f'카운터 값은 {expected}여야 하는데, 실제로는 {found} 입니다')

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')


"""
파이썬 인터프리터는 각 스레드의 실행시간을 거의 비슷하게 만든다.
-> 실행 중인 스레드를 일시 중단시키고 다른 스레드를 실행시키는 일 반복 but 스레드를 언제 중단시킬지는 모름,,


counter.increment(1): += 연산 3가지로 나뉨

value = getattr(counter, 'count')
result = value + 1
setattr(counter, 'count', result)

세 연산 사이에서 중단될 수 있음 -> 이전 값을 카운터에 대입하는 등의 일이 생길 수 있으므로 값이 부정확해진다.
"""
