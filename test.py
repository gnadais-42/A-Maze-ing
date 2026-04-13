from generator import MazeGenerator
from maze_printer import print_maze
from shortest_path import shortest_path

def count_edges(grid):
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

gen = MazeGenerator(10, 10, entry=(1, 7), exit=(2, 0), seed=47)
maze = gen.generate(perfect=True)
path = shortest_path(maze, entry=(1, 7), exit=(2, 0))

print_maze(maze, entry=(1, 7), exit=(2, 0), path=path)
print(path)

print (count_edges(maze))
