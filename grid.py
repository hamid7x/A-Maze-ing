class Grid:
    """Represents a 2D grid with a specified width and height."""
    def __init__(self, width: int, height: int) -> None:
        """
            Initialize the Grid object.
            Args:
                width (int): Number of columns in the grid.
                height (int): Number of rows in the grid.
        """
        self.width: int = width
        self.height: int = height
        self.grid: list[list[int]] = []

    def build_grid(self) -> None:
        """
        Build a 2D grid initialized with the value 0xf.

        The method creates a grid with the specified height and width
        and fills each cell with the integer value 0xf.
        """
        for _ in range(self.height):
            row: list[int] = []
            for _ in range(self.width):
                row.append(0xf)
            self.grid.append(row)
