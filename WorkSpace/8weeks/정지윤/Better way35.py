
#
# 아이템 35
#
class MyError(Exception):
    pass

def my_generator():
    yield 1
    yield 2
    yield 3

it = my_generator()
print(next(it))  # 1을 내놓음
print(next(it))  # 2를 내놓음
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#print(it.throw(MyError('test error')))

#
def my_generator():
    yield 1
    try:
        yield 2
    except MyError:
        print('MyError 발생!')
    else:
        yield 3
    yield 4

it = my_generator()
print(next(it))  # 1을 내놓음
print(next(it))  # 2를 내놓음
print(it.throw(MyError('test error')))

#
class Reset(Exception):
    pass

def timer(period):
    current = period
    while current:
        current -= 1
        try:
            yield current
        except Reset:
            current = period

#
RESETS = [
    False, False, False, True, False, True, False,
    False, False, False, False, False, False, False]

def check_for_reset():
    # 외부 이벤트를 폴링한다
    return RESETS.pop(0)

def announce(remaining):
    print(f'{remaining} 틱 남음')

def run():
    it = timer(4)
    while True:
        try:
            if check_for_reset():
                current = it.throw(Reset())
            else:
                current = next(it)
        except StopIteration:
            break
        else:
            announce(current)

#
class Timer:
    def __init__(self, period):
        self.current = period
        self.period = period

    def reset(self):
        self.current = self.period

    def __iter__(self):
        while self.current:
            self.current -= 1
            yield self.current

#
def run():
    timer = Timer(4)
    for current in timer:
        if check_for_reset():
            timer.reset()
        announce(current)

run()

"""
제너레이터 안에서 throw를 사용해 예외 경우를 관리 가능 but 코드 가독성 떨어짐
예외적인 경우를 처리해야 한다면 throw를 사용하지 않고 이터러블 클래스를 사용하라 -> 이터러블 클래스 내부에 예외 상황일 때 처리해야 할 작업을 정의한다.
일반적인 제너레이터를 사용할 경우 throw를 던져야 실행 도중에 예외를 잡아내고 하던 작업을 이어서 할 수 있다.
"""
