#
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

"""
리스트 컴프리헨션은 C언어로 구현된 Python의 내부 루프 사용 -> for loop보다 빠르다
"""
