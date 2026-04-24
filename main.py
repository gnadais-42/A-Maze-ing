from maze import MazeGenerator, MazeConfiguration, print_maze, shortest_path
from parser import parser
from MazeDisplay import MazeDisplay
import sys


def main() -> None:
    config: MazeConfiguration = parser("config.txt")

    if config is None:
        print("=== Invalid configuration input ===")
        return  # ou sera melhor sys.exit(1)?

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
