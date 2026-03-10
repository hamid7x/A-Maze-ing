import sys
from grid import Grid
from config_parser import ConfigParser
from maze_generator import MazeGenerator
from renderer import Renderer

if __name__ == "__main__":
    size = len(sys.argv)
    if (size == 2):
        file_name = sys.argv[1]
        config_parser = ConfigParser(file_name)
        config_parser.parsing_file()
        width = config_parser.get_val("width")
        height = config_parser.get_val("height")
        entry = config_parser.get_val("entry")
        exit = config_parser.get_val("exit")
        output_file = config_parser.get_val("output_file")
        grid = Grid(width, height)
        grid.build_grid()
        maze_generator = MazeGenerator(grid.grid)
        maze_generator.dfs((0, 0))
        maze_generator.write_output(
            output_file, grid.grid, entry, exit)
        maze_generator.solve_maze()
        maze_generator.write_output(
            output_file, grid.grid, entry, exit)
        render = Renderer(width, height)
        render.get_info_from_file()
        render.show_hide_path()
        render.display_maze()
        render.display_menu()
    elif (size > 2):
        print("one argument required")
    else:
        print("file name is required")
