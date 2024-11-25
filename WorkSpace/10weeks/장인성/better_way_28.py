# 컴프리헨션 내부에 제어 하위 식을 세 개 이상 사용하지 말라

# 이해하기 어려우므로 일반 if와 for문을 사용하고 도우미 함수를 작성하라
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0] for row in matrix if sum(row) >= 10]
