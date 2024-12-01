import subprocess
import os

# 시스템에 openssl을 설치하지 않은 경우에는 작동하지 않을 수 있다.
# - 파이썬 프로그램의 데이터를 파이프를 통해 하위 프로세스로 보내거나, 하위 프로세스의 출력 받기도 가능.
# - Ex) openssl command line 을 사용해 데이터 암호화 할때
def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush() # 자식이 입력을 받도록 보장한다
    return proc

procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)

for proc in procs:
    out, _ = proc.communicate()
    print(out[-10:])
