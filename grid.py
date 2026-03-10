class Grid:

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = []

    def build_grid(self) -> None:
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(0xf)
            self.grid.append(row)
