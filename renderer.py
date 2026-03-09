from grid import Grid
from config_parser import ConfigParser
from maze_generator import MazeGenerator


class Renderer:
    switch = True

    def __init__(self, width, height) -> None:
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
            "\033[48;5;129m",
            "\033[48;5;202m",
            "\033[48;5;123m",
            "\033[48;5;214m",
            "\033[48;5;201m"
            "\033[48;5;82m",
        ]
        config = ConfigParser("config.txt")
        config.parsing_file()
        filename = config.get_val("OUTPUT_FILE")
        self.filename = filename
        self.path_index = 0
        self.wall_index = 0

    def get_info_from_file(self) -> None:
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

    def display_maze(self) -> None:
        reset = "\033[0m"
        wall_color = self.wall_colors[self.wall_index]
        path_color = self.path_colors[self.path_index]
        end_path_color = "\033[0m" + wall_color
        entry_color = self.wall_colors[(
            (self.wall_index + 2) % len(self.wall_colors))]
        exit_color = self.wall_colors[(
            (self.wall_index + 3) % len(self.wall_colors))]
        result = ""
        for h in range(self.height):
            top = "█"
            for w in range(self.width):
                direction = self.draw_path[h][w]
                is_path = self.switch and direction is not None
                if (self.grid[h][w] & 1):
                    top += "██"
                else:
                    prev_direc = self.draw_path[h - 1][w] if h > 0 else None
                    is_exist_above = (self.switch and h == self.exit["y"]
                                      and w == self.exit["x"]
                                      and prev_direc is not None)
                    if ((is_path and direction == "N")
                       or (self.switch and prev_direc == "S")
                       or is_exist_above):
                        top += f"{path_color} {end_path_color}█"
                    else:
                        top += " █"
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
                    is_exist_left = (self.switch and is_exit
                                     and prv_w_dir is not None)
                    if ((is_path and direction == "W")
                       or (self.switch and prv_w_dir == "E") or is_exist_left):
                        midd += f"{path_color} {end_path_color}"
                    else:
                        midd += " "
                if (is_path and not is_entry and not is_exit):
                    midd += f"{path_color} {end_path_color}"
                elif (is_entry):
                    midd += f"{entry_color}█{end_path_color}"
                elif (is_exit):
                    midd += f"{exit_color}█{end_path_color}"
                else:
                    midd += " "
            result += wall_color + midd + "█" + reset + "\n"
        bottom = "██" * self.width
        result += wall_color + bottom + "█" + reset + "\n"
        print(result)

    def display_menu(self) -> None:
        while True:
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate Maze colors")
            print("4. Quit")
            try:
                nb = input("Choice? (1-4): ")
                operation = int(nb)
            except ValueError:
                print(f"enter a valid number (1-4) ('{nb}' not a number)")
                continue
            except BaseException:
                print("\nProgram has been stopped")
                break
            if (operation == 1):
                g = Grid(self.width, self.height)
                g.build_grid()
                self.grid = g.grid
                maze = MazeGenerator(self.grid)
                maze.dfs((self.entry["y"], self.entry["x"]))
                maze.write_output(
                    self.filename, self.grid, self.entry, self.exit)
                maze.solve_maze()
                maze.write_output(
                    self.filename, self.grid, self.entry, self.exit)
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

    def show_hide_path(self) -> None:
        self.draw_path = [[None] * self.width for _ in range(self.height)]
        c = self.entry["x"]
        r = self.entry["y"]
        for d in self.path.strip():
            self.draw_path[r][c] = d
            if d == "N":
                r -= 1
            elif d == "S":
                r += 1
            elif d == "W":
                c -= 1
            elif d == "E":
                c += 1


if __name__ == "__main__":
    r = Renderer(3, 3)
    gr = Grid(3, 3)
    gr.build_grid()
    g = MazeGenerator(gr.grid)
    g.dfs((0, 0))
    g.write_output("maze.txt", gr.grid, {"x": 2, "y": 2}, {"x": 0, "y": 0})
    g.solve_maze()
    g.write_output("maze.txt", gr.grid, {"x": 2, "y": 2}, {"x": 0, "y": 0})
    r.get_info_from_file()
    r.show_hide_path()
    r.display_maze()
    r.display_menu()
