import subprocess
import time

# 윈도우에서는 sleep이 없는 경우 제대로 작동하지 않을 수 있다.
# - 자식프로세스, 부모프로세스 분리하면 원하는개수만큼 많은 자식 프로세스 병렬 실행 가능.
start = time.time()
sleep_procs = []
for _ in range(10):
    proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)

for proc in sleep_procs:
    proc.communicate()

end = time.time()
delta = end - start
print(f'{delta:.3} 초만에 끝남')
