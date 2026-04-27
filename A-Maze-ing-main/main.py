from mazegen import MazeGenerator, MazeConfiguration, print_maze, shortest_path
from parser import parser
from MazeDisplay import MazeDisplay
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

    generator: MazeGenerator = MazeGenerator(
        config.width,
        config.height,
        config.entry,
        config.exit,
        config.seed
    )

    generator.generate(config.perfect)
    maze = generator.grid
    print(len(generator.cells_generated))

    sys.argv[1]
    with open(config.output_file, "w") as f:
        for row in maze:
            line = ''.join(format(x, 'X') for x in row)
            f.write(line + '\n')
        f.write("\n")
        f.write(f"{config.entry[0]},{config.entry[1]}\n")
        f.write(f"{config.exit[0]},{config.exit[1]}\n")
        f.write(shortest_path(maze, config.entry, config.exit))

    print_maze(maze, config.entry, config.exit,
               shortest_path(maze, config.entry, config.exit))

    dsp = MazeDisplay(config)
    dsp.start_display()

    # pseudocodigo:
    # Criar a MazeDisplay  classe
    # Abrir a janela com a funcao que imprime o labirinto e
    # deteta botoes de teclado para mudar cenas no labirinto


if __name__ == "__main__":
    main()
