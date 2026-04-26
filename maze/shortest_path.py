from collections import deque
from typing import List, Tuple, Dict

DIRS = [
    (0, -1, "N"),
    (1, 0, "E"),
    (0, 1, "S"),
    (-1, 0, "W"),
]


def shortest_path(
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit: Tuple[int, int],
) -> str:
    """
    Computes the shortest path between the entry and exit point.
    It uses Breadth-first search (BFS) to find the shortest path
    For a Perfect maze, there is really just 1 option

    grid is the Maze's matrix

    entry and exit are tuples representing the exit and entry cell coordenates
    queue holds an ordered queue of points to 'investigate'
    visited stores all visited points

    parent is a dictionary where the keys are coordinates for a cell
    and the values are tuples containing the cell it came from
    and the direction it came from.

    parent allows us to in the end reconstruct the path from exit to entry
    by following in reverse the "child:parent" pairs in parent
    """

    height = len(grid)
    width = len(grid[0])

    queue = deque([entry])
    visited = set([entry])
    parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}

    while queue:
        x, y = queue.popleft()

        if (x, y) == exit:
            break

        for d, (dx, dy, letter) in enumerate(DIRS):
            nx, ny = x + dx, y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if grid[y][x] & (1 << d):
                continue

            if (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = ((x, y), letter)
                queue.append((nx, ny))

    path = []
    current = exit

    while current != entry:
        if current not in parent:
            return ""

        prev, move = parent[current]
        path.append(move)
        current = prev

    return "".join(reversed(path))
