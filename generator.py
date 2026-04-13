import random
from typing import List, Tuple

# Directions: N, E, S, W
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
OPPOSITE = {0: 2, 1: 3, 2: 0, 3: 1}


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: Tuple[int, int], exit: Tuple[int, int], seed: int | None = None):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.random = random.Random(seed)

        self.grid = [[0b1111 for _ in range(width)] for _ in range(height)]
        self.blocked = [[False for _ in range(width)] for _ in range(height)]

    def generate(self, perfect: bool = True) -> List[List[int]]:
        self._place_42_center()
        self._generate_perfect()

        if not perfect:
            self._add_cycles()

        return self.grid

    def _generate_perfect(self):
        visited = [[False] * self.width for _ in range(self.height)]

        start = self._random_unblocked_cell()
        stack = [start]
        visited[start[0]][start[1]] = True

        while stack:
            x, y = stack[-1]
            neighbors = []

            for d, (dx, dy) in enumerate(DIRS):
                nx, ny = x + dx, y + dy
                if self._in_bounds(nx, ny) and not visited[nx][ny] and not self.blocked[nx][ny]:
                    neighbors.append((d, nx, ny))

            if neighbors:
                d, nx, ny = self.random.choice(neighbors)
                self._remove_wall(x, y, d)
                self._remove_wall(nx, ny, OPPOSITE[d])
                visited[nx][ny] = True
                stack.append((nx, ny))
            else:
                stack.pop()

    def _add_cycles(self, attempts: int | None = None):
        if attempts is None:
            attempts = (self.width * self.height) // 10

        for _ in range(attempts):
            x, y = self._random_unblocked_cell()

            dirs = list(range(4))
            self.random.shuffle(dirs)

            for d in dirs:
                nx, ny = x + DIRS[d][0], y + DIRS[d][1]

                if self._in_bounds(nx, ny) and not self.blocked[nx][ny]:
                    if self._has_wall(x, y, d):
                        self._remove_wall(x, y, d)
                        self._remove_wall(nx, ny, OPPOSITE[d])
                        break

    def _place_42_center(self):
        if self.width < 6 or self.height < 5:
            return

        pattern = [
            [1, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 1],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 1],
        ]

        start_x = (self.height - 5) // 2
        start_y = (self.width - 6) // 2

        for i in range(5):
            for j in range(6):
                if pattern[i][j] == 1:
                    x, y = start_x + i, start_y + j
                    self.blocked[x][y] = True
                    self.grid[x][y] = 0b1111

    def _remove_wall(self, x: int, y: int, d: int):
        self.grid[x][y] &= ~(1 << d)

    def _has_wall(self, x: int, y: int, d: int) -> bool:
        return (self.grid[x][y] & (1 << d)) != 0

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.width

    def _random_unblocked_cell(self) -> Tuple[int, int]:
        while True:
            x = self.random.randrange(self.height)
            y = self.random.randrange(self.width)
            if not self.blocked[x][y]:
                return x, y
