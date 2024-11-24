# map과 filter 대신 컴프리헨션을 사용하라

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# 리스트 컴프리헨션
even_squares = [x**2 for x in a if x % 2 == 0]
# filter 내장 함수를 map과 함께 사용할 수도 있지만, 읽기가 어렵다
alt = map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, a))


# 딕셔너리 컴프리헨션
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
alt_dict = dict(map(lambda x: (x, x**2), filter(lambda x: x % 2 == 0, a)))


# 집합 컴프리헨션
threes_cubed_set = {x**3 for x in a if x % 3 == 0}
alt_set = set(map(lambda x: x**3, filter(lambda x: x % 3 == 0, a)))

