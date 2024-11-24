# 리스트를 반환하기보다는 제너레이터를 사용하라


# 핵심을 알아보기 어렵다
# 반환하기 전에 모든 결과를 저장해야 한다. 메모리가 터질 수 있다.
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

address = '컴퓨터(영어: Computer, 문화어: 콤퓨터, 순화어: 전산기)는 진공관'
result = index_words(address)
print(result[:10])


# 제너레이터를 사용한다
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1


it = index_words_iter(address)
print(next(it))
print(next(it))


# 제너레이터가 반환하는 이터레이터를 리스트 내장 함수에 넘기면 제너레이터를 쉽게 리스트로 변환할 수 있다.
result = list(index_words_iter(address))
print(result[:10])