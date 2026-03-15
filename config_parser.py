import sys
from typing import Any


class ConfigParser:

    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.file_data: dict[str, Any] = {}

    def parsing_file(self) -> None:
        try:
            with open(self.filename, 'r') as file:
                for i in file:
                    line = i.strip().lower()
                    if (not line or line[0] == "#"):
                        continue
                    lst = [i.strip() for i in line.split("=", 1)]
                    if (len(lst) != 2 or line.startswith("=")):
                        print("Error: invalid format in config file")
                        sys.exit(1)
                    constants = ["width", "height", "entry", "exit",
                                 "output_file", "perfect", "seed", "pattern"]
                    if (lst[0] not in constants):
                        print("Error: invalid key added!")
                        sys.exit(1)
                    if (lst[0] in self.file_data):
                        print("Error: Deplicate key!")
                        sys.exit(1)
                    self.file_data.update({lst[0]: lst[1]})
            constants = ["width", "height", "entry", "exit",
                         "output_file", "perfect"]
            unknown = []
            p = False
            for i in constants:
                is_found = i in self.file_data
                if (not is_found):
                    unknown.append(i)
                    p = True
            if (p):
                sep = ", "
                print(f"'{sep.join(unknown)}' not found in config file")
                sys.exit(1)
            self.is_valid_data()
            if (self.file_data["width"] < 0):
                print("Error: width must be >= 0")
                sys.exit(1)
            if (self.file_data["height"] < 0):
                print("Error: height must be >= 0")
                sys.exit(1)
            entry_x = self.file_data["entry"]["x"]
            entry_y = self.file_data["entry"]["y"]
            exit_x = self.file_data["exit"]["x"]
            exit_y = self.file_data["exit"]["y"]
            if (entry_x == exit_x and entry_y == exit_y):
                print("Error: entry and exit must be a different values")
                sys.exit(1)
        except FileNotFoundError:
            print("Error: file not found")
            sys.exit(1)
        except IsADirectoryError:
            print("Output file cannot be dirctory")
            sys.exit(1)
        except Exception as err:
            print(err)
            sys.exit(1)

    def is_valid_data(self) -> None:
        for key, val in self.file_data.items():
            try:
                if (key == "width"):
                    if (val == ""):
                        print("Error: width cannot be empty")
                        sys.exit(1)
                    self.file_data.update({key: int(val)})
            except ValueError:
                print("Error: width must be integer")
                sys.exit(1)
            try:
                if (key == "height"):
                    if (val == ""):
                        print("Error: height cannot be empty")
                        sys.exit(1)
                    self.file_data.update({key: int(val)})
            except ValueError:
                print("Error: height must be integer")
                sys.exit(1)
        for key, val in self.file_data.items():
            if (key == "output_file"):
                if (val == ""):
                    print("Error: file name cannot be empty")
                    sys.exit(1)
            if (key == "perfect"):
                if (val == "true" or val == "1"):
                    self.file_data[key] = True
                elif (val == "false" or val == "0"):
                    self.file_data[key] = False
                else:
                    print("Error: perfect must be a boolean")
                    sys.exit(1)
            try:
                if (key == "entry" or key == "exit"):
                    coord = val.split(",")
                    if (len(coord) == 1):
                        print("Error: coordinates must "
                              "be tow integer ex (1,1)")
                        sys.exit(1)
                    if (len(coord) > 2):
                        print("Error: coordinates must be",
                              "just tow integers ex (1,1)")
                        sys.exit(1)
                    self.file_data.update(
                        {key: {"x": int(coord[0]), "y": int(coord[1])}})
                    width = self.file_data["width"]
                    height = self.file_data["height"]
                    x = self.file_data[key]["x"]
                    y = self.file_data[key]["y"]
                    if not 0 <= x < width:
                        print(f"Error: {key} coordinates out of range")
                        sys.exit(1)
                    if not 0 <= y < height:
                        print(f"Error: {key} coordinates out of range")
                        sys.exit(1)
            except ValueError:
                print(f"Error: {key} coordinates must be integers")
                sys.exit(1)
            try:
                if (key == "seed"):
                    self.file_data.update({key: int(val)})
            except ValueError:
                self.file_data.update({key: None})
            if (key == "pattern" and val == ""):
                self.file_data.update({key: None})

    def get_val(self, k: str) -> int | str | dict[str, int] | None:
        return self.file_data.get(k)
