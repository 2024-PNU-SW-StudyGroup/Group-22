# 제너레이터 안에서 throw로 상태를 변화시키지 말라

# 어떤 제너레이터에 대해 throw가 호출되면 이 제너레이터는 throw가 제공한 Exception을 다시 던진다


class MyError(Exception):
    pass


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
print(next(it))
print(next(it))
print(it.throw(MyError('test error')))


# 읽기 어려우니 이터러블 컨테이너 객체를 사용하자