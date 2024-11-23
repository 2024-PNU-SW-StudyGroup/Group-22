# 요구에 따라 팬아웃을 진행하려면 새로운 스레드를 생성하지 마라

from threading import Thread, Lock
import contextlib
import io

ALIVE = '*'
EMPTY = '-'

class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

        
    def get(self, y, x):
        return self.rows[y % self.height][x % self.width]
    

    def set(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state


    def __str__(self):
        grid_str = ""
        for row in self.rows:
            for c in row:
                grid_str += c
            grid_str += '\n'
        return grid_str
    

class LockingGrid(Grid):
    def __init__(self, height, width):
        super().__init__(height, width)
        self.lock = Lock()
     

    def __str__(self):
        with self.lock:
            return super().__str__()
        
    def get(self, y, x):
        with self.lock:
            return super().get(y, x)
        
    def set(self, y, x, state):
        with self.lock:
            return super().set(y, x, state)


def count_neighbors(y, x, get):
    n_ = get(y-1, x+0)
    ne = get(y-1, x+1)
    e_ = get(y+0, x+1)
    se = get(y+1, x+1)
    s_ = get(y+1, x+0)
    sw = get(y+1, x-1)
    w_ = get(y+0, x-1)
    nw = get(y-1, x-1)

    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


def game_logic(state, neighbors):
    # Blocking I/O
    # data = my_socket.recv(100)
    # 순차적으로 처리 시 그리드 크기만큼 선형적으로 시간이 소요
    # 해결책: I/O를 병렬로 수행하여 그리드 크기와 관계없이 각 세대를 계산

    raise OSError('I/O 문제 발생')

    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state


def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)


def simulate(grid):
    next_grid = LockingGrid(grid.height, grid.width)


    # 스레드를 사용한 코드는 유지보수가 어렵다
    # 스레드 하나 당 8MB의 메모리가 필요하여, 메모리가 많이 필요하다
    # 스레드를 시작하는 비용, 컨텍스트 스위치에 많은 비용이 필요하다
    threads = []
    for y in range(grid.height):
        for x in range(grid.width):
            args = (y, x, grid.get, next_grid.set)
            thread = Thread(target=step_cell, args=args)
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    return next_grid


fake_stderr = io.StringIO()
with contextlib.redirect_stderr(fake_stderr):
    thread = Thread(target=game_logic, args=(ALIVE, 3))
    thread.start()
    thread.join()

print(fake_stderr.getvalue())

# 예외가 스레드를 시작한 쪽으로 다시 던져지지 않는다 -> 디버깅이 어렵다


# grid = LockingGrid(5, 9)
# grid.set(0, 3, ALIVE)
# grid.set(1, 4, ALIVE)
# grid.set(2, 2, ALIVE)
# grid.set(2, 3, ALIVE)
# grid.set(2, 4, ALIVE)

# for i in range(5):
#     print(grid)
#     grid = simulate(grid)