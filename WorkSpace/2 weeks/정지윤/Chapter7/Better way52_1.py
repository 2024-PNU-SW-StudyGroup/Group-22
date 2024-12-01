import subprocess

# 파이썬 3.6이나 그 이전 버전에서는 제대로 작동하지 않는다.(capture_output을 사용할 수 없음)
# 윈도우에서는 echo가 없는 경우 제대로 작동하지 않을 수 있다.

# - 부모 프로세스 -> 파이썬 인터프리터
# - 한국어 시스템에서는 UTF-8 대신 cp949나 euc-kr 인코딩이 출력에 쓰일 때도 있다.
# - subprocess 등의 모듈을 통해 실행한 자식 프로세스는 부모 프로세스인 파이썬 인터프리터와 독립적으로 실행된다.
result = subprocess.run(['echo', '자식프로세스가 보내는 인사!'], capture_output=True, encoding='utf-8')

result.check_returncode() # 예외가 발생하지 않으면 문제 없이 잘 종료한 것이다
print(result.stdout) #
