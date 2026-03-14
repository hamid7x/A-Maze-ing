*This project has been created as part of the 42 curriculum by houkaamo, aoukaamo.*

# A-Maze-ing

## Description

A-Maze-ing is a terminal-based maze generator and solver written in Python 3.10+. The program reads a configuration file to set up maze parameters, generates a maze using either a Depth-First Search (DFS) or Prim's algorithm, embeds a visual pattern (default: "42") in the center of the maze, solves it using BFS, and renders it in the terminal with ANSI colors and block characters.

The project also provides a reusable Python package `mazegen` that exposes the `MazeGenerator` class for use in any Python project.

**Key features:**
- Maze generation with DFS (recursive backtracker) or Prim's algorithm
- Embedded text pattern in the maze center (default "42", or any alphanumeric string)
- BFS pathfinding to find the shortest solution
- Perfect or imperfect maze modes (with or without loops)
- Reproducible mazes via seed
- Animated generation and path rendering in the terminal
- Interactive menu to regenerate, change colors, switch algorithms, resize, and more
- Reusable `mazegen` package installable via pip

---

## Instructions

### Requirements

- Python 3.10 or later
- pip
- virtualenv (installed automatically via `make install`)

### Setup and Run

```bash
# Step 1 — Build the package
make build

# Step 2 — Install dependencies in a virtualenv
make install

# Step 3 — Run the program
make run
```

### Other Commands

```bash
make debug        # Run in debug mode with pdb
make lint         # Run flake8 and mypy checks
make lint-strict  # Run mypy with --strict flag
make clean        # Remove __pycache__, .mypy_cache, build artifacts
make clean-venv   # Remove the virtual environment
```

### Configuration File

The program requires a configuration file as its only argument:

```bash
python3 a_maze_ing.py config.txt
```

**Config file format** (key=value, case-insensitive):

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=12345
PATTERN=42
```

| Key         | Type    | Required | Description                                      |
|-------------|---------|----------|--------------------------------------------------|
| WIDTH       | int     | Yes      | Number of columns in the maze (> 0)             |
| HEIGHT      | int     | Yes      | Number of rows in the maze (> 0)                |
| ENTRY       | x,y     | Yes      | Entry cell coordinates                          |
| EXIT        | x,y     | Yes      | Exit cell coordinates                           |
| OUTPUT_FILE | string  | Yes      | Path to the output file                         |
| PERFECT     | bool    | Yes      | True = no loops, False = imperfect maze         |
| SEED        | int     | No       | Random seed for reproducibility                 |
| PATTERN     | string  | No       | Alphanumeric pattern to embed (default: 42)     |

Lines starting with `#` are treated as comments and ignored.

---

## Maze Generation Algorithm

### Primary: Depth-First Search (DFS) — Recursive Backtracker

The DFS algorithm works as follows:
1. Start from a random unmasked, non-hollow cell
2. Mark it as visited and push it to a stack
3. Randomly pick an unvisited neighbor, break the wall, and move to it
4. If no unvisited neighbors exist, backtrack by popping the stack
5. Repeat until the stack is empty

**Why DFS?**
- Produces long, winding corridors — visually interesting and challenging mazes
- Simple to implement iteratively with a stack
- Guarantees all reachable cells are visited (perfect maze property)
- Works naturally around masked pattern cells

### Secondary: Prim's Algorithm

Available as an alternative via the interactive menu (option 5). Prim's picks randomly from a frontier list, producing mazes with more branches and shorter dead ends — a different aesthetic from DFS.

---

## Reusable Module

The `mazegen` package exposes the `MazeGenerator` class for use in any Python project.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or rebuild from source and install:

```bash
python3 -m build --no-isolation
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Basic Usage

```python
from mazegen.maze_generator import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry={'x': 0, 'y': 0},
    exit={'x': 19, 'y': 14},
    perfect=True,
    pattern='42',
    seed=12345
)

# Generate maze and solve it, write output to file
maze.generate(algorithm='dfs', output_file='maze.txt')

# Access maze structure
print(maze.grid)           # 2D list of integers (bitmask walls)
print(maze.solution_path)  # List of directions ['N', 'S', 'E', 'W']
print(maze.seed)           # Seed used (useful if not specified)
```

### Custom Parameters

```python
# Use Prim's algorithm
maze.generate(algorithm='prim', output_file='output.txt')

# Use a custom pattern
maze = MazeGenerator(
    width=30, height=20,
    entry={'x': 0, 'y': 0},
    exit={'x': 29, 'y': 19},
    perfect=False,
    pattern='HELLO',
    seed=None  # Random seed
)
maze.generate()
```

### Grid Format

`maze.grid` is a 2D list of integers where each cell encodes its walls as a 4-bit bitmask:

| Bit | Value | Wall  |
|-----|-------|-------|
| 0   | 1     | North |
| 1   | 2     | South |
| 2   | 4     | East  |
| 3   | 8     | West  |

A cell with value `15` (all bits set) has all walls intact. A cell with value `0` has no walls.

### Accessing the Solution

```python
maze.bfs()  # Run BFS separately if needed
path = maze.solution_path  # e.g. ['E', 'E', 'S', 'S', 'E']
```

---

## Team and Project Management

### Team Members

| Member       | Role                                                                 |
|--------------|----------------------------------------------------------------------|
| houkaamo     | Maze generation algorithms (DFS, Prim), BFS pathfinding, pattern embedding, hollow cells, package structure |
| aoukaamo  | Terminal renderer, animation system, config parser, interactive menu, project packaging |

### Planning

**Initial plan:**
- Week 1: Config parser, basic maze generation (DFS), algorithm solver (BFS), terminal rendering, interactive menu
- Week 2: Prim's algorithm, pattern embedding, animation, packaging, README

**How it evolved:**
The pattern embedding took significantly longer than expected due to hollow cell handling and the mask system. Animation and the interactive menu also required several iterations to fix edge cases (nested loops, grid sync issues). Packaging was added at the end and required refactoring imports and restructuring the codebase.

### What Worked Well

- The bitmask grid representation made wall operations clean and efficient
- The callback system for animation kept DFS/Prim decoupled from the renderer
- Using `seed` made debugging reproducible — we could replay exact mazes
- Separating `MazeGenerator` from `Renderer` made the reusable package straightforward

### What Could Be Improved

- The hollow cell system is hardcoded — a more generic approach would be better
- Animation speed could be configurable via the menu
- More algorithms (Kruskal's, Wilson's) could be added

### Tools Used

- **Python 3.10** — main language
- **flake8** — code style linting
- **mypy** — static type checking
- **setuptools + build** — packaging
- **pdb** — debugging
- **Git** — version control
---

## Resources

- [mazes for programmers — Jamis Buck's book](http://mazesforprogrammers.com/)
- [Recursive backtracker (DFS) — Jamis Buck's blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Prim's algorithm for mazes — Jamis Buck's blog](http://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)
- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [BFS pathfinding — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [ANSI escape codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)


### AI Usage

Claude (Anthropic) was used as a development assistant throughout this project.
Specifically for:
- help understand concepts
- make architectural decisions
- and improve the overall structure of the code