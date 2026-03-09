from collections import deque
import random
from grid import Grid
from renderer import Renderer
from config_parser import ConfigParser


parser = ConfigParser('config.txt')
parser.parsing_file()
WIDTH = parser.get_val('WIDTH')
HEIGHT = parser.get_val('HEIGHT')
OUTPUT_FILE = parser.get_val('OUTPUT_FILE')
ENTRY = parser.get_val('ENTRY')
EXIT = parser.get_val('EXIT')
PERFECT = parser.get_val('PERFECT')
seed = None
# seed = 7817301

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
    }

DIRECTIONS = {
    NORTH: (-1, 0),
    SOUTH: (1, 0),
    EAST: (0, 1),
    WEST: (0, -1)
    }

PATH_PARSER = {
    1: 'N',
    2: 'E',
    4: 'S',
    8: 'W'
}

PATTERN_HEIGHT = 5
PATTERN_WIDTH = 7

PATTERN_GRID = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]


class MazeGenerator:
    def __init__(self, grid):
        self.grid = grid
        self.visited = [[False] * WIDTH for _ in range(HEIGHT)]
        self.solution_path = []
        self.mask = set()

    def pattern_mask(self):
        if WIDTH < 9 or HEIGHT < 7:
            return
        start_row = HEIGHT // 2 - PATTERN_HEIGHT // 2
        start_col = WIDTH // 2 - PATTERN_WIDTH // 2
        for p_row in range(PATTERN_HEIGHT):
            for p_col in range(PATTERN_WIDTH):
                if PATTERN_GRID[p_row][p_col] == 1:
                    self.mask.add((start_row + p_row, start_col + p_col))

    def break_wall(self, c_row, c_col, direction):
        d_row, d_col = DIRECTIONS[direction]
        n_row, n_col = c_row + d_row, c_col + d_col
        self.grid[c_row][c_col] &= ~direction
        self.grid[n_row][n_col] &= ~OPPOSITE[direction]

    def neighbors_cells(self, c_row, c_col):
        neighbors = []
        for direction, (d_row, d_col) in DIRECTIONS.items():
            n_row, n_col = c_row + d_row, c_col + d_col
            if 0 <= n_col < WIDTH and 0 <= n_row < HEIGHT:
                masked = (n_row, n_col) in self.mask
                # print(masked)
                if not self.visited[n_row][n_col] and not masked:
                    neighbors.append((n_row, n_col, direction))
        return neighbors

    def dfs(self, entry, seed=None):
        self.pattern_mask()
        stack = []
        curr_cell_row, curr_cell_col = entry
        curr_cell = (curr_cell_row, curr_cell_col)
        stack.append(curr_cell)
        self.visited[curr_cell_row][curr_cell_col] = True
        if seed:
            random.seed(seed)
        else:
            seed = random.randint(1, 9999999)
            random.seed(seed)
        
        print('maze seed:', seed)
        while stack:
            # print(f'curr cell {curr_cell}')
            # print(f'curr row, col {curr_cell_row, curr_cell_col}')
            curr_cell_neighbors = self.neighbors_cells(*curr_cell)
            # print(f'neighbors {curr_cell_neighbors}')
            if curr_cell_neighbors:
                random_cell = random.randint(0, len(curr_cell_neighbors) - 1)
                # print(f'random cell to go {random_cell}')
                vc_row, vc_col, direction = curr_cell_neighbors[random_cell]
                self.break_wall(curr_cell_row, curr_cell_col, direction)
                curr_cell = (vc_row, vc_col)
                stack.append(curr_cell)
                self.visited[vc_row][vc_col] = True
                curr_cell_row, curr_cell_col = curr_cell
            else:
                stack.pop()
                # print(f'stack {stack}')
                if stack:
                    curr_cell = stack[-1]
                    curr_cell_row, curr_cell_col = curr_cell
            self.make_imperfect()

    def make_imperfect(self):
        if PERFECT:
            return
        for c_row in range(0, HEIGHT):
            for c_col in range(0, WIDTH):
                # print('cell: ', (c_row, c_col))
                for direction, (d_row, d_col) in DIRECTIONS.items():
                    n_row, n_col = c_row + d_row, c_col + d_col
                    # print('neightbors: ')
                    if 0 <= n_row < HEIGHT and 0 <= n_col < WIDTH:
                        wall = self.grid[n_row][n_col] & OPPOSITE[direction]
                        masked = (n_row, n_col) in self.mask
                        if wall and not masked:
                            if random.random() < 0.2:
                                # print('break')
                                # print(direction, (c_row, c_col))
                                self.break_wall(c_row, c_col, direction)

    def find_neighbors(self, c_row, c_col, distances):
        neighbors = []
        for direction, (d_row, d_col) in DIRECTIONS.items():
            n_row, n_col = c_row + d_row, c_col + d_col
            if 0 <= n_col < WIDTH and 0 <= n_row < HEIGHT:
                if distances[n_row][n_col] == -1:
                    # print('direction', direction)
                    wall = self.grid[n_row][n_col] & OPPOSITE[direction]
                    # print(f'from ({c_row},{c_col}) → ({n_row},{n_col}) wall={wall}')
                    # print(wall)
                    if wall == 0:
                        neighbors.append((n_row, n_col))
        return neighbors

    def solve_maze(self):
        distances = [[-1] * WIDTH for _ in range(HEIGHT)]
        queue = deque()
        curr_cell = (ENTRY['y'], ENTRY['x'])
        exit_cell = (EXIT['y'], EXIT['x'])
        queue.append(curr_cell)
        c_row, c_col = curr_cell
        distances[c_row][c_col] = 0
        while queue:
            curr_cell = queue.popleft()
            c_row, c_col = curr_cell
            if curr_cell == exit_cell:
                break
            curr_cell_neighbors = self.find_neighbors(*curr_cell, distances)
            # print(f'nb: {curr_cell} - {curr_cell_neighbors}')
            for n_row, n_col in curr_cell_neighbors:
                queue.append((n_row, n_col))
                distances[n_row][n_col] = distances[c_row][c_col] + 1
            # curr_cell = queue.popleft()
            # c_row, c_col = curr_cell

        e_row = ENTRY['y']
        e_col = ENTRY['x']
        c_row, c_col = curr_cell
        # print('star point: ', (c_row, c_col))
        while (c_row, c_col) != (e_row, e_col):
            for direction, (d_row, d_col) in DIRECTIONS.items():
                n_row, n_col = c_row + d_row, c_col + d_col
                # print('can i go', direction, (n_row, n_col))
                if 0 <= n_row < HEIGHT and 0 <= n_col < WIDTH:
                    if distances[n_row][n_col] != -1:
                        wall = self.grid[n_row][n_col] & OPPOSITE[direction]
                        # print(f'is wall open {wall}')
                        # print((n_row, n_col), wall)
                        if distances[n_row][n_col] == distances[c_row][c_col] - 1 and wall == 0:
                            # print('yes')
                            # print('am here now', direction, (n_row, n_col))
                            op_direction = OPPOSITE[direction]
                            self.solution_path.append(PATH_PARSER[op_direction])
                            c_row, c_col = n_row, n_col
                            break
        self.solution_path = list(reversed(self.solution_path))
        print(self.solution_path)

    def write_output(self, filepath, grid, entry, exit):
        with open(filepath, 'w') as f:
            for row in grid:
                hex_row = ""
                for col in row:
                    hex_row += format(col, 'X')
                f.write(f'{hex_row}\n')
            f.write('\n')
            f.write(f"{entry['x']},{entry['y']}\n")
            f.write(f"{exit['x']},{exit['y']}\n")
            f.write(''.join(self.solution_path))


if __name__ == "__main__":
    print('Before')
    grid = Grid(WIDTH, HEIGHT)
    grid.build_grid()
    # grid.render_grid(HEIGHT, WIDTH)
    r = Renderer(grid.grid, WIDTH, HEIGHT)
    r.renderer()
    print('After')
    maze = MazeGenerator(grid.grid)
    maze.dfs((ENTRY['y'], ENTRY['x']), seed)
    maze.solve_maze()
    maze.write_output(OUTPUT_FILE, grid.grid, ENTRY, EXIT)
    # print(maze.visited)
    r.renderer()
