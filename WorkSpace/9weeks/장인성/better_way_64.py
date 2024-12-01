# 진정한 병렬성을 살리려면 concurrent.futures를 사용하라

# GIL 때문에 느리다
# C로 전체를 포팅하기는 힘들다
# concurrent.futures의 multiprocessing을 사용하자

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i
    assert False, "도달할 수 없음"


NUMBERS = [
    (1963309, 2265973), (2030677, 3814172),
    (1551656, 2229620), (2039045, 2020802),
    (1823712, 1924928), (2293129, 1020491),
    (1281238, 2273782), (3823812, 4237281),
    (3812741, 4729139), (1292391, 2123811)
]

def main():
    start = time.time()
    results = list(map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f"총 {delta:.3f} 초 걸림")

    start = time.time()
    pool = ThreadPoolExecutor(max_workers=2)
    results = list(pool.map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f"총 {delta:.3f} 초 걸림")


    start = time.time()
    pool = ProcessPoolExecutor(max_workers=2)
    results = list(pool.map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f"총 {delta:.3f} 초 걸림")


if __name__ == '__main__':
    main()


# 1. (부모) 이 객체(ProcessPoolExecutor 인스턴스)는 입력 데이터로 들어온 map 메서드에 전달된 NUMBERS의 각 원소를 취한다.
# 2. (부모) 이 객체는 1번에서 얻은 원소를 pickle 모듈을 사용해 이진 데이터로 직렬화한다.
# 3. (부모, 자식) 이 객체는 로컬 소켓을 통해 주 인터프리터 프로세스로부터 자식 인터프리터 프로세스에게 2번에서 직렬화한 데이터를 복사한다.
# 4. (자식) 이 객체는 pickle을 사용해 데이터를 파이썬 객체로 역직렬화한다.
# 5. (자식) 이 객체는 gcd 함수가 들어 있는 모듈을 임포트한다.
# 6. (자식) 이 객체는 입력 데이터에 대해 gcd 함수를 실행하낟. 이떄 다른 자식 인터프리터 프로세스와 병렬로 실행한다.
# 7. (자식) 이 객체는 gcd 함수의 결과를 이진 데이터로 직렬화한다.
# 8. (부모, 자식) 이 객체는 로컬 소켓을 통해 자식 인터프리터 프로세스로부터 부모 인터프리터 프로세스에게 7번에서 직렬화한 결과 데이터를 돌려준다.
# 9. (부모) 이 객체는 데이터를 파이썬 객체로 역직렬화한다.
# 10. (부모) 여러 자식 프로세스가 돌려준 결과를 병합해서 한 list로 만든다. 