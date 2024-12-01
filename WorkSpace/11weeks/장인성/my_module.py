class Error(Exception):
    """이 모듈에서 발생할 모든 예외의 상위 클래스."""


class InvalidDensityError(Error):
    """밀도 값이 잘못된 경우."""


class InvalidVolumeError(Error):
    """부피 값이 잘못된 경우."""


# 세 번째 효과: 미래의 API를 보호해준다.
class NegativeDensityError(InvalidDensityError):
    """밀도가 음수인 경우."""


def determine_weight(volume, density):
    if density < 0:
        raise InvalidDensityError(f"밀도는 0보다 커야 합니다.")
    if volume < 0:
        raise InvalidVolumeError(f"부피는 0보다 커야 합니다.")
    if volume == 0:
        density / volume # API 코드의 버그