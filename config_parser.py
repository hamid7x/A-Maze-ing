import sys


class ConfigParser:

    def __init__(self, filename: str):
        self.filename = filename
        self.file_data = {}

    def parsing_file(self):
        try:
            with open(self.filename, 'r') as file:
                for i in file:
                    line = i.strip()
                    if (not line or line[0] == "#"):
                        continue
                    lst = line.split("=")
                    if (len(lst) > 2 or "=" not in line):
                        print("invalid format in config file")
                        sys.exit(1)
                    self.file_data.update({lst[0]: lst[1]})
            constants = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                         "OUTPUT_FILE", "PERFECT"]
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
            self.convert_data()
            if (self.file_data["WIDTH"] < 0):
                print("WIDTH must be >= 0")
                sys.exit(1)
            if (self.file_data["HEIGHT"] < 0):
                print("HEIGHT must be >= 0")
                sys.exit(1)
            entry_x = self.file_data["ENTRY"]["x"]
            entry_y = self.file_data["ENTRY"]["y"]
            exit_x = self.file_data["EXIT"]["x"]
            exit_y = self.file_data["EXIT"]["y"]
            if (entry_x == exit_x and entry_y == exit_y):
                print("ENTRY and EXIT must be a different values")
                sys.exit(1)
        except FileNotFoundError:
            print("Error: file not found")
            sys.exit(1)

    def convert_data(self):
        for key, val in self.file_data.items():
            try:
                if (key == "WIDTH" or key == "HEIGHT"):
                    self.file_data.update({key: int(val)})
            except ValueError:
                print("width and height must be integers")
                sys.exit(1)
            if (key == "PERFECT"):
                if (val == "True"):
                    self.file_data[key] = True
                elif (val == "False"):
                    self.file_data[key] = False
                else:
                    print("PERFECT must be a boolean")
                    sys.exit(1)
            try:
                if (key == "ENTRY" or key == "EXIT"):
                    coord = val.split(",")
                    self.file_data.update(
                        {key: {"x": int(coord[0]), "y": int(coord[1])}})
                    width = self.file_data["WIDTH"]
                    height = self.file_data["HEIGHT"]
                    x = self.file_data[key]["x"]
                    y = self.file_data[key]["y"]
                    if not 0 <= x < width:
                        print(f"{key} coordinates out of range")
                        sys.exit(1)
                    if not 0 <= y < height:
                        print(f"{key} coordinates out of range")
                        sys.exit(1)
            except ValueError:
                print("coordinates must be integers")
                sys.exit(1)
    def get_val(self, k):
        for key, val in (self.file_data).items():
            if (key == k):
                return (val)
