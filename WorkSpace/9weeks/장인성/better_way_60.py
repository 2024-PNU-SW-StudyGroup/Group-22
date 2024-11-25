# I/O를 할 때는 코루틴을 사용해 동시성을 높여라 

import asyncio

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


async def game_logic(state, neighbors):
    # data = await my_socket.read(50)
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state


async def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = await game_logic(state, neighbors)
    set(y, x, next_state)


async def simulate(grid):
    next_grid = Grid(grid.height, grid.width)

    tasks = []
    for y in range(grid.height):
        for x in range(grid.width):
            task = step_cell(y, x, grid.get, next_grid.set)
            tasks.append(task)

    await asyncio.gather(*tasks)

    return next_grid


grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)


for i in range(5):
    print(grid)
    grid = asyncio.run(simulate(grid))


# 코루틴을 시작하는 비용은 함수 호출뿐이다.
# 활성화된 코루틴은 종료될 때까지 1KB 미만의 메모리를 사용한다.