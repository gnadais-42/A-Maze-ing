*This project has been created as part of the 42 curriculum by gnadais- and pcoelho-.*

# Maze Generator

## Description

This project implements a maze generator based on graph theory principles. The maze is represented as a grid where each cell acts as a node in a graph, and connections between cells correspond to the absence of walls.

The goal of the project is to generate a valid maze (i.e., a connected, acyclic structure) and allow it to be explored or played. Internally, the maze is stored as a matrix of integers ranging from 0 to 15, where each bit encodes the presence or absence of a wall in a specific direction.

Bitwise encoding of walls:

* Least Significant Bit (LSB): North wall
* Second bit: East wall
* Third bit: South wall
* Fourth bit: West wall

This compact representation allows efficient storage and manipulation of maze structures.

## Instructions
### Prerequisites
Python 3 must be installed on your system
make must be available
Setup & Execution

The project uses a Makefile to fully automate environment setup and execution.
You do not need to manually install dependencies.

To install dependencies and run the project:

make run

This command will:

Create a virtual environment (venv/) if it does not exist
Install all required dependencies from:
requirements/requirements.txt
requirements/mlx-2.2-py3-none-any.whl
Execute the main script (main.py)

### Debug Mode

To run the project with the Python debugger:

make debug

### Cleaning the Project

To remove the virtual environment and all generated files:

make clean

### Linting

To check code quality:

make lint

For stricter checks:

make lint-strict

### Configuration

The project depends on a config.txt file located at the root of the repository.

This file contains all parameters required for the maze generation

You must ensure that config.txt is properly filled before running the program.

Example (structure)
WIDTH=15
HEIGHT=15
ENTRY=2,5
EXIT=14,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42

## Maze Representation

The maze is implemented as a 2D matrix of integers

Each cell contains a value between 0 and 15:

* Each bit represents whether a wall exists in a direction
* A bit set to `1` means the wall is present
* A bit set to `0` means the wall is open (connection to another cell)

Example:

* `0` → no walls (fully open cell)
* `15` → all walls present (isolated cell)

## Algorithm
### Perfect
The maze is generated using a tree-based algorithm.

Each cell is treated as a node in a graph. The generation process builds a spanning tree over the grid:

* Initially, all cells are disconnected (all walls present)
* Connections are progressively carved between neighboring cells
* Each connection removes a wall between two adjacent cells
* The process ensures there are no cycles and all cells are reachable

This results in a *perfect maze*:

* Exactly one path between any two cells
* No isolated sections
* No loops

### Imperfect

An Imperfect maze is one that has at least one cycle in it, making it so that there are at least two paths from point x to point y.
So to generate one we just build a perfect maze and "break" some walls so as to create cycles

## Why This Algorithm

This approach was chosen because:

* It guarantees a valid maze structure (connected and acyclic)
* It is efficient and relatively simple to implement
* It maps naturally to grid-based representations
* It allows easy control over randomness and maze complexity

Additionally, modeling the maze as a tree makes reasoning about correctness straightforward.

## Reusable Code

Several parts of the code are designed to be reusable:

* Grid/matrix handling utilities
* Bitwise wall encoding and decoding functions
* Graph traversal logic
* Maze generation core algorithm

These components can be reused in:

* Pathfinding projects
* Game development (grid-based maps)
* Procedural content generation

## Advanced Features

* Playable maze (user can navigate through the maze)
* Various color pallettes
* Various playable sprites
* Toggleable shortest path
* Configurable maze size

## Team & Project Management

### Roles

* gnadais-: Core algorithm implementation, gameplay, path finding
* pcoelho-: Input/output handling, parsing, display and documentation

### Planning & Evolution

Initially, the project focused on defining the data representation and basic maze generation. As development progressed:

* The algorithm was refined for correctness and efficiency
* A playable interface was added
* Code structure was improved for modularity

### What Worked Well

* Clear separation between generation logic and display
* Simple and efficient data representation
* Good collaboration on debugging and testing

### What Could Be Improved

* More extensive testing (edge cases, large mazes)
* Additional generation algorithms for comparison
* Better visualization tools

### Tools Used

* Git (version control)
* Makefile (build system)

## Resources

### References

* Graph theory fundamentals (spanning trees)
* Maze generation algorithms (DFS)
* Bitwise operations in Python

### AI Usage

AI tools were used to:

* Help structure the README file
* Suggest improvements in code organization


## Additional Notes

This project demonstrates how graph theory concepts can be applied to procedural generation and highlights the efficiency of bit-level data representation.
