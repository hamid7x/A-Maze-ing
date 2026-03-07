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


class MazeGenerator:
    def __init__(self, grid):
        self.grid = grid
        self.visited = [[False] * WIDTH for _ in range(HEIGHT)]

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
                if not self.visited[n_row][n_col]:
                    neighbors.append((n_row, n_col, direction))
        return neighbors

    def dfs(self, entry):
        stack = []
        curr_cell_row, curr_cell_col = entry
        curr_cell = (curr_cell_row, curr_cell_col)
        stack.append(curr_cell)
        self.visited[curr_cell_row][curr_cell_col] = True

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


if __name__ == "__main__":
    print('Before')
    grid = Grid(WIDTH, HEIGHT)
    grid.build_grid()
    # grid.render_grid(HEIGHT, WIDTH)
    r = Renderer(grid.grid, WIDTH, HEIGHT)
    r.renderer()
    print('After')
    maze = MazeGenerator(grid.grid)
    maze.dfs((0, 0))
    maze.write_output(OUTPUT_FILE, grid.grid, ENTRY, EXIT)
    # print(maze.visited)
    r.renderer()
