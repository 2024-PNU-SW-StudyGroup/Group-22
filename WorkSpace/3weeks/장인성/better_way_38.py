# 간단한 인터페이스의 경우 클래스 대신 함수를 받아라
from collections import defaultdict

names = ['소크라테스', '아르키메데스', '플라톤', '아리스토텔레스']
# API가 실행되는 과정에서 전달한 함수를 실행하는 경우, 이런 함수를 훅(hook)이라고 부른다.
# 파이썬 함수는 일급 시민 객체로, 함수나 메서드를 다른 함수에 넘기거나 변수 등으로 참조할 수 있다.
names.sort(key=len)
print(names)


# 호출 가능 객체
class BetterCountMissing:
    def __init__(self):
        self.added = 0


    # __call__을 사용하면 객체를 함수처럼 호출할 수 있다.
    def __call__(self):
        self.added += 1
        return 0
    

current = {'초록': 12, '파랑': 3}
increments = [('빨강', 5), ('파랑', 17), ('주황', 9)]

counter = BetterCountMissing()
result = defaultdict(counter, current)
for key, amount in increments:
    result[key] += amount
assert counter.added == 2