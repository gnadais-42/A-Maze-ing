from typing import List, Tuple, Iterable, Set

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIR_LETTER_TO_IDX = {"N": 0, "E": 1, "S": 2, "W": 3}


def _path_to_cells(entry: Tuple[int, int], path: str) -> Set[Tuple[int, int]]:
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
) -> None:
    height = len(grid)
    width = len(grid[0]) if height else 0

    green = "\033[92m"
    red = "\033[91m"
    blue = "\033[94m"
    reset = "\033[0m"

    path_cells: Set[Tuple[int, int]] = set()
    if path:
        path_cells = _path_to_cells(entry, path)

    print("+" + "---+" * width)

    for i in range(height):
        row_top = "|"
        row_bottom = "+"

        for j in range(width):
            cell = grid[i][j]

            if (i, j) == entry:
                content = f" {green}0{reset} "
            elif (i, j) == exit:
                content = f" {red}0{reset} "
            elif (i, j) in path_cells and cell != 0b1111:
                content = f" {blue}0{reset} "
            elif cell == 0b1111:
                content = "###"
            else:
                content = "   "

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