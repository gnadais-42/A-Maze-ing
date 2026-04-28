*This project has been created as part of the 42 curriculum by gnadais- and pcoelho-.*

# Maze Generating module

## Description

This standalone module generates perfect or imperfect mazes  using DFS (Depth-First Search), and also calculates the shortest path between two points in said maze, using BFS (Breadth-First Search). 

The maze is represented by an integer matricx (list of lists), where each Maze tile is represented by an int between 0 and 15, which encondes the existence (or nonexistence) of walls around the tile.

## Instructions
### Prerequisites
Python 3 must be installed on your system


### Usage
from mazegen import MazeGenerator, shortest_path, print_maze

gen = MazeGenerator(width=10, height=10, entry=(9,9) , exit=(1,1), seed=None)

gen.generate(perfect=True)

path = shortest_path(grid = gen.grid, entry=(9,9), exit=(1,1))

print_maze(grid = gen.grid, entry=(9,9), exit=(1,1), path=path, player=None)

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

