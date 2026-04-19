from generator import MazeGenerator
from typing import List, Tuple


DIRS = [
    (0, -1, "N"),
    (1, 0, "E"),
    (0, 1, "S"),
    (-1, 0, "W"),
]
DIR_LETTER_TO_IDX = {"N": 0, "E": 1, "S": 2, "W": 3}


class Player:
    def __init__(self, generator: MazeGenerator, coords: Tuple[int, int] | None = None) -> None:
        self.maze = generator
        self.coords = coords
        self.path = ""
        self.path_cells = set()

    def move(self, d: int) -> None:
        nx = self.coords[0] + DIRS[d][0]
        ny = self.coords[1] + DIRS[d][1]

        if (self.maze._has_wall(self.coords[0], self.coords[1], d)
            and self.maze._in_bounds(nx, ny)):
            self.coords = (nx, ny)
            self.path += DIRS[d]
            self.path_cells.add(self.coords)
