class Renderer:
    
    def __init__(self, grid, width, height):
        self.width = width
        self.height = height
        self.grid = grid

    def renderer(self):
        result = ""
        for h in range(self.height):
            top = "+"
            for w in range(self.width):
                if (self.grid[h][w] & 1):
                    top += "---+"
                else:
                    top += "   +"
            result += top + "\n"
            midd = ""
            for w in range(self.width):
                if (self.grid[h][w] & 8):
                    midd += "|   "
                else:
                    midd += "    "
            result += midd + "|" + "\n" 
        bottom = "+"
        for w in range(self.width):
            if (self.grid[self.height - 1][w] & 4):
                bottom += "---+"
            else:
                bottom += "   +"
        result += bottom + "\n"
        print(result)

