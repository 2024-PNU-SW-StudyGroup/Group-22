# 이터레이터나 제너레이터를 다룰 때는 itertools를 사용하라

import itertools

# chain: 여러 이터레이터를 하나의 순차적인 이터레이터로 합치고 싶을 때
it = itertools.chain([1, 2, 3], [4, 5 ,6])
print(list(it))

# repeat: 한 값을 계속 반복해 내놓고 싶을 때
it = itertools.repeat('안녕', 3)
print(list(it))

# cycle: 어떤 이터레이터가 내높는 원소를 계속 반복하고 싶을 때
it = itertools.cycle([1, 2])
result = [next(it) for _ in range(10)]
print(result)

# tee: 한 이터레이터를 병렬적으로 두 번째 인자로 지정된 개수의 이터레이터로 만들고 싶을 때
it1, it2, it3 = itertools.tee(['하나', '둘'], 3)
print(list(it1))
print(list(it2))
print(list(it3))

# zip_longest: 여러 이터레이터 중 짧은 쪽 이터레이터의 원소를 다 사용한 경우 fillvalue로 지정한 값을 채워 넣어준다.
keys = ['하나', '둘', '셋']
values = [1, 2]
normal = list(zip(keys, values))
print('zip:', normal)
it = itertools.zip_longest(keys, values, fillvalue='없음')
longest = list(it)
print('zip_longest:', longest)


# islice: 이터레이터를 슬라이싱하고 싶을 때
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
first_five = itertools.islice(range(10), 5)
print('앞에서 다섯 개:', list(first_five))

middle_odds = itertools.islice(range(10), 2, 8, 2)
print('중간의 홀수들:', list(middle_odds))

# takewhile: 이터레이터에서 False를 반환하는 첫 원소가 나타날 때까지 원소를 돌려준다.
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, values)
print(list(it))

# dropwhile: takewhile과 반대로, False를 반환하는 첫 원소를 찾을 때까지 원소를 건너뛴다.
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.dropwhile(less_than_seven, values)
print(list(it))

# filterfalse: filter와 반대로, False를 반환하는 모든 원소를 돌려준다.
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = lambda x: x % 2 == 0
filter_result = filter(evens, values)
print('Filter:', list(filter_result))

filter_false_result = itertools.filterfalse(evens, values)
print('Filter false:', list(filter_false_result))

# accumulate: 파라미터를 두 개 받는 함수를 반복 적용하면서 이터레이터 원소를 값 하나로 줄여준다. 이터레이터의 각 원소에 대해 누적된 결과를 내놓는다.
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_reduce = itertools.accumulate(values)
print('합계:', list(sum_reduce))

def sum_modulo_20(first, second):
    output = first + second
    return output % 20

modulo_reduce = itertools.accumulate(values, sum_modulo_20)
print('20으로 나눈 나머지의 합계:', list(modulo_reduce))

# product: 하나 이상의 이터레이터에 들어 있는 아이템들의 데카르트 곱을 반환한다.
single = itertools.product([1, 2], repeat=2)
print('리스트 한 개:', list(single))
multiple = itertools.product([1, 2], ['a', 'b'])
print('리스트 두 개:', list(multiple))

# permutations: 이터레이터가 내놓는 원소들로부터 만들어낸 길이 N의 순열을 돌려준다.
it = itertools.permutations([1, 2, 3, 4], 2)
print(list(it))

# combinations: 이터레이터가 내놓는 원소들로부터 만들어낸 길이 N의 조합을 돌려준다.
it = itertools.combinations([1, 2, 3, 4], 2)
print(list(it))

# combinations_with_replacement: 중복 조합을 돌려준다.
it = itertools.combinations_with_replacement([1, 2, 3, 4], 2)
print(list(it))