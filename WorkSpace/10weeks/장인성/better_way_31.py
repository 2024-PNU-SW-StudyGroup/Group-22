# 인자에 대해 이터레이션할 때는 방어적이 돼라

from collections.abc import Iterator

def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages) # [11.538461538461538, 26.923076923076923, 61.53846153846154]


# 이터레이터가 결과를 단 한 번만 만들어내기 때문에 다시 이터레이션하면 아무 결과도 얻을 수 없다.
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

path = 'my_numbers.txt'
it = read_visits(path)
percentages = normalize(it)
print(percentages) # []


# 이터레이터 프로토콜을 구현한 새로운 컨테이너 클래스를 제공하자
# 이 코드가 잘 작동하는 이유는 normalize 함수 안의 sum 메서드가 ReadVisits.__iter__를 호출해서 새로운 이터레이터 객체를 할당하기 때문이다.
# 각 숫자를 정규화하기 위한 for 루프도 __iter__를 호출해서 두 번째 이터레이터 객체를 만든다.
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages) # [11.538461538461538, 26.923076923076923, 61.53846153846154]


# 이터레이터가 iter 내장 함수에 전달되는 경우에는 전달받은 이터레이터가 그대로 반환된다.
# 반대로 컨테이너 타입이 iter에 전달되면 매번 새로운 이터레이터 객체가 반환된다.
def normalize_defensive(numbers):
    if iter(numbers) is numbers:
        raise TypeError('컨테이너를 제공해야 합니다')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


# collections.abc 내장 모듈은 isinstance를 사용해 잠재적인 문제를 검사할 수 있는 Iterator 클래스를 제공한다.
def normalize_defensive_isinstance(numbers):
    if isinstance(numbers, Iterator):
        raise TypeError('컨테이너를 제공해야 합니다')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# 리스트: 이터레이터 프로토콜을 따르는 이터러블 컨테이너
visits = [15, 35, 80]
percentages = normalize_defensive_isinstance(visits)
print(percentages)

# ReadVisits: 이터레이터 프로토콜을 따르는 이터러블 컨테이너
visits = ReadVisits(path)
percentages = normalize_defensive_isinstance(visits)
print(percentages)

# 컨테이너가 아닌 이터레이터면 예외를 발생시킨다.
visits = [15, 35, 80]
it = iter(visits)
percentages = normalize_defensive_isinstance(it)
print(percentages)

