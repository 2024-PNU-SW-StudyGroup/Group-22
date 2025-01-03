# 언제 동시성이 필요할지 인식하는 방법을 알아두라

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


def game_logic(state, neighbors):
    # Blocking I/O
    # data = my_socket.recv(100)
    # 순차적으로 처리 시 그리드 크기만큼 선형적으로 시간이 소요
    # 해결책: I/O를 병렬로 수행하여 그리드 크기와 관계없이 각 세대를 계산

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
    next_grid = Grid(grid.height, grid.width)
    for y in range(grid.height):
        for x in range(grid.width):
            step_cell(y, x, grid.get, next_grid.set)
    return next_grid


grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

for i in range(5):
    print(grid)
    grid = simulate(grid)