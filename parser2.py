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

    @model_validator(mode="before")
    @classmethod
    def parse_tuple_fields(cls, data):
        def parse(coords):
            if isinstance(coords, str):
                return tuple(x for x in coords.split(","))
            return coords

        if isinstance(data, dict):
            if "entry" in data:
                data["entry"] = parse(data["entry"])
            if "exit" in data:
                data["exit"] = parse(data["exit"])

        return data

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

def parser(config_file: str) -> Optional[MazeConfiguration]:
    """Function that reads the config file and turns it into variables
    usable by the maze generator

    Probably has redundant validation"""

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
    print(
        os.getenv("WIDTH"),
        os.getenv("HEIGHT"),
        os.getenv("ENTRY"),
        os.getenv("EXIT"),
        os.getenv("OUTPUT_FILE"),
        os.getenv("PERFECT"),
        os.getenv("ALGORITHM"),
        os.getenv("SEED"),
        os.getenv("DISPLAY_MODE")
    )
    print_config(config)
