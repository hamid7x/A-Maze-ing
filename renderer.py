from grid import Grid

class Renderer:
    
    def __init__(self, grid, width, height):
        self.width = width
        self.height = height
        self.grid = grid
        self.colors = [
            "\033[31m",
            "\033[32m",
            "\033[33m",
            "\033[34m",
            "\033[35m",
            "\033[36m"
        ]
        self.index = 0
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
        print(self.colors[self.index] + result + "\033[0m")

    def display_menu(self):
        while True:
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate Maze colors")
            print("4. Quit")
            nb = input("Choice? (1-4): ")
            try:
                operation = int(nb)
            except ValueError:
                print(f"enter a valid number (1-4) ('{nb}' not a number)")
                continue
            if (operation == 1):
                pass
            elif (operation == 2):
                pass
            elif (operation == 3):
                self.renderer()
                self.index = (self.index + 1) % len(self.colors)
            elif (operation == 4):
                break
            else:
                print("enter a valid number (1-4)")
if __name__ == "__main__":
    r = Grid(4, 4)
    r.build_grid()
    r = Renderer(r.grid,4 , 4)
    r.display_menu()