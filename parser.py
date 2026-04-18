from dotenv import load_dotenv
import os
from pydantic import BaseModel, model_validator, ValidationError, Field
from typing import Dict, Optional


class MazeConfiguration(BaseModel):
    """class for validating Maze config"""
    width: int = Field(gt=1)
    height: int = Field(gt=1)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    algorithm: Optional[str] = None
    seed: Optional[int] = None
    display_mode: Optional[str] = None

    @model_validator(mode="after")
    def valid_chk(self):
        if not ((0 <= self.entry[0] < self.width)
                and (0 <= self.entry[1] < self.height)):
            raise ValueError("Entry point must be inside maze")

        if not ((0 <= self.exit[0] < self.width)
                and (0 <= self.exit[1] < self.height)):
            raise ValueError("Exit point must be inside maze")

        if self.entry == self.exit:
            raise ValueError("Exit and Entry points must be different")

        if self.height > 6 or self.width > 7:
            pattern = [
                [1, 0, 1, 0, 1, 1],
                [1, 0, 1, 0, 0, 1],
                [1, 1, 1, 0, 1, 1],
                [0, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 1],
            ]

            start_x = (self.width - 6) // 2
            start_y = (self.height - 5) // 2

            if (
                6 > self.exit[0] - start_x >= 0 and
                5 > self.exit[1] - start_y >= 0
            ):

                if pattern[self.exit[1] - start_y][self.exit[0] - start_x]:
                    raise ValueError("Exit point must not "
                                     "fall inside 42 pattern")

            if (
                6 > self.entry[0] - start_x >= 0 and
                5 > self.entry[1] - start_y >= 0
            ):
                if pattern[self.entry[1] - start_y][self.entry[0] - start_x]:
                    raise ValueError("Entry point must not "
                                     "fall inside 42 pattern")

        return self


def valid_config(config: Dict) -> Optional[MazeConfiguration]:
    """validator/interface function for maze config.
    Pretty sure it catches most errors.
    Unfortunatelly stuff like type errors (WIDTH=asd) doesnt seem to show up in the error messages. Maybe fix that"""
    if not config:
        return None

    config_data = {
        "width":        config.get("WIDTH", None),
        "height":       config.get("HEIGHT", None),
        "entry":        config.get("ENTRY", None),
        "exit":         config.get("EXIT", None),
        "output_file":  config.get("OUTPUT_FILE", None),
        "perfect":      config.get("PERFECT", None),
        "algorithm":    config.get("ALGORITHM", None),
        "seed":         config.get("SEED", None),
        "display_mode": config.get("DISPLAY_MODE", None)
    }

    try:
        validated_config = MazeConfiguration(**config_data)
        return validated_config
    except ValidationError as e:
        for err in e.errors():
            print(err["msg"])
        return None


def parser(config_file: str) -> Optional[Dict]:
    """Function that reads the config file and turns it into variables
    usable by the maze generator

    Probably has redundant validation"""

    try:
        load_dotenv(config_file)
    except (FileNotFoundError, PermissionError):
        return None

    config = {}
    try:

        exit_raw = os.getenv("EXIT")
        entry_raw = os.getenv("ENTRY")

        if not exit_raw or not entry_raw:
            return None

        config["WIDTH"] = int(os.getenv("WIDTH"))
        config["HEIGHT"] = int(os.getenv("HEIGHT"))
        config["EXIT"] = tuple(map(int, (exit_raw.split(","))))
        config["ENTRY"] = tuple(map(int, (entry_raw.split(","))))
        config["OUTPUT_FILE"] = os.getenv("OUTPUT_FILE")
        config["PERFECT"] = os.getenv("PERFECT").upper() == "TRUE"

    except (ValueError, TypeError):
        return None

    try:
        config["SEED"] = int(os.getenv("SEED"))
    except (ValueError, TypeError):
        config["SEED"] = None

    config["DISPLAY_MODE"] = os.getenv("DISPLAY_MODE")
    config["ALGORITHM"] = os.getenv("ALGORITHM")
    return config


if __name__ == "__main__":
    configs = parser("config_test.txt")
    if (configs):
        print(configs)
        print("\n\n\n\n---------------------------------------")
        validated_config = valid_config(configs)
        print(validated_config)
