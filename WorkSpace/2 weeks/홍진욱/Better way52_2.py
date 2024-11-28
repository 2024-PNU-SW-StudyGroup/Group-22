import subprocess

# 윈도우에서는 sleep이 없는 경우 제대로 작동하지 않을 수 있다.

# - 파이썬에서 자식프로세스는 부모 프로세스(파이썬 인터프리터)와 독립적으로 실행.
# - run 함수 대신 popen 클래스 사용하면, 다른일 하면서 주기적으로 자식 프로세스 상태 검사 가능.
proc = subprocess.Popen(['sleep', '1'])
while proc.poll() is None:
    print('작업중...')
    # 시간이 걸리는 작업을 여기서 수행한다

print('종료 상태', proc.poll())


