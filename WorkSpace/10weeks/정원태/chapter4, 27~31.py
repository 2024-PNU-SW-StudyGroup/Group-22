# 아이템 27
#
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = []
for x in a:
    squares.append(x**2)

print(squares)

#
squares = [x**2 for x in a] # 리스트 컴프리핸션

print(squares)

#
alt = map(lambda x: x ** 2, a)

#
even_squares = [x**2 for x in a if x % 2 == 0]
print(even_squares)

#
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)

#
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
threes_cubed_set = {x**3 for x in a if x % 3 == 0}
print(even_squares_dict)
print(threes_cubed_set)

#
alt_dict = dict(map(lambda x: (x, x**2),
                filter(lambda x: x % 2 == 0, a)))
alt_set = set(map(lambda x: x**3,
              filter(lambda x: x % 3 == 0, a)))
#
 아이템 28
#
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)

#
squared = [[x**2 for x in row] for row in matrix]
print(squared)

#
my_lists = [
    [[1, 2, 3], [4, 5, 6]],
    [[7, 8, 9], [1, 2, 3]],
    [[4, 5, 6], [7, 8, 9]],
]
flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]

#
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)

#
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0]

#
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]
print(filtered)
# 아이템 29
#
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
    count = stock.get(name, 0)
    batches = get_batches(count, 8)
    if batches:
        result[name] = batches

print(result)

#
found = {name: get_batches(stock.get(name, 0), 8)
         for name in order
         if get_batches(stock.get(name, 0), 8)}
print(found)

#
has_bug = {name: get_batches(stock.get(name, 0), 4)
           for name in order
           if get_batches(stock.get(name, 0), 8)}

print('예상:', found)
print('실졔: ', has_bug)

#
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#result = {name: (tenth := count // 10)
#          for name, count in stock.items() if tenth > 0}

#
result = {name: tenth for name, count in stock.items()
          if (tenth := count // 10) > 0}
print(result)

#
half = [(last := count // 2) for count in stock.values()]
print(f'{half}의 마지막 원소는 {last}')

#
for count in stock.values(): # 루프 변수가 누출됨
    pass

print(f'{list(stock.values())}의 마지막 원소는 {count}')

#
half = [count // 2 for count in stock.values()]
print(half)  # 작동함
print(count) # 루프 변수가 누출되지 않기 때문에 예외가 발생함

#
stock = {
    '못': 125,
    '나사못': 35,
    '나비너트': 8,
    '와셔': 24,
}

order = ['나사못', '나비너트', '클립']

found = ((name, batches) for name in order
         if (batches := get_batches(stock.get(name, 0), 8)))
print(next(found))
print(next(found))

#
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

#
visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0

#
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

#
it = read_visits('my_numbers.txt')
percentages = normalize(it)
print(percentages)

#
it = read_visits('my_numbers.txt')
print(list(it))
print(list(it)) # 이미 모든 원소를 다 소진했다

#
def normalize_copy(numbers):
    numbers_copy = list(numbers) # 이터레이터 복사
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result

#
it = read_visits('my_numbers.txt')
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0

#
def normalize_func(get_iter):
    total = sum(get_iter())  # 새 이터레이터
    result = []
    for value in get_iter(): # 새 이터레이터
        percent = 100 * value / total
        result.append(percent)
    return result

#
path = 'my_numbers.txt'
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0

#
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

#
visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0

#
def normalize_defensive(numbers):
    if iter(numbers) is numbers: # 이터레이터 -- 나쁨!
        raise TypeError('컨테이너를 제공해야 합니다')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

#
from collections.abc import Iterator

def normalize_defensive(numbers):
    if isinstance(numbers, Iterator): # 반복 가능한 이터레이터인지 검사하는 다른 방법
        raise TypeError('컨테이너를 제공해야 합니다')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

#
visits = [15, 35, 80]
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0

visits = ReadVisits(path)
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0

#
visits = [15, 35, 80]
it = iter(visits)
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#normalize_defensive(it)
