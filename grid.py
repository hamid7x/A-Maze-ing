class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = self.build_grid()
    def build_grid(self):
        grid = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(0xf)
            grid.append(row)
        return grid
    
    def get_cell(self, x, y):
        if (0 <= x < self.width and 0 <= y < self.height):
            return self.grid[y][x]
        else:
            return None
    def set_cell(self, x, y, val) -> None:
        if (0 <= x < self.width and 0 <= y < self.height):
            self.grid[y][x] = val

rg = Grid(4, 4)
rg.build_grid()
print(rg.get_cell(2,4))
rg.set_cell(2,3,0x0)
print(rg.get_cell(2,3))
print(rg.grid)
rg.renderer()