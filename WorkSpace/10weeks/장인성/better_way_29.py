# 대입식을 사용해 컴프리헨션 안에서 반복 작업을 피하라

stock = {
    '못': 125,
    '나사못': 35,
    '나비너트': 8,
    '와셔': 24,
}

order = ['나사못', '나비너트', '클립']


def get_batches(count, size):
    return count // size

result = {}
for name in order:
    count = stock.get(name, 0) # 없으면 0을 반환
    batches = get_batches(count, 8)
    if batches:
        result[name] = batches

print(result)


found = {name: batches for name in order if (batches := get_batches(stock.get(name, 0), 8))}
print(found)


# 대입식을 컴프리헨션의 값 식에 사용해도 문법적으로 올바르다.
# 그러나, 컴프리헨션의 다른 부분에서 이 변수를 읽으려고 하면 컴프리헨션이 평가되는 순서 때문에 실행 시점에 오류가 발생한다.
#result = {name: (tenth := count // 10) for name, count in stock.items() if tenth > 0}
# NameError: name 'tenth' is not defined

# 대입식을 조건 쪽으로 옮겨서 해결한다
result = {name: tenth for name, count in stock.items() if (tenth := count // 10) > 0}

# 컴프리헨션의 값 부분에서 왈러스 연산자를 사용하면 루프 밖 영역으로 루프 변수가 누출된다.
half = [(last := count // 2) for count in stock.values()]
# print(last) 12

# 컴프리헨션의 루프 변수인 경우에는 누출이 생기지 않는다. 누출하지 않는 편이 낫다.
half = [count // 2 for count in stock.values()]
# print(count) NameError: name 'count' is not defined


# 딕셔너리 인스턴스 대신 이터레이터를 만든다
found = ((name, batches) for name in order if (batches := get_batches(stock.get(name, 0), 8)))
print(found)
print(next(found))
print(next(found))
