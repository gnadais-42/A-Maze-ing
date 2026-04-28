import random
from typing import List, Tuple


DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
OPPOSITE = {0: 2, 1: 3, 2: 0, 3: 1}


class MazeGenerator:
    """
    Maze Generator Class
    """
    def __init__(self, width: int, height: int, entry: Tuple[int, int],
                 exit: Tuple[int, int], seed: int | None = None):
        """
        Reusable generator able to make both perfect and imperfect mazes

        Attributes:

        width: (int) Determines the width of the maze
        height: (int) Determines the height of the maze
        entry: (tuple[int, int]) Starting point of the maze
        exit: (tuple[int, int]) End point of the maze
        random: (int | None) Controls the random aspect of
        the maze generation
        grid: (list[list[int]]) The actual maze structure
        as a matrix of ints
        blocked: (list[list[bool]]) Matrix of bools responsible
        for the 42 pattern
        cells_generated: (list[tuple[int,int]]) list containing the order
        in which the maze cells were generated
        """

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.random = random.Random(seed)

        self.grid = [[0b1111 for _ in range(width)] for _ in range(height)]
        self.blocked = [[False for _ in range(width)] for _ in range(height)]

        self.cells_generated: List[Tuple[int, int]] = []

        self._place_42_center()

    def generate(self, perfect: bool = True) -> List[List[int]]:
        """This function calls the generator functions for the perfect
        maze and then ,if needed, tweaks it to create an imperfect maze
        """
        self._generate_perfect()

        if not perfect:
            self._add_cycles()

        return self.grid

    def _generate_perfect(self) -> None:
        """
        Generates a Perfect Maze through a DFS implementation
        """

        row = [0b1111 for _ in range(self.width)]
        self.grid = [row[:] for _ in range(self.height)]
        self.grid_list = [[row.copy() for row in self.grid]]
        visited = [[False] * self.width for _ in range(self.height)]

        start = self._random_unblocked_cell()
        stack = [start]
        visited[start[1]][start[0]] = True
        self.cells_generated = [start]

        while stack:
            x, y = stack[-1]
            neighbors = []

            for d, (dx, dy) in enumerate(DIRS):
                nx, ny = x + dx, y + dy

                if (
                    self._in_bounds(nx, ny)
                    and not visited[ny][nx]
                    and not self.blocked[ny][nx]
                ):
                    neighbors.append((d, nx, ny))

            if neighbors:
                d, nx, ny = self.random.choice(neighbors)
                self._remove_wall(x, y, d)
                self._remove_wall(nx, ny, OPPOSITE[d])
                visited[ny][nx] = True
                stack.append((nx, ny))
                self.cells_generated.append((nx, ny))
            else:
                stack.pop()

    def _add_cycles(self, attempts: int | None = None) -> None:
        """
        Adds cycles in order to generate a false (non-perfect) Maze
        """
        if attempts is None:
            attempts = (self.width * self.height) // 10

        for _ in range(attempts):
            x, y = self._random_unblocked_cell()

            dirs = list(range(4))
            self.random.shuffle(dirs)

            for d in dirs:
                nx, ny = x + DIRS[d][0], y + DIRS[d][1]

                if self._in_bounds(nx, ny) and not self.blocked[ny][nx]:
                    if self._has_wall(x, y, d):
                        self._remove_wall(x, y, d)
                        self._remove_wall(nx, ny, OPPOSITE[d])
                        break

    def _place_42_center(self) -> None:
        """Places a 42 pattern at the center of the Maze,
        if the size allows it"""

        if self.height < 7 or self.width < 8:
            print("Maze Too small for 42 pattern")
            return

        pattern = [
            [1, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 1],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 1],
        ]

        start_x = (self.width - 6) // 2
        start_y = (self.height - 5) // 2

        for i in range(6):
            for j in range(5):
                if pattern[j][i] == 1:
                    x, y = start_x + i, start_y + j
                    self.blocked[y][x] = True
                    self.grid[y][x] = 0b1111

    def _remove_wall(self, x: int, y: int, d: int) -> None:
        """removes a cell's wall in a given direction"""
        self.grid[y][x] &= ~(1 << d)

    def _has_wall(self, x: int, y: int, d: int) -> bool:
        """checks that the cell has a wall in a given direction"""
        return (self.grid[y][x] & (1 << d)) != 0

    def _in_bounds(self, x: int, y: int) -> bool:
        """checks if the given cell is within the bounds of the maze"""
        return 0 <= x < self.width and 0 <= y < self.height

    def _random_unblocked_cell(self) -> Tuple[int, int]:
        """selects a random unblocked cell to use as a starting point"""
        while True:
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            if not self.blocked[y][x]:
                return x, y
