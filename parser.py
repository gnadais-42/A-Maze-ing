from dotenv import load_dotenv
import os
from typing import Optional
from maze import MazeGenerator, MazeConfiguration, print_maze
from pydantic import ValidationError


def parser(config_file: str) -> Optional[MazeConfiguration]:
    """Function that reads the config file and turns it into variables
    usable by the maze generator"""

    try:
        load_dotenv(config_file)
    except (FileNotFoundError, PermissionError):
        return None

    try:
        config = MazeConfiguration(
            width=os.getenv("WIDTH"),
            height=os.getenv("HEIGHT"),
            entry=os.getenv("ENTRY"),
            exit=os.getenv("EXIT"),
            output_file=os.getenv("OUTPUT_FILE"),
            perfect=os.getenv("PERFECT"),
            algorithm=os.getenv("ALGORITHM"),
            seed=os.getenv("SEED"),
            display_mode=os.getenv("DISPLAY_MODE")
        )
    except ValidationError as e:
        for err in e.errors():
            print(err["msg"])
        return None
    return config


def print_config(config: MazeConfiguration) -> None:
    for name, value in config:
        print(f"{name}: {value}")


if __name__ == "__main__":
    config = parser("config_test.txt")
    # print(
    #     os.getenv("WIDTH"),
    #     os.getenv("HEIGHT"),
    #     os.getenv("ENTRY"),
    #     os.getenv("EXIT"),
    #     os.getenv("OUTPUT_FILE"),
    #     os.getenv("PERFECT"),
    #     os.getenv("ALGORITHM"),
    #     os.getenv("SEED"),
    #     os.getenv("DISPLAY_MODE")
    # )
    if config is not None:
        gen = MazeGenerator(
            config.width,
            config.height,
            config.entry,
            config.exit,
            config.seed,
        )
        gen.generate(config.perfect)
        print_maze(gen.grid, gen.entry, gen.exit, None, None)
        print_config(config)
