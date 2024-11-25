# 동시성을 위해 스레드가 필요한 경우에는 ThreadpoolExecutor를 사용하라

from queue import Queue
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor

ALIVE = '*'
EMPTY = '-'


class SimulationError(Exception):
    pass

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
    # data = my_socket.recv(100)
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


def simulate_pool(pool, grid):
    next_grid = LockingGrid(grid.height, grid.width)
    futures = []
    for y in range(grid.height):
        for x in range(grid.width):
            args = (y, x, grid.get, next_grid.set)
            future = pool.submit(step_cell, *args)
            futures.append(future)

    for future in futures:
        future.result()

    return next_grid


grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)


with ThreadPoolExecutor(max_workers=10) as pool:
    task = pool.submit(game_logic, ALIVE, 3)
    task.result()

with ThreadPoolExecutor(max_workers=10) as pool:
    for i in range(5):
        print(grid)
        grid = simulate_pool(pool, grid)        

# 스레드를 실행하는 중에 발생한 예외를 자동으로 전파시켜준다
# 스레드 시작 비용을 줄일 수 있다
# max_workers의 개수를 미리 지정해야 하므로 I/O 병렬성을 제한한다