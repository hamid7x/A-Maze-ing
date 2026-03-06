from grid import Grid
from renderer import Renderer 

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
DELTA = {
    NORTH: (0,-1),
    SOUTH: (0,1),
    EAST: (1,0),
    WEST: (-1,0)
    }
class MazeGenerator:
    def __init__(self, grid):
        self.grid = grid
    
    def break_wall(self, y, x, direction):
        dx, dy = DELTA[direction]
        nx, ny = x + dx, dy + y
        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~OPPOSITE[direction]

if __name__ == "__main__":
    WIDTH = 5
    HEIGHT = 5
    print('Before')
    grid = Grid(WIDTH, HEIGHT)
    grid.build_grid()
    # grid.render_grid(HEIGHT, WIDTH)
    r = Renderer(grid.grid, WIDTH, HEIGHT)
    r.renderer()
    print('After')
    maze = MazeGenerator(grid.grid)
    maze.break_wall(0, 2, WEST)
    maze.break_wall(1, 2, WEST)
    # maze.break_wall(0, 1, SOUTH)
    # maze.break_wall(1, 1, EAST)
    # maze.break_wall(0, 4, WEST)
    # maze.break_wall(0, 3, WEST)
    maze.break_wall(0, 3, SOUTH)
    maze.break_wall(1, 3, SOUTH)
    maze.break_wall(2, 3, SOUTH)
    # maze.break_wall(1, 2, SOUTH)
    # maze.break_wall(3, 0, SOUTH)
    # maze.break_wall(1, 0, SOUTH)
    # maze.break_wall(2, 2, NORTH)
    # grid.print_grid()
    r.renderer()
 