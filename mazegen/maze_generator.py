from constants import DIRECTIONS, OPPOSITE
from constants import PATH_PARSER
from collections import deque
from typing import Optional, Callable
import random
from pattern_font import PATTERN_42_FONT
from custom_pattern_font import PATTERNS_FONTS
from hollow_cells import HOLLOW_CELLS


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: dict[str, int],
        exit: dict[str, int],
        perfect: bool,
        pattern: str,
        seed: Optional[int]
    ) -> None:
        """Initialize the MazeGenerator with grid, dimensions, and config"""

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.pattern = pattern or '42'
        self.seed = seed
        self.grid = [[15] * self.width for _ in range(self.height)]
        self.visited: list[list[bool]] = [
            [False] * self.width for _ in range(self.height)
        ]
        self.solution_path: list[str] = []
        self.mask: set[tuple[int, int]] = set()
        self.pattern_grid: list[list[int]] = []
        self.size_warning: str = ""

    def build_pattern(self) -> list[list[int]]:
        """Build the combined pattern grid for the current pattern string"""

        if self.pattern != '42':
            pattern_grid = PATTERNS_FONTS
            row_height = 7
            self.pattern = self.pattern.upper()
        else:
            pattern_grid = PATTERN_42_FONT
            row_height = 5

        combined_pattern = []
        for row_indx in range(row_height):
            combined_row = []
            for char in self.pattern:
                combined_row += pattern_grid[char][row_indx]
                combined_row += [0]
            combined_pattern.append(combined_row[:-1])
        return combined_pattern

    def pattern_mask(self) -> None:
        """
        Build the mask set by marking
        all pattern cells as blocked for DFS
        """

        pattern_grid = self.pattern_grid
        pattern_height = len(pattern_grid)
        pattern_width = len(pattern_grid[0])
        start_row = self.height // 2 - pattern_height // 2
        start_col = self.width // 2 - pattern_width // 2
        for p_row in range(pattern_height):
            for p_col in range(pattern_width):
                if pattern_grid[p_row][p_col] == 1:
                    self.mask.add((start_row + p_row, start_col + p_col))

    def break_wall(self, c_row: int, c_col: int, direction: int) -> None:
        """Break the wall between current cell and its neighbor"""

        d_row, d_col = DIRECTIONS[direction]
        n_row, n_col = c_row + d_row, c_col + d_col
        self.grid[c_row][c_col] &= ~direction
        self.grid[n_row][n_col] &= ~OPPOSITE[direction]

    def neighbors_cells(
        self, c_row: int, c_col: int
    ) -> list[tuple[int, int, int]]:
        """Return unvisited, unmasked neighbors of the current cell"""

        neighbors = []
        for direction, (d_row, d_col) in DIRECTIONS.items():
            n_row, n_col = c_row + d_row, c_col + d_col
            if 0 <= n_col < self.width and 0 <= n_row < self.height:
                not_visited = not self.visited[n_row][n_col]
                not_masked = (n_row, n_col) not in self.mask
                if not_visited and not_masked:
                    neighbors.append((n_row, n_col, direction))
        return neighbors

    def hollow_pattern(self) -> None:
        """Open walls inside hollow areas of pattern characters"""

        if self.pattern == '42' or not self.pattern_grid:
            return
        pattern_grid = self.pattern_grid
        pattern_height = len(pattern_grid)
        pattern_width = len(pattern_grid[0])
        start_row = self.height // 2 - pattern_height // 2
        start_col = self.width // 2 - pattern_width // 2
        for char_index, char in enumerate(self.pattern):
            if char not in HOLLOW_CELLS:
                continue
            char_col_offset = char_index * 6
            for p_row, p_col in HOLLOW_CELLS[char]:
                abs_p_col = p_col + char_col_offset
                grid_row = start_row + p_row
                grid_col = start_col + abs_p_col
                for d, (d_row, d_col) in DIRECTIONS.items():
                    n_p_row = p_row + d_row
                    n_p_col = abs_p_col + d_col
                    n_grid_row = grid_row + d_row
                    n_grid_col = grid_col + d_col
                    row_in_bounds = 0 <= n_p_row < pattern_height
                    col_in_bounds = 0 <= n_p_col < pattern_width
                    if row_in_bounds and col_in_bounds:
                        if pattern_grid[n_p_row][n_p_col] == 0:
                            opp = OPPOSITE[d]
                            curr_wall = self.grid[grid_row][grid_col] & d
                            n_wall = self.grid[n_grid_row][n_grid_col] & opp
                            if curr_wall:
                                self.grid[grid_row][grid_col] &= ~d
                            if n_wall:
                                self.grid[n_grid_row][n_grid_col] &= ~opp

    def get_min_dimensions(self) -> tuple[int, int]:
        """
        Return minimum width and height
        required to fit the current pattern
        """

        min_w = len(self.pattern_grid[0]) + 4
        min_h = len(self.pattern_grid) + 4
        return min_w, min_h

    def print_pattern_too_large(self, pattern_name: str) -> None:
        """Print error message when pattern is too large for the maze"""

        min_w, min_h = self.get_min_dimensions()
        print(f"Pattern '{pattern_name}' too large!")
        print(f"Requires at least WIDTH={min_w} HEIGHT={min_h}\n")

    def validate_entry_exit(self) -> None:
        """Validate that entry and exit do not fall inside the pattern mask"""

        entry_cell = (self.entry['y'], self.entry['x'])
        exit_cell = (self.exit['y'], self.exit['x'])
        if entry_cell in self.mask:
            print('Error: entry coordinates are inside the pattern')
            exit(1)
        if exit_cell in self.mask:
            print('Error: exit coordinates are inside the pattern')
            exit(1)

    def validate_pattern_size(self) -> bool:
        """Validate that the maze is large enough to fit the pattern"""

        min_width, min_height = self.get_min_dimensions()
        if self.height < min_height or self.width < min_width:
            return False
        return True

    def check_pattern_size(self) -> bool:
        """Check pattern size and exit with error message if too large"""

        if not self.validate_pattern_size():
            min_w, min_h = self.get_min_dimensions()
            self.size_warning = (
                f"\033[38;5;226mWarning: Maze too small"
                f"to display '{self.pattern}'\n"
                f"Requires at least WIDTH={min_w} HEIGHT={min_h}\033[0m\n"
            )
            self.pattern_grid = []
            self.mask = set()
            return False
        return True

    def build_hollow_set(self) -> set[tuple[int, int]]:
        """
            Return absolute grid positions
            of all hollow cells in the pattern.
        """

        hollow_set: set[tuple[int, int]] = set()
        pattern_height = len(self.pattern_grid)
        pattern_width = len(self.pattern_grid[0])
        start_row = self.height // 2 - pattern_height // 2
        start_col = self.width // 2 - pattern_width // 2
        for char_index, char in enumerate(self.pattern):
            if char in HOLLOW_CELLS:
                char_col_offset = char_index * 6
                for p_row, p_col in HOLLOW_CELLS[char]:
                    abs_row = start_row + p_row
                    abs_col = start_col + p_col + char_col_offset
                    hollow_set.add((abs_row, abs_col))
        return hollow_set

    def dfs(
        self,
        callback: Optional[Callable] = None
    ) -> None:
        """Generate maze using iterative DFS recursive backtracker."""

        self.pattern_grid = self.build_pattern()
        pattern_exist = self.check_pattern_size()
        if pattern_exist:
            self.pattern_mask()
            self.validate_entry_exit()
        if self.seed is None:
            self.seed = random.randint(1, 99999)
        random.seed(self.seed)

        hollow_set = self.build_hollow_set() if pattern_exist else set()
        while True:
            curr_cell_row = random.randint(0, self.height - 1)
            curr_cell_col = random.randint(0, self.width - 1)
            if ((curr_cell_row, curr_cell_col) not in self.mask
                    and (curr_cell_row, curr_cell_col) not in hollow_set):
                break

        stack = []
        curr_cell = (curr_cell_row, curr_cell_col)
        stack.append(curr_cell)
        self.visited[curr_cell_row][curr_cell_col] = True

        while stack:
            curr_cell_neighbors = self.neighbors_cells(*curr_cell)
            if curr_cell_neighbors:
                random_cell = random.randint(0, len(curr_cell_neighbors) - 1)
                vc_row, vc_col, direction = curr_cell_neighbors[random_cell]
                self.break_wall(curr_cell_row, curr_cell_col, direction)
                if callback:
                    callback(curr_cell_row, curr_cell_col)
                curr_cell = (vc_row, vc_col)
                stack.append(curr_cell)
                self.visited[vc_row][vc_col] = True
                curr_cell_row, curr_cell_col = curr_cell
            else:
                stack.pop()
                if stack:
                    curr_cell = stack[-1]
                    curr_cell_row, curr_cell_col = curr_cell
        self.make_imperfect()
        self.hollow_pattern()

    def prim(self, callback: Optional[Callable] = None) -> None:
        """Generate maze using Prim's algorithm."""

        self.pattern_grid = self.build_pattern()
        pattern_exist = self.check_pattern_size()
        if pattern_exist:
            self.pattern_mask()
            self.validate_entry_exit()
        if self.seed is None:
            self.seed = random.randint(1, 99999)
        random.seed(self.seed)
        frontier = []
        hollow_set = self.build_hollow_set() if pattern_exist else set()
        while True:
            start_row = random.randint(0, self.height - 1)
            start_col = random.randint(0, self.width - 1)
            if ((start_row, start_col) not in self.mask
                    and (start_row, start_col) not in hollow_set):
                break

        self.visited[start_row][start_col] = True
        frontier += self.neighbors_cells(start_row, start_col)

        while frontier:
            idx = random.randint(0, len(frontier) - 1)
            n_row, n_col, direction = frontier.pop(idx)
            if not self.visited[n_row][n_col]:
                d_row, d_col = DIRECTIONS[direction]
                prev_row, prev_col = n_row - d_row, n_col - d_col
                self.break_wall(prev_row, prev_col, direction)
                if callback:
                    callback(n_row, n_col)
                self.visited[n_row][n_col] = True
                frontier += self.neighbors_cells(n_row, n_col)
        self.make_imperfect()
        self.hollow_pattern()

    def make_imperfect(self) -> None:
        """Randomly break extra walls to create loops in the maze."""

        if self.perfect:
            return
        for c_row in range(self.height):
            for c_col in range(self.width):
                for direction, (d_row, d_col) in DIRECTIONS.items():
                    n_row, n_col = c_row + d_row, c_col + d_col
                    if 0 <= n_row < self.height and 0 <= n_col < self.width:
                        wall = self.grid[n_row][n_col] & OPPOSITE[direction]
                        neighbor_masked = (n_row, n_col) in self.mask
                        current_masked = (c_row, c_col) in self.mask
                        if wall and not neighbor_masked and not current_masked:
                            if random.random() < 0.1:
                                self.break_wall(c_row, c_col, direction)

    def find_neighbors(
        self, c_row: int, c_col: int, distances: list[list[int]]
    ) -> list[tuple[int, int]]:
        """Return reachable unvisited neighbors for BFS pathfinding."""

        neighbors = []
        for direction, (d_row, d_col) in DIRECTIONS.items():
            n_row, n_col = c_row + d_row, c_col + d_col
            if 0 <= n_col < self.width and 0 <= n_row < self.height:
                if distances[n_row][n_col] == -1:
                    if self.grid[n_row][n_col] & OPPOSITE[direction] == 0:
                        neighbors.append((n_row, n_col))
        return neighbors

    def bfs(self) -> None:
        """
        Solve the maze using BFS algorithm
        to find the shortest path from entry to exit.
        """

        queue: deque[tuple[int, int]] = deque()
        distances = [[-1] * self.width for _ in range(self.height)]
        curr_cell = (self.entry['y'], self.entry['x'])
        exit_cell = (self.exit['y'], self.exit['x'])
        queue.append(curr_cell)
        c_row, c_col = curr_cell
        distances[c_row][c_col] = 0
        while queue:
            curr_cell = queue.popleft()
            c_row, c_col = curr_cell
            if curr_cell == exit_cell:
                break
            for n_row, n_col in self.find_neighbors(*curr_cell, distances):
                queue.append((n_row, n_col))
                distances[n_row][n_col] = distances[c_row][c_col] + 1
        e_row = self.entry['y']
        e_col = self.entry['x']
        c_row, c_col = curr_cell
        while (c_row, c_col) != (e_row, e_col):
            for direction, (d_row, d_col) in DIRECTIONS.items():
                n_row, n_col = c_row + d_row, c_col + d_col
                if 0 <= n_row < self.height and 0 <= n_col < self.width:
                    if distances[n_row][n_col] != -1:
                        wall = self.grid[n_row][n_col] & OPPOSITE[direction]
                        prev_dist = distances[c_row][c_col] - 1
                        if distances[n_row][n_col] == prev_dist and wall == 0:
                            self.solution_path.append(
                                PATH_PARSER[OPPOSITE[direction]]
                                )
                            c_row, c_col = n_row, n_col
                            break
        self.solution_path = list(reversed(self.solution_path))

    def generate(
                 self,
                 algorithm: str = 'dfs',
                 output_file: str = 'maze.txt'
                 ) -> None:
        """Generate and solve the maze and write"""
        """the maze in output file in one call"""

        if algorithm == 'dfs':
            self.dfs()
        else:
            self.prim()
        self.bfs()
        self.write_output(output_file)

    def write_output(self, filepath: str) -> None:
        """Write the maze grid, entry, exit and solution path to a file"""

        try:
            with open(filepath, 'w') as f:
                for row in self.grid:
                    f.write(''.join(format(col, 'X') for col in row) + '\n')
                f.write('\n')
                f.write(f"{self.entry['x']},{self.entry['y']}\n")
                f.write(f"{self.exit['x']},{self.exit['y']}\n")
                f.write(''.join(self.solution_path))
        except IsADirectoryError:
            print("Output file cannot be directory")
            exit(1)
