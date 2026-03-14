import sys
from config_parser import ConfigParser
from renderer import Renderer
from typing import cast, Optional

if __name__ == "__main__":
    size = len(sys.argv)
    if (size == 2):
        file_name: str = sys.argv[1]
        config_parser: ConfigParser = ConfigParser(file_name)
        config_parser.parsing_file()
        width = cast(int, config_parser.get_val("width"))
        height = cast(int, config_parser.get_val("height"))
        entry = cast(dict, config_parser.get_val("entry"))
        exit = cast(dict, config_parser.get_val("exit"))
        output_file = cast(str, config_parser.get_val("output_file"))
        perfect = cast(bool, config_parser.get_val("perfect"))
        pattern = cast(str, config_parser.get_val("pattern"))
        seed = cast(Optional[int], config_parser.get_val("seed"))
        render: Renderer = Renderer(
            width, height, entry, exit, output_file, perfect, pattern, seed)
        render.generate_maze()
        render.display_menu()
    elif (size > 2):
        print("one argument required")
    else:
        print("file name is required")
