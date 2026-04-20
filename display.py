from mlx import Mlx
from typing import Any, Tuple

class Display:
    def __init__(self, width: int = 1280, height: int = 720, name: str = "A_Maze_ing") -> None:
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(self.mlx_ptr, width, height, name)

    def new(self, width: int = 1280, height: int = 720, name: str = "A_Maze_ing"):
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.win_ptr = self.mlx.mlx_new_window(self.mlx_ptr, width, height, name)

    def display_maze_mlx(self, mlx_ptr, win_ptr, maze, path, configs):

        entry = configs.entry
        exit = configs.exit
        if path is None:
            path = []
        self.mlx.mlx_clear_window(mlx_ptr, win_ptr)
        self.fill_square(mlx_ptr, win_ptr, (0, 0), (configs.width * 20, configs.height * 20), 0xFFFFFFFF)

        for y in range(configs.height):
            real_y = y*20
            for x in range(configs.width):
                real_x = x*20
                cell = maze[y][x]

                if (x, y) == entry:
                    self.fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 20), 0xFF00FF00)
                elif (x, y) == exit:
                    self.fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 20), 0xFFFF0000)
                elif (x, y) in path and cell != 0b1111:
                    self.fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 20), 0xFF00E5FF)

                if cell & (1 << 3):  # check N wall
                    print("hellllp")
                    self.fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 3), 0x0000000)

                if cell & (1 << 2):  # check E wall
                    self.fill_square(mlx_ptr, win_ptr, (real_x + 17, real_y), (real_x + 20, real_y + 20), 0x0000000)

                if cell & (1 << 1):  # check S wall
                    self.fill_square(mlx_ptr, win_ptr, (real_x, real_y + 17), (real_x + 20, real_y + 20), 0x0000000)

                if cell & 1:  # check W wall
                    self.fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 3, real_y + 20), 0x0000000)

                if cell == 0b1111:
                    for xx in range(20):
                        for yy in range(20):
                            self.mlx.mlx_pixel_put(mlx_ptr, win_ptr,
                                            real_x + xx, real_y + yy, 0x00000000)

        def fill_square(self, mlx_ptr: Any, win_ptr: Any,
                        start: Tuple[int, int], end: Tuple[int, int], color: int):
            st_x, st_y = start
            fn_x, fn_y = end

            for xx in range(st_x, fn_x):
                for yy in range(st_y, fn_y):
                    self.mlx.mlx_pixel_put(mlx_ptr, win_ptr, xx, yy, color)
                    #print(f"painted {xx},{yy} with {color}")