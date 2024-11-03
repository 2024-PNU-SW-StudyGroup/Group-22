from queue import Queue
from threading import Thread
import time

# 두 단계 사이에 허용할 수 있는 미완성 작업의 최대 개수 지정 가능
# 버퍼 크기를 정함 -> 큐가 이미 가득 참 -> put() 블록
my_queue = Queue(1)  # 버퍼 크기 1

def consumer():
    time.sleep(0.1)  # 대기
    my_queue.get()  # 두 번째로 실행됨
    print('소비자 1')
    my_queue.get()  # 네 번째로 실행됨
    print('소비자 2')
    print('소비자 완료')

thread = Thread(target=consumer)
thread.start()

my_queue.put(object()) # 첫 번째로 실행됨
print('생산자 1')
my_queue.put(object()) # 세 번째로 실행됨: 미완성 작업 최대 개수가 1이므로(Queue의 크기가 1이므로) 이전 작업이 완성돼야 put() 실행 가능함
print('생산자 2')
print('생산자 완료')
thread.join()
