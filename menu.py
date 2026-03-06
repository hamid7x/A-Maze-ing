class Menu:
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
                print("enter a valid number (1-4)")
                continue
            if (operation == 1):
                pass
            elif (operation == 2):
                pass
            elif (operation == 3):
                pass
            elif (operation == 4):
                break
            else:
                print("enter a valid number (1-4)")
r = Menu()
r.display_menu()