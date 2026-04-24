from pydantic import BaseModel, model_validator, Field
from typing import Optional


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
    def valid_coords(self):
        if not ((0 <= self.entry[0] < self.width)
                and (0 <= self.entry[1] < self.height)):
            raise ValueError("Entry point must be inside maze")

        if not ((0 <= self.exit[0] < self.width)
                and (0 <= self.exit[1] < self.height)):
            raise ValueError("Exit point must be inside maze")

        return self

    def is_inside_42(self, x: int, y: int) -> bool:
        if self.height < 6 or self.width < 7:
            return False

        pattern = [
            [1, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 1],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 1],
        ]

        start_row = (self.height - 5) // 2
        start_col = (self.width - 6) // 2

        local_r = y - start_row
        local_c = x - start_col

        if 0 <= local_r < 5 and 0 <= local_c < 6:
            return pattern[local_r][local_c] == 1

        return False

    @model_validator(mode="after")
    def valid_entry_exit(self):
        if self.entry == self.exit:
            raise ValueError("Exit and Entry points must be different")

        if self.is_inside_42(*self.entry):
            raise ValueError("Entry point must not fall inside 42 pattern")

        if self.is_inside_42(*self.exit):
            raise ValueError("Exit point must not fall inside 42 pattern")

        return self
