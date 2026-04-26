from typing import List, Tuple, Set
from .player import Player

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
DIR_LETTER_TO_IDX = {"N": 0, "E": 1, "S": 2, "W": 3}


def path_to_cells(entry: Tuple[int, int], path: str) -> Set[Tuple[int, int]]:
    """Takes a point and a path in a string format
    (eg. WWWENS, where letters represent directions)
    And returns all the coordinates/points along that path"""
    cells: Set[Tuple[int, int]] = set()
    r, c = entry
    cells.add((r, c))
    for ch in path:
        d = DIR_LETTER_TO_IDX[ch]
        dr, dc = DIRS[d]
        r, c = r + dr, c + dc
        cells.add((r, c))
    return cells


def print_maze(
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit: Tuple[int, int],
    path: str | None = None,
    player: Player | None = None
) -> None:

    """Prints the maze using ASCII characters,
    placing a green zero on the entry point cell,
    a red zero on the exit point cell and blue zeros
    on the cells composed by the shortest path between
    the entry point and the exit point (if it exists)"""

    height = len(grid)
    width = len(grid[0]) if height else 0

    green = "\033[92m"
    red = "\033[91m"
    blue = "\033[94m"
    yellow = "\033[93m"
    reset = "\033[0m"

    path_cells: Set[Tuple[int, int]] = set()
    if path:
        path_cells = path_to_cells(entry, path)
    player_coords = (-1, -1)
    if player is not None:
        player_coords = player.coords

    print("+" + "---+" * width)

    for i in range(height):
        row_top = "|"
        row_bottom = "+"

        for j in range(width):
            cell = grid[i][j]

            if (j, i) == entry:
                content = f" {green}0{reset} "
            elif (j, i) == exit:
                content = f" {red}0{reset} "
            elif (j, i) in path_cells and cell != 0b1111:
                content = f" {blue}0{reset} "
            elif cell == 0b1111:
                content = "###"
            else:
                content = "   "
            if (j, i) == player_coords:
                content = f" {red if player.wrong_turn else yellow}P{reset} "

            row_top += content

            if cell & (1 << 1):
                row_top += "|"
            else:
                row_top += " "

            if cell & (1 << 2):
                row_bottom += "---+"
            else:
                row_bottom += "   +"

        print(row_top)
        print(row_bottom)
