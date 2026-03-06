from grid import Grid
from renderer import Renderer 
from config_parser import ConfigParser

HEIGHT = 3
WIDTH = 3

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
        self.visited = [[False] * WIDTH for _ in range(HEIGHT)]
    
    def break_wall(self, x, y, direction):
        dx, dy = DELTA[direction]
        nx, ny = x + dx, y + dy
        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~OPPOSITE[direction]

        
    def neighbours_cells(self, x, y):
        neighbours = []
        for direction, (dx, dy) in DELTA.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                if not self.visited[ny][nx]:
                    neighbours.append((nx, ny, direction))
        return neighbours

    def dfs(self, entry):
        ex, ey = entry
        self.visited[ey][ex] = True
        neighbours = self.neighbours_cells(ex, ey)
        print(neighbours)
        for x, y, direction in neighbours:
            self.visited[y][x] = True
            self.break_wall(x, y, direction)

if __name__ == "__main__":
    parser = ConfigParser('config.txt')
    parser.parsing_file()

    # WIDTH = parser.get_val('WIDTH')
    # HEIGHT = parser.get_val('HEIGHT')


    print('Before')
    grid = Grid(WIDTH, HEIGHT)
    grid.build_grid()
    # grid.render_grid(HEIGHT, WIDTH)
    r = Renderer(grid.grid, WIDTH, HEIGHT)
    r.renderer()
    print('After')
    maze = MazeGenerator(grid.grid)
    # maze.break_wall(0, 2, WEST)
    # maze.break_wall(1, 2, WEST)
    # maze.break_wall(0, 3, SOUTH)
    # maze.break_wall(1, 3, SOUTH)
    # maze.break_wall(2, 3, SOUTH)
    # maze.break_wall(1, 2, SOUTH)
    # maze.break_wall(3, 0, SOUTH)
    # maze.break_wall(1, 0, SOUTH)
    # maze.break_wall(2, 2, NORTH)
    # maze.break_wall(0, 0, EAST)
    # maze.break_wall(0, 4, SOUTH)
    # maze.break_wall(1, 4, SOUTH)
    # maze.break_wall(1, 4, SOUTH)
    # print(maze.visited)
    # print(maze.neighbours(0,0))
    maze.dfs((0,0))
    print(maze.visited)
    r.renderer()