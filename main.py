from maze import MazeGenerator, parser, MazeConfiguration, print_maze, shortest_path, path_to_cells
from time import sleep
import sys

def main() -> None:
    config: MazeConfiguration = parser("config.txt")

    if config is None:
        print("=== Invalid configuration input ===")
        return # ou sera melhor sys.exit(1)?

    generator: MazeGenerator = MazeGenerator(
        config.width,
        config.height,
        config.entry,
        config.exit,
        config.seed
    )

    generator.generate(config.perfect)
    maze = generator.grid

    #pseudocodigo:
    # Criar a MazeDisplay  classe
    # Abrir a janela com a funcao que imprime o labirinto e 
    # deteta botoes de teclado para mudar cenas no labirinto
