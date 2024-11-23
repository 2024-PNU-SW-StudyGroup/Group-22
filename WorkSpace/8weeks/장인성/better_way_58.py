# 동시성과 Queue를 사용하기 위해 코드를 어떻게 리팩터링해야 하는지 이해하라

from queue import Queue
from threading import Thread

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


class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)



def game_logic(state, neighbors):
    # raise OSError('게임 로직에서 I/O 문제 발생')

    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state

def game_logic_thread(item):
    y, x, state, neighbors = item
    try:
        next_state = game_logic(state, neighbors)
    except Exception as e:
        next_state = e
    return (y, x, next_state)


def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)


in_queue = ClosableQueue()
out_queue = ClosableQueue()

threads = []
for y in range(5):
    thread = StoppableWorker(game_logic_thread, in_queue, out_queue)
    thread.start()
    threads.append(thread)

def simulate_pipeline(grid, in_queue, out_queue):
    for y in range(grid.height):
        for x in range(grid.width):
            state = grid.get(y, x)
            neighbors = count_neighbors(y, x, grid.get)
            in_queue.put((y, x, state, neighbors))
    
    in_queue.join()
    out_queue.close()
    next_grid = Grid(grid.height, grid.width)
    for item in out_queue:
        y, x, next_state = item
        if isinstance(next_state, Exception):
            raise SimulationError(y, x) from next_state
        next_grid.set(y, x, next_state)
    
    return next_grid


# simulate_pipeline(Grid(1, 1), in_queue, out_queue)

grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

for i in range(5):
    print(grid)
    grid = simulate_pipeline(grid, in_queue, out_queue)

for thread in threads:
    in_queue.close()
for thread in threads:
    thread.join()

# game_logic뿐 아니라 count_neighbors 함수에서도 I/O를 수행해야할 때, 별도의 스레드에서 실행하는 단계를 파이프라인에 추가해야 한다.
# 코드 변경할 부분이 많아진다
# Queue를 사용하는 방식이 Thread보다 낫지만 부가 비용이 많이 필요하다