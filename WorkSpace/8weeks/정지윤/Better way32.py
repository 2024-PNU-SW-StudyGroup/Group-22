
#
# 아이템 32
#

# 파일에서 읽은 x에는 newline이 들어있음에 유의하라
value = [len(x) for x in open('my_file.txt')]
print(value)

"""
제너레이터 식이 이터레이터를 다른 제너레이터 하위 식으로 사용함으로써 제너레이터 식을 서로 합성할 수 있다
"""
