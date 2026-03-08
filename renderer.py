from grid import Grid
from config_parser import ConfigParser
from maze_generator import MazeGenerator


class Renderer:
    switch = True

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        self.entry = {}
        self.exit = {}
        self.path = ""
        self.draw_path = []
        self.wall_colors = [
            "\033[0m",
            "\033[31m",
            "\033[32m",
            "\033[33m",
            "\033[34m",
            "\033[35m",
            "\033[36m"
        ]
        self.path_colors = [
            "\033[43m",
            "\033[46m",
            "\033[44m",
            "\033[45m",
            "\033[41m",
            "\033[42m",
            "\033[47m"
        ]
        config = ConfigParser("config.txt")
        config.parsing_file()
        filename = config.get_val("OUTPUT_FILE")
        self.filename = filename
        self.path_index = 0
        self.wall_index = 0

    def get_info_from_file(self):
        self.grid = []
        with open(self.filename) as file:
            lines = file.readlines()
            for i in lines:
                row = []
                line = i.strip()
                if (not line):
                    break
                for c in line:
                    row.append(int(c, 16))
                self.grid.append(row)
            i = 0
            while (i < len(lines) and lines[i].strip()):
                i += 1
                continue
            data = []
            i += 1
            while (i < len(lines)):
                data.append(lines[i])
                i += 1
            entry_x, entry_y = data[0].split(",")
            self.entry = {"x": int(entry_x), "y": int(entry_y)}
            exit_x, exit_y = data[1].split(",")
            self.exit = {"x": int(exit_x), "y": int(exit_y)}
            self.path = data[2]

    def display_maze(self):
        reset = "\033[0m"
        wall_color = self.wall_colors[self.wall_index]
        path_color = self.path_colors[self.path_index]
        end_path_color = "\033[0m" + wall_color
        entry_color = self.wall_colors[self.wall_index + 1 % len(self.wall_colors)]
        exit_color = self.wall_colors[self.wall_index + 2 % len(self.wall_colors)]
        result = ""
        for h in range(self.height):
            top = "█"
            for w in range(self.width):
                direction = self.draw_path[h][w]
                is_path = self.switch and direction is not None
                if (self.grid[h][w] & 1):
                    top += "████"
                else:
                    prev_direc = self.draw_path[h - 1][w] if h > 0 else None
                    is_exist_above = (self.switch and h == self.exit["y"] and w == self.exit["x"] and prev_direc is not None)
                    if (is_path and direction == "N") or (self.switch and prev_direc == "S") or is_exist_above:
                        top += f"{path_color}   {end_path_color}█"
                    else:
                        top += "   █"
            result += wall_color + top + reset + "\n"
            midd = ""
            for w in range(self.width):
                direction = self.draw_path[h][w]
                is_path = self.switch and direction is not None
                is_entry = (h == self.entry["y"] and w == self.entry["x"])
                is_exit = (h == self.exit["y"] and w == self.exit["x"])
                if (self.grid[h][w] & 8):
                    midd += "█"
                else:
                    prv_w_dir = (self.draw_path[h][w - 1] if w > 0 else None)
                    is_exist_left = (self.switch and is_exit and prv_w_dir is not None)
                    if (is_path and direction == "W") or (self.switch and prv_w_dir == "E") or is_exist_left:
                        midd += f"{path_color} {end_path_color}"
                    else:
                        midd += " "
                if (is_path and not is_entry and not is_exit):
                    midd += f"{path_color}   {end_path_color}"
                elif (h == self.entry["y"] and w == self.entry["x"]):
                    midd += f"{entry_color}███{end_path_color}"
                elif (h == self.exit["y"] and w == self.exit["x"]):
                    midd += f"{exit_color}███{end_path_color}"
                else:
                    midd += "   "
            result += wall_color + midd + "█" + reset + "\n"
        bottom = "█"
        for w in range(self.width):
            if (self.grid[self.height - 1][w] & 4):
                bottom += "████"
            else:
                bottom += "   █"
        result += wall_color + bottom + reset + "\n"
        print(result)

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
                g = Grid(self.width, self.height)
                g.build_grid()
                self.grid = g.grid
                maze = MazeGenerator(self.grid)
                maze.dfs((self.entry["y"], self.entry["x"]))
                maze.write_output(self.filename, self.grid, self.entry, self.exit)
                maze.solve_maze()
                maze.write_output(self.filename, self.grid, self.entry, self.exit)
                self.get_info_from_file()
                self.show_hide_path()
                self.display_maze()
            elif (operation == 2):
                self.show_hide_path()
                self.switch = not self.switch
                self.display_maze()
            elif (operation == 3):
                self.wall_index = (self.wall_index + 1) % len(self.wall_colors)
                self.path_index = (self.path_index + 1) % len(self.path_colors)
                self.display_maze()
            elif (operation == 4):
                break
            else:
                print("enter a valid number (1-4)")

    def show_hide_path(self):
        self.draw_path = [[None] * self.width for _ in range(self.height)]
        x = self.entry["x"]
        y = self.entry["y"]
        for d in self.path.strip():
            self.draw_path[y][x] = d
            if d == "N":
                y -= 1
            elif d == "S":
                y += 1
            elif d == "W":
                x -= 1
            elif d == "E":
                x += 1

if __name__ == "__main__":
    r = Renderer(20, 15)
    gr = Grid(20, 15)
    gr.build_grid()
    g = MazeGenerator(gr.grid)
    g.dfs((0,0))
    g.write_output("maze.txt", gr.grid, {"x": 0, "y": 0}, {"x": 19, "y": 14})
    g.solve_maze()
    g.write_output("maze.txt", gr.grid, {"x": 0, "y": 0}, {"x": 19, "y": 14})
    r.get_info_from_file()
    r.show_hide_path()
    r.display_maze()
    r.display_menu()