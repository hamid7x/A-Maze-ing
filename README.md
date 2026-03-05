*This project has been created as part of the 42 curriculum by hamid, abdo.*

# 🌀 A-Maze-ing

A Python maze generator and terminal visualizer. Generates perfect or imperfect mazes from a config file, renders them with extended ASCII art, and finds the shortest path from entry to exit.

---

## Description

A-Maze-ing generates random mazes using **DFS (Recursive Backtracker)** or **Prim's Algorithm**. Each maze is encoded in a hexadecimal wall format and displayed interactively in the terminal. A hidden **"42" pattern** is embedded in every maze using fully-closed cells.

---

## Instructions

### Requirements

```
Python 3.10+
pip
```

### Install

```bash
git clone https://github.com/hamid7x/A-Maze-ing.git
cd A-Maze-ing
make install
```

### Run

```bash
make run
# or directly:
python3 a_maze_ing.py config.txt
```

### Other commands

```bash
make lint        # run flake8 + mypy
make debug       # run with pdb debugger
make clean       # remove __pycache__ and temp files
```

---

## Configuration File

The config file uses `KEY=VALUE` pairs. Lines starting with `#` are comments.

| Key           | Description                     | Example                |
|---------------|---------------------------------|------------------------|
| `WIDTH`       | Maze width in cells             | `WIDTH=20`             |
| `HEIGHT`      | Maze height in cells            | `HEIGHT=15`            |
| `ENTRY`       | Entry coordinates (x,y)         | `ENTRY=0,0`            |
| `EXIT`        | Exit coordinates (x,y)          | `EXIT=19,14`           |
| `OUTPUT_FILE` | Output filename                 | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | One path between entry and exit | `PERFECT=True`         |
| `SEED`        | Reproducibility seed            | `SEED=42`              |
| `ALGORITHM`   | `dfs` or `prim`                 | `ALGORITHM=dfs`        |

---

## Algorithm

We use **DFS Recursive Backtracker** as the default algorithm.

It starts from the entry cell, carves passages by visiting unvisited neighbours randomly, and backtracks when stuck. This guarantees every cell is visited and produces a perfect maze with long winding corridors.

**Why DFS?** It's intuitive, produces visually interesting mazes, and guarantees full connectivity by construction.

**Prim's algorithm** is also supported via `ALGORITHM=prim`. It grows the maze from a seed cell using a random frontier list, producing mazes with more branching.

---

## Project Structure

```
A-Maze-ing/
├── a_maze_ing.py        ← main entry point
├── config_parser.py     ← reads and validates config.txt
├── grid.py              ← builds the initial full closed grid
├── renderer.py          ← terminal ASCII renderer + interactive menu
├── maze_generator.py    ← DFS, BFS, 42 pattern, output writer
├── config.txt           ← default configuration
├── Makefile
├── pyproject.toml       ← pip packaging
└── tests/
    ├── test_generator.py
    └── test_config_parser.py
```

---

## Code Architecture

### How everything connects

```python
from config_parser import ConfigParser
from grid import Grid
from maze_generator import MazeGenerator
from renderer import Renderer

# abdo — reads config
config = ConfigParser("config.txt")
config.parse()

# abdo — builds full closed grid (all cells = 0xF)
grid = Grid(config.get("WIDTH"), config.get("HEIGHT"))
grid.build()

# hamid — receives grid, carves maze, finds path, writes output
gen = MazeGenerator(grid.cells, config.get("ENTRY"), config.get("EXIT"), seed=42)
gen.generate()
gen.solve()
gen.embed_42()
gen.write_output(config.get("OUTPUT_FILE"))

# abdo — renders the result
renderer = Renderer(grid.cells, config.get("ENTRY"), config.get("EXIT"))
renderer.solution = gen.solution
renderer.render_loop(gen)
```

---

## Class Reference

### `MazeGenerator` — hamid (`maze_generator.py`)

```python
class MazeGenerator:
    def __init__(self, grid, entry, exit, seed=None, algorithm="dfs"):
        self.grid      = grid      # 2D list[list[int]] — modified in place
        self.entry     = entry     # (x, y)
        self.exit      = exit      # (x, y)
        self.seed      = seed      # int or None
        self.algorithm = algorithm # "dfs" or "prim"
        self.solution  = []        # list of "N"/"E"/"S"/"W" steps

    def generate(self)              # runs DFS or Prim to carve the maze
    def _dfs(self)                  # private — iterative DFS backtracker
    def _break_wall(self, x, y, d)  # private — removes wall between two cells
    def _get_neighbours(self, x, y, visited)  # private — unvisited neighbours
    def solve(self)                 # runs BFS to find shortest path
    def _bfs(self)                  # private — BFS pathfinder
    def embed_42(self)              # places "42" pattern into the grid
    def write_output(self, filepath)# writes hex maze output file
```

### `ConfigParser` — abdo (`config_parser.py`)

```python
class ConfigParser:
    def __init__(self, filepath)  # path to config.txt
    def parse(self)               # reads file, fills self.config dict
    def _validate(self)           # private — checks all required keys
    def get(self, key)            # returns value for a given key
```

### `Grid` — abdo (`grid.py`)

```python
class Grid:
    def __init__(self, width, height)
    def build(self)               # creates grid — all cells = 0xF
    def get_cell(self, x, y)      # returns bitmask at (x, y)
    def set_cell(self, x, y, val) # sets bitmask at (x, y)
```

### `Renderer` — abdo (`renderer.py`)

```python
class Renderer:
    def __init__(self, grid, entry, exit)
    def render(self)              # prints maze to terminal
    def render_loop(self, gen)    # interactive menu loop
    def _draw_cell(self, x, y)   # private — draws one cell from bitmask
    def toggle_path(self)         # show/hide solution path
    def change_colour(self)       # cycle through wall colours
```

---

## Reusable Module

The maze generation logic is packaged as a standalone pip-installable module.

### Install

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Usage

```python
from mazegen import MazeGenerator

gen = MazeGenerator(grid, entry=(0,0), exit=(19,14), seed=42, algorithm="dfs")
gen.generate()
gen.solve()

print(gen.grid)      # list[list[int]] — wall bitmask per cell
print(gen.solution)  # ["S", "S", "E", "E", ...]
print(gen.entry)     # (0, 0)
print(gen.exit)      # (19, 14)
```

### Wall encoding

| Bit | Wall  | Value |
|-----|-------|-------|
| 0   | North | 1     |
| 1   | East  | 2     |
| 2   | South | 4     |
| 3   | West  | 8     |

`0xF` = all 4 walls present. `0x0` = no walls.

---

## Team & Project Management

### Roles

| Member  | Responsibilities                                              |
|---------|---------------------------------------------------------------|
| `hamid` | `MazeGenerator` class — DFS, Prim, BFS solver, 42 pattern, hex output file, pip package |
| `abdo`  | `ConfigParser`, `Grid`, `Renderer` — ASCII display, interactive menu, main entry point |

### The handoff contract

```
abdo  provides → grid.cells       list[list[int]] (all 0xF)
hamid receives → grid.cells       modifies it in place
hamid provides → gen.solution     list of N/E/S/W steps
abdo  reads    → gen.solution     to display the path overlay
```

### Planning

| Week | hamid | abdo |
|------|-------|------|
| 1 | DFS generator + `_break_wall()` | Config parser + grid init |
| 2 | BFS solver + wall coherence fixes | ASCII renderer |
| 3 | Prim's algorithm + 42 pattern | Interactive menu + colour |
| 4 | Hex output file + pip package | Main entry point wiring + tests |

### What worked well
- Clean class separation made both parts independently testable
- Agreeing on the `grid.cells` interface early meant no integration surprises
- Using a seed from the start made debugging much easier

### What could be improved
- The "42" pattern placement was trickier than expected
- More unit tests earlier would have caught wall coherence bugs sooner

### Tools used
- VS Code for development
- Claude (AI) — used to discuss algorithm design, wall encoding logic,
  renderer architecture, and README structure. All generated content
  was reviewed, tested, and fully understood before inclusion.
- `pytest` for unit testing
- `mypy` + `flake8` for static analysis

---

## Resources

- [Maze generation algorithms — Jamis Buck](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [Maze generation — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Python typing module](https://docs.python.org/3/library/typing.html)
- [PEP 257 — Docstrings](https://peps.python.org/pep-0257/)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [flake8 docs](https://flake8.pycqa.org/)
- [mypy docs](https://mypy.readthedocs.io/)