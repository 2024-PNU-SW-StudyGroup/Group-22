# send로 제너레이터에 데이터를 주입하지 말라

import math


def wave(amplitude, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output


def transmit(output):
    if output is None:
        print(f"출력: None")
    else:
        print(f"출력: {output:>5.1f}")


def run(it):
    for output in it:
        transmit(output)

run(wave(3.0, 8))



# 일반적으로 제너레이터를 이터레이션할 때  yield 식이 반환하는 값는 None이다.
def my_generator():
    received = yield 1
    print(f"받은 값 = {received}")


it = iter(my_generator())
output = next(it)
print(f"출력값 = {output}")

try:
    next(it)
except StopIteration:
    pass
'''
출력값 = 1
받은 값 = None
'''

# send 메서드는 입력을 제너레이터에 스트리밍하는 동시에 출력을 내보낼 수 있다.
# 제너레이터를 이터레이션하지 않고 send 메서드를 호출하면, 제너레이터가 재개될 때 yield가 send에 전달된 파라미터 값을 반환한다.
# 하지만 방금 시작한 제너레이터는 아직 yield 식에 도달하지 못했기 때문에 최초로 send를 호출할 때 인자로 전달할 수 있는 유일한 값은 None뿐이다.
it = iter(my_generator())
output = it.send(None)
print(f"출력값 = {output}")

try:
    it.send('안녕!')
except StopIteration:
    pass
'''
출력값 = 1
받은 값 = 안녕!
'''


def wave_modulating(steps):
    step_size = 2 * math.pi / steps
    amplitude = yield  # 초기 진폭을 받는다
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        amplitude = yield output # 다음 진폭을 받는다


def run_modulating(it):
    amplitudes = [
        None, 7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    for amplitude in amplitudes:
        output = it.send(amplitude)
        transmit(output)


run_modulating(wave_modulating(12))
'''
출력: None
출력:   0.0
출력:   3.5
출력:   6.1
출력:   2.0
출력:   1.7
출력:   1.0
출력:   0.0
출력:  -5.0
출력:  -8.7
출력: -10.0
출력:  -8.7
출력:  -5.0
'''


def complex_wave():
    yield from wave(7.0, 3)
    yield from wave(2.0, 4)
    yield from wave(10.0, 5)

run(complex_wave())
'''
출력:   0.0
출력:   6.1
출력:  -6.1
출력:   0.0
출력:   2.0
출력:   0.0
출력:  -2.0
출력:   0.0
출력:   9.5
출력:   5.9
출력:  -5.9
출력:  -9.5
'''

# 출력에 None이 생긴다
# yield from과 send를 같이 사용하면 문제가 생긴다
def complex_wave_modulating():
    yield from wave_modulating(3)
    yield from wave_modulating(4)
    yield from wave_modulating(5)

run_modulating(complex_wave_modulating())
'''
출력: None
출력:   0.0
출력:   6.1
출력:  -6.1
출력: None
출력:   0.0
출력:   2.0
출력:   0.0
출력: -10.0
출력: None
출력:   0.0
출력:   9.5
출력:   5.9
'''

# 해결책은 wave 함수에 이터레이터를 전달하는 것이다.

def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it)
        output = amplitude * fraction
        yield output


def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)


def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    it = complex_wave_cascading(iter(amplitudes))
    for amplitude in amplitudes:
        output = next(it)
        transmit(output)


run_cascading()

'''
출력:   0.0
출력:   6.1
출력:  -6.1
출력:   0.0
출력:   2.0
출력:   0.0
출력:  -2.0
출력:   0.0
출력:   9.5
출력:   5.9
출력:  -5.9
출력:  -9.5
'''

# 제너레이터가 항상 스레드 안전하지는 않다.
# 스레드 경계를 넘나들면서 제너레이터를 사용해야 한다면 async 함수가 더 나은 해법일 수도 있다.