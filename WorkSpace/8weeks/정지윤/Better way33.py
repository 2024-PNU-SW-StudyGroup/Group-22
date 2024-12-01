
#
# 아이템 33
#
def move(period, speed):
    for _ in range(period):
        yield speed

#
def pause(delay):
    for _ in range(delay):
        yield 0

#
def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta

#
def render(delta):
    print(f'Delta: {delta:.1f}')
    # 화면에서 이미지를 이동시킨다

def run(func):
    for delta in func():
        render(delta)

run(animate)

# 파이썬 인터프리터가 for loop를 내포시키고 yield 식을 처리하도록 만든다
def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)


run(animate_composed)

#

import timeit

def child():
    for i in range(1_000_000):
        yield i

def slow():
    for i in child():
        yield i

def fast():
    yield from child()

baseline = timeit.timeit(
    stmt='for _ in slow(): pass',
    globals=globals(),
    number=50)
print(f'수동 내포: {baseline:.2f}s')

comparison = timeit.timeit(
    stmt='for _ in fast(): pass',
    globals=globals(),
    number=50)
print(f'합성 사용: {comparison:.2f}s')

reduction = -(comparison - baseline) / baseline
print(f'{reduction:.1%} 시간이 적게 듦')

"""
제너레이터를 합성한다면 yield from을 사용하라 -> 여러 내장 제너레이터를 모아서 제너레이터 하나로 합성 가능
"""