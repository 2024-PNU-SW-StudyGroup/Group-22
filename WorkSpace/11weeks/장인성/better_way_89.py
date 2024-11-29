# 리팩터링과 마이그레이션 방법을 알려주기 위해 warning을 사용하라


import warnings


CONVERSIONS = {
    'mph': 1.60934 / 3600 * 1000,
    '시간': 3600,
    '마일': 1.60934 * 1000,
    '미터': 1,
    'm/s': 1,
    '초': 1
}


def convert(value, units):
    rate = CONVERSIONS[units]
    return rate * value


def localize(value, units):
    rate = CONVERSIONS[units]
    return value / rate


def require(name, value, default):
    if value is not None:
        return value
    warnings.warn(
        f'{name}이(가) 곧 필수가 됩니다. 코드를 변경해주세요', 
        DeprecationWarning,
        stacklevel=3) # 현재 함수의 호출자의 호출자에서 경고를 발생시킨다.
    return default
    

def print_distance(speed, duration, *,
                   speed_units=None,
                   time_units=None,
                   distance_units=None):
    
    speed_units = require('speed_units', speed_units, 'mph')
    time_units = require('time_units', time_units, '시간')
    distance_units = require('distance_units', distance_units, '마일')

    norm_speed = convert(speed, speed_units)
    norm_duration = convert(duration, time_units)
    norm_distance = norm_speed * norm_duration
    distance = localize(norm_distance, distance_units)
    print(f'{distance} {distance_units}')


import contextlib
import io


fake_stderr = io.StringIO()
with contextlib.redirect_stderr(fake_stderr):
    print_distance(1000, 3,
                   speed_units='미터',
                   time_units='초')
    

print(fake_stderr.getvalue())



    

