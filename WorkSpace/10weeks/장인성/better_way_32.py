# 긴 리스트 컴프리헨션보다는 제너레이터 식을 사용하라

# 파일이 크거나, 끝나지 않는 소켓의 경우 문제가 된다.
value = [len(x) for x in open('my_file.txt')]
print(value)

# ()로 만든 제너레이터 식은 이터레이터로 즉시 평가되어, 더 이상 시퀀스 원소 계산이 진행되지 않는다.
it = (len(x) for x in open('my_file.txt'))
print(it)

# 두 제너레이터 식을 합성할 수 있다.
roots = ((x, x ** 0.5) for x in it)
print(next(roots))