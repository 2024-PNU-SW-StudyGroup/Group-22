import subprocess


proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()


print('종료 상태', proc.poll())



'''
except 문으로 이동한다.
종료 상태 -15 (SIGTERM)
'''