from typing import List


def output(output_file: str, maze: List[List[int]], path: str,
           entry: tuple[int, int], exit: tuple[int, int]) -> None:
    """
    Makes an output file with hexadecimal maze representation and path info
    """

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
