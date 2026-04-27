from mazegen import MazeGenerator, MazeConfiguration, print_maze, shortest_path
from parser import parser
from MazeDisplay import MazeDisplay
from output_matrix import output
import sys
import os


def main() -> None:

    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print("Invalid input. Only argument must be a valid config file")
        sys.exit()

    config: MazeConfiguration | None = parser(sys.argv[1])

    if config is None:
        print("=== Invalid configuration input ===")
        sys.exit(1)

    dsp = MazeDisplay(config)
    maze = dsp.start_display()

    output(
        config.output_file,
        maze,
        shortest_path(maze, config.entry, config.exit),
        config.entry,
        config.exit)


if __name__ == "__main__":
    main()
