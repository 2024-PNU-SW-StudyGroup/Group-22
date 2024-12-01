# yield from을 사용해 여러 제너레이터를 합성하라

import timeit

def move(period, speed):
    for _ in range(period):
        yield speed


def pause(delay):
    for _ in range(delay):
        yield 0


def render(delta):
    print(f"Delta: {delta}")


def run(func):
    for delta in func():
        render(delta)


# animate가 너무 반복적이다.
def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta


# 코드가 더 직관적이다
# yield from이 for 루프를 내포하는데, 직접 명시하는 것보다 성능이 좋다.
def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)


run(animate)
run(animate_composed)


def child():
    for i in range(1_000_000):
        yield i


def slow():
    for i in child():
        yield i


def fast():
    yield from child()


baseline = timeit.timeit(
    stmt="for _ in slow(): pass",
    globals=globals(),
    number=50
)
print(f"수동 내포: {baseline:.2f}s")


comparison = timeit.timeit(
    stmt="for _ in fast(): pass",
    globals=globals(),
    number=50
)
print(f"합성 사용: {comparison:.2f}s")

reduction = -(comparison - baseline) / baseline
print(f"{reduction:.1%} 시간이 적게 듦")