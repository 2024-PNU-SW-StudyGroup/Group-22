import subprocess
import time

# 윈도우에서는 sleep이 없는 경우 제대로 작동하지 않을 수 있다.

start = time.time()
sleep_procs = []
for _ in range(10):
    proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)

# 순차적으로 실행됐다면, 총 지연 시간은 10초 이상이었음.
for proc in sleep_procs:
    proc.communicate()

end = time.time()
delta = end - start
print(f'{delta:.3} 초만에 끝남')
