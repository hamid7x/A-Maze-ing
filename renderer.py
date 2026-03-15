from mazegen.maze_generator import MazeGenerator
from typing import Optional
import os
import time
import random


class Renderer:
    """
        Responsible for reading maze data, rendering it in the terminal,
        and providing a small interactive menu to regenerate the maze,
        toggle the solution path, and rotate colors.
    """
    switch: bool = True

    def __init__(
            self,
            width: int,
            height: int,
            entry: dict[str, int],
            exit: dict[str, int],
            filename: str,
            perfect: bool,
            pattern: str,
            seed: Optional[int]
            ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: list[list[int]] = []
        self.path: str = ""
        self.draw_path: list[list[str | None]] = []
        self.wall_colors: list[str] = [
            "\033[0m",
            "\033[31m",
            "\033[32m",
            "\033[33m",
            "\033[34m",
            "\033[35m",
            "\033[36m"
        ]
        self.some_cl: list[str] = [
            "\033[48;5;95m",
            "\033[48;5;214m",
            "\033[48;5;82m",
            "\033[48;5;201m",
        ]
        self.path_colors: list[str] = [
            "\033[48;5;279m",
            "\033[48;5;129m",
            "\033[48;5;123m",
            "\033[48;5;58m",
            "\033[48;5;202m",
            "\033[48;5;59m",
        ]
        self.filename: str = filename
        self.perfect: bool = perfect
        self.pattern = pattern or '42'
        self.seed: Optional[int] = seed
        self.has_config_seed = seed is not None
        self.path_index: int = 0
        self.wall_index: int = 0
        self.another_ind: int = 0
        self.animating: bool = False
        self.algorithm: str = "dfs"
        self.curr_cell: Optional[tuple[int, int]] = None
        self.animation_speed = 0.03

    def get_info_from_file(self) -> None:
        """
            Read maze data from the output file.

            The file contains:
            - The maze grid encoded in hexadecimal values.
            - The solution path as directions (N, S, E, W).
        """
        try:
            self.grid = []
            with open(self.filename) as file:
                lines: list = file.readlines()
                for i in lines:
                    row: list[int] = []
                    line: str = i.strip()
                    if (not line):
                        break
                    for c in line:
                        row.append(int(c, 16))
                    self.grid.append(row)
                i = 0
                while (i < len(lines) and lines[i].strip()):
                    i += 1
                    continue
                data: list[str] = []
                i += 1
                while (i < len(lines)):
                    data.append(lines[i])
                    i += 1
                self.path = data[2] if len(data) > 2 else ""
        except IsADirectoryError:
            print("Output file cannot be directory")
            exit(1)

    def display_maze(self) -> None:
        """
            Render the maze in the terminal.

            The maze is drawn using block characters and ANSI color codes.
            It optionally displays the solution path between the entry
            and exit cells depending on the `switch` flag.
        """
        os.system("clear")
        reset = "\033[0m"
        header = (f"  A-MAZE-ING  ◆  {self.width} x {self.height}"
                  f" ◆  Seed: {self.seed}  ")
        print(f"{'█' * len(header)}")
        print(header)
        print(f"{'█' * len(header)}")
        print()
        wall_color = self.wall_colors[self.wall_index]
        path_color = self.path_colors[self.path_index]
        end_path_color = "\033[0m" + wall_color
        entry_color = self.some_cl[(
            (self.another_ind + 1) % len(self.some_cl))]
        exit_color = self.some_cl[(
            (self.another_ind + 2) % len(self.some_cl))]
        color_42 = self.path_colors[(
            (self.path_index + 1) % len(self.path_colors))]
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
                is_current = (self.curr_cell == (h, w))
                if is_current and self.animating:
                    midd += f"\033[48;5;226m \033[0m{wall_color}"
                elif (is_path and not is_entry and not is_exit):
                    midd += f"{path_color} {end_path_color}"
                elif (is_entry):
                    midd += f"{entry_color} {end_path_color}"
                elif (is_exit):
                    midd += f"{exit_color} {end_path_color}"
                else:
                    if (not self.animating and self.grid[h][w] & 1
                            and self.grid[h][w] & 2
                            and self.grid[h][w] & 4 and self.grid[h][w] & 8):
                        midd += f"{color_42} {end_path_color}"
                    else:
                        midd += " "
            result += wall_color + midd + "█" + reset + "\n"
        bottom = "██" * self.width
        result += wall_color + bottom + "█" + reset + "\n"
        print(result)

    def generate_maze(self) -> None:
        """Generate maze without animation and display result."""

        self.draw_path = [[None] * self.width for _ in range(self.height)]
        if not self.has_config_seed:
            self.seed = None
        maze = MazeGenerator(
            self.width, self.height,
            self.entry, self.exit, self.perfect,
            self.pattern, self.seed
        )
        maze.generate(self.algorithm, self.filename)
        self.seed = maze.seed
        self.get_info_from_file()
        self.show_hide_path()
        self.display_maze()
        if maze.size_warning:
            print(maze.size_warning)

    def change_animation_speed(self) -> None:
        """Change animation speed."""
        print(f"Current speed {self.animation_speed}")
        print("Enter value bettween 0.0 (instant) and 1.0 (very slow)")
        try:
            speed = float(input('Speed: ').strip())
            if 0.0 <= speed <= 1.0:
                self.animation_speed = speed
                self.display_maze()
            else:
                self.display_maze()
                print("Speed must be between 0.0 and 1.0")
        except ValueError:
            self.display_maze()
            print('Speed must be a valid number between 0.0 and 1.0')
        except KeyboardInterrupt:
            print('\nProgram stoped by user')
            exit(1)

    def animate_generation(self) -> None:
        """Animate maze generation by redrawing after each wall break."""

        self.animating = True
        print("\033[?25l", end="", flush=True)
        try:
            self.draw_path = [[None] * self.width for _ in range(self.height)]
            if not self.has_config_seed:
                self.seed = random.randint(1, 99999)
            maze = MazeGenerator(
                self.width, self.height, self.entry,
                self.exit, self.perfect, self.pattern, self.seed
            )

            self.grid = maze.grid

            def callback(curr_row: int, curr_col: int) -> None:
                self.curr_cell = (curr_row, curr_col)
                self.display_maze()
                time.sleep(self.animation_speed)
            if self.algorithm == 'dfs':
                maze.dfs(callback=callback)
            else:
                maze.prim(callback=callback)
            maze.bfs()
            maze.write_output(self.filename)
            self.seed = maze.seed

            self.get_info_from_file()
            self.show_hide_path()
            self.animating = False
            self.animate_path()
            if maze.size_warning:
                print(maze.size_warning)
        except KeyboardInterrupt:
            print("\nProgram stopped by user")
            exit(1)
        finally:
            self.animating = False
            print("\033[?25h", end="", flush=True)

    def animate_path(self) -> None:
        """draw solution path step by step."""

        print("\033[?25l", end="", flush=True)
        try:
            self.draw_path = [[None] * self.width for _ in range(self.height)]
            c = self.entry["x"]
            r = self.entry["y"]
            for d in self.path.strip():
                self.draw_path[r][c] = d
                self.display_maze()
                time.sleep(self.animation_speed)
                if d == "N":
                    r -= 1
                elif d == "S":
                    r += 1
                elif d == "W":
                    c -= 1
                elif d == "E":
                    c += 1
        except KeyboardInterrupt:
            print('\nProgram stopped by user')
            exit(1)
        finally:
            print("\033[?25h", end="", flush=True)

    def change_pattern(self) -> None:
        """Change pattern, validate and regenerate maze."""

        try:
            new_pattern = input("Enter pattern: ").strip().upper()
            if not new_pattern.isalnum():
                self.display_maze()
                print("Pattern must contain only letters and numbers")
                return
            temp_maze = MazeGenerator(
                self.width, self.height,
                self.entry, self.exit,
                self.perfect, new_pattern, self.seed
            )
            temp_maze.pattern_grid = temp_maze.build_pattern()
            if temp_maze.validate_pattern_size():
                self.pattern = new_pattern
                self.generate_maze()
            else:
                self.display_maze()
                temp_maze.print_pattern_too_large(new_pattern)
        except KeyboardInterrupt:
            print('\nProgram stopped by user. Goodbye!')
            exit(1)

    def resize_width_and_height(self) -> None:
        """Resizing dimensions of maze, validate and regenerate maze."""

        while True:
            try:
                new_width = int(input('Enter new width: ').strip())
                new_height = int(input('Enter new height :').strip())
            except ValueError:
                print('Width and Height must be a number')
                continue
            except KeyboardInterrupt:
                print('\nProgram stopped by user')
                exit(1)
            if new_width <= 0 or new_height <= 0:
                print("Width and Height must be greater than 0")
                continue
            temp_maze = MazeGenerator(
                new_width, new_height,
                self.entry, self.exit, self.perfect,
                self.pattern, self.seed
            )
            temp_maze.pattern_grid = temp_maze.build_pattern()
            if temp_maze.validate_pattern_size():
                self.width = new_width
                self.height = new_height
                self.entry = {'x': 0, 'y': 0}
                self.exit = {'x': self.width - 1, 'y': self.height - 1}
                self.generate_maze()
                return
            else:
                self.display_maze()
                temp_maze.print_pattern_too_large(self.pattern)
                return

    def display_menu(self) -> None:
        """
            Display the interactive command menu.

            The menu allows the user to:
            1. Generate a new maze.
            2. Show or hide the solution path.
            3. Rotate maze colors.
            4. Show Path with animation
            5. Switch algorithm (DFS/PRIM)
            6. Change Pattern (Default 42)
            7. Resize Maze Width/Height.
            8. Quit the program.
            User input is validated to ensure a correct option is selected.
        """
        while True:
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate Maze colors")
            print("4. Show Path with animation")
            print(f"5. Switch algorithm(DFS/PRIM)"
                  f"(current: {self.algorithm.upper()})")
            print("6. Change Pattern (Default 42)")
            print("7. Resize Maze Width/Height")
            print("8. Change animation speed")
            print("9. Quit")
            try:
                nb = input("Choice? (1-8): ")
                operation = int(nb)
            except ValueError:
                self.display_maze()
                print(f"enter a valid number (1-8) ('{nb}' not a number)")
                continue
            except KeyboardInterrupt:
                print("\nProgram stopped by user")
                break
            if (operation == 1):
                self.animate_generation()
            elif operation == 2:
                self.show_hide_path()
                self.switch = not self.switch
                self.display_maze()
            elif operation == 3:
                self.wall_index = (self.wall_index + 1) % len(self.wall_colors)
                self.path_index = (self.path_index + 1) % len(self.path_colors)
                self.another_ind = (self.another_ind + 1) % len(self.some_cl)
                self.display_maze()
            elif (operation == 4):
                self.animate_path()
            elif operation == 5:
                self.algorithm = "prim" if self.algorithm == "dfs" else "dfs"
                self.display_maze()
                print(f"Algorithm switched to {self.algorithm.upper()}")
            elif operation == 6:
                self.change_pattern()
            elif operation == 7:
                self.resize_width_and_height()
            elif operation == 8:
                self.change_animation_speed()
            elif (operation == 9):
                print("Goodbye!")
                break
            else:
                self.display_maze()
                print("enter a valid number (1-8)")

    def show_hide_path(self) -> None:
        """
            Build the path visualization grid.
            This method converts the stored path string (N, S, E, W)
            into a 2D structure (`draw_path`) that indicates the direction
            of movement for each cell along the solution path.
        """
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
