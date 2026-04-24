from .generator import MazeGenerator
from typing import Tuple


DIRS = [
    (0, -1, "N"),
    (1, 0, "E"),
    (0, 1, "S"),
    (-1, 0, "W"),
]
DIR_LETTER_TO_IDX = {"N": 0, "E": 1, "S": 2, "W": 3}


class Player:
    def __init__(self, generator: MazeGenerator,
                 coords: Tuple[int, int] | None = None) -> None:

        self.start = coords
        self.maze = generator
        self.coords = coords
        self.path = ""
        self.path_cells = set([coords])
        self.wrong_turn = False
        self.lock = False

    def move(self, d: int | None) -> None:
        if d is None or self.lock:
            return

        nx = self.coords[0] + DIRS[d][0]
        ny = self.coords[1] + DIRS[d][1]

        print(nx, ny)

        if (not self.maze._has_wall(self.coords[0], self.coords[1], d)
                and self.maze._in_bounds(nx, ny)):

            self.coords = (nx, ny)
            self.path += DIRS[d][2]
            self.path_cells.add(self.coords)
        else:
            self.wrong_turn = True

        if self.coords == self.maze.exit:
            self.lock = True

    def correct_turn(self):
        self.wrong_turn = False

    def reset(self):
        self.path = ""
        self.path_cells = set([self.start])
        self.wrong_turn = False
        self.coords = self.start
        self.lock = False
