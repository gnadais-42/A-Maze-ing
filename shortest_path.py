from collections import deque
from typing import List, Tuple, Dict

DIRS = [
    (-1, 0, "N"),
    (0, 1, "E"),
    (1, 0, "S"),
    (0, -1, "W"),
]


def shortest_path(
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit: Tuple[int, int],
) -> str:
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

            if not (0 <= nx < height and 0 <= ny < width):
                continue

            if grid[x][y] & (1 << d):
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