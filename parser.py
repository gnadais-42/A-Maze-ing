from dotenv import load_dotenv
import os
from typing import Optional
from mazegen import MazeGenerator, print_maze
from MazeConfiguration import MazeConfiguration
from pydantic import ValidationError


def require_env(name: str) -> str:
    """
    Checks if variables exist in the env
    """
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Missing environment variable: {name}")
    return value


def parse_tuple(value: str) -> tuple[int, int]:
    """Unravels coordinate tuples"""
    x, y = value.split(",")
    return int(x), int(y)


def parse_bool(value: str) -> bool:
    """parses 'perfect' bool value"""
    return value.lower() in {"1", "true"}


def parser(config_file: str) -> Optional[MazeConfiguration]:
    """Function that reads the config file and turns it into variables
    usable by the maze generator"""

    try:
        load_dotenv(config_file)
    except (FileNotFoundError, PermissionError):
        return None

    try:
        config = MazeConfiguration(
            width=int(require_env("WIDTH")),
            height=int(require_env("HEIGHT")),
            entry=parse_tuple(require_env("ENTRY")),
            exit=parse_tuple(require_env("EXIT")),
            output_file=require_env("OUTPUT_FILE"),
            perfect=parse_bool(require_env("PERFECT")),
            algorithm=os.getenv("ALGORITHM"),
            seed=int(require_env("SEED")),
            display_mode=os.getenv("DISPLAY_MODE")
        )
    except ValidationError as e:
        for err in e.errors():
            print(err["msg"])
        return None
    except (ValueError, TypeError) as e:
        print(e)
        return None

    return config


def print_config(config: MazeConfiguration) -> None:
    """prints configs attributes. Used in debugging"""
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
