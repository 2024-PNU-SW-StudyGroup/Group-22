# 호출자를 API로부터 보호하기 위해 최상위 Exception을 정의하라


import logging
import my_module


try:
    weight = my_module.determine_weight(-1, 1)
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error: # 첫 번째 효과: 최상위 예외가 있으면 API를 호출하는 사용자가 API를 잘못 사용한 경우를 더 쉽게 이해할 수 있다.
    logging.exception("호출 코드에 버그가 있음")


try:
    weight = my_module.determine_weight(0, 1)
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error:
    logging.exception("호출 코드에 버그가 있음")
except Exception: # API 모듈 코드의 버그를 발견할 때 도움이 된다.
    logging.exception("API 코드에 버그가 있음!")
    raise