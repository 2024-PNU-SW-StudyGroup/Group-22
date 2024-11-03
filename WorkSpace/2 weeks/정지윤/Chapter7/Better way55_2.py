from queue import Queue
from threading import Thread

my_queue = Queue()

# 큐에 입력 데이터가 들어오기를 기다리는 스레드
# 새로운 데이터가 put()으로 나타나기 전까지 get 메서드가 블록되게 만들어 작업자의 바쁜 대기 문제를 해결한다. -> Queue 고유 특성
def consumer():
    print('소비자 대기')
    my_queue.get()  # 다음에 보여줄 put()이 실행된 다음에 시행된다
    print('소비자 완료')

thread = Thread(target=consumer)
thread.start()

print('생산자 데이터 추가')
my_queue.put(object())     # 앞에서 본 get()이 실행되기 전에 실행된다.
print('생산자 완료')
thread.join()

