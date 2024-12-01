import subprocess

# 윈도우에서는 sleep이 없는 경우 제대로 작동하지 않을 수 있다.

# - run 함수 대신 Popen 클래스를 사용해 하위 프로세스를 만들면 파이썬이 다른 일을 하면서 주기적으로 자식 프로세스의 상태를 검사(polling)할 수 있다.
# 작업이 끝나지 않으면 proc.poll() 값이 None, 끝나면 0으로 바뀐다.
proc = subprocess.Popen(['sleep', '1'])
while proc.poll() is None:
    print('작업중...')
    # 시간이 걸리는 작업을 여기서 수행한다

print('종료 상태', proc.poll())


