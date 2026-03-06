class Grid:

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = []

    def build_grid(self):
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(0xf)
            self.grid.append(row)
    
    def get_cell(self, x, y):
        if (0 <= x < self.width and 0 <= y < self.height):
            return self.grid[y][x]
        else:
            return None
    def set_cell(self, x, y, val) -> None:
        if (0 <= x < self.width and 0 <= y < self.height):
            self.grid[y][x] = val
