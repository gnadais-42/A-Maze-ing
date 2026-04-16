from generator import MazeGenerator
from maze_printer import print_maze
from shortest_path import shortest_path
from parser import parser, valid_config
from typing import List


def count_edges(grid):
    """Uses Graph Theory, and by treating the Maze as a collection of vertices and edges,
    counts the edges in order to find, quickly, if the Maze is or isn't perfect.
    A perfect Maze is akin to a Graph Tree, where edges = vertices - 1 """
    h, w = len(grid), len(grid[0])
    edges = 0
    nodes = 0

    for i in range(h):
        for j in range(w):
            if grid[i][j] == 0b1111:
                continue

            nodes += 1

            for d in range(4):
                if not (grid[i][j] & (1 << d)):
                    edges += 1

    return nodes, edges // 2


def preset_test():
    gen = MazeGenerator(10, 10, entry=(1, 7), exit=(2, 0), seed=47)
    maze = gen.generate(perfect=True)
    path = shortest_path(maze, entry=(1, 7), exit=(2, 0))
    print_maze(maze, entry=(1, 7), exit=(2, 0), path=path)

    print(path)
    print(count_edges(maze))


def output(output_file: str, maze: List[List[int]], path: str,
           entry: tuple[int, int], exit: tuple[int, int]) -> None:

    with open(output_file, "w") as f:
        for line in maze:
            for digit in line:
                if digit > 9:
                    f.write(chr(ord('A') + digit - 10))
                else:
                    f.write(f"{digit}")
            f.write("\n")
        f.write("\n")
        f.write(f"{entry}\n")
        f.write(f"{exit}\n")
        f.write(f"{path}")


def config_file_test(filename: str):

    configs = valid_config(parser(filename))

    if not configs:
        print("Invalid configuration")
        return

    print(configs)
    gen = MazeGenerator(width=configs.width, height=configs.height,
                        entry=configs.entry, exit=configs.exit,
                        seed=configs.seed)

    maze = gen.generate(perfect=configs.perfect)
    path = shortest_path(maze, entry=configs.entry, exit=configs.exit)

    print_maze(maze, entry=configs.entry, exit=configs.exit, path=path)
    print(path)
    print(count_edges(maze))
    output(configs.output_file, maze, path, configs.entry, configs.exit)


config_file_test("config_test.txt")

# config_file_test("config_preset.txt")

# preset_test()
