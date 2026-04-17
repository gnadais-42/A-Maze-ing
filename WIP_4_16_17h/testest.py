from mlx import Mlx
from generator import MazeGenerator
from shortest_path import shortest_path
from maze_printer import _path_to_cells
from parser import valid_config, parser
from typing import Tuple, Any
from maze_printer import print_maze
from time import sleep


def mymouse(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at {x},{y}.")


def mykey(keynum, mystuff):
    print(f"Got key {keynum}, and got my stuff back:")
    print(mystuff)
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)
    if keynum == 103:
        regen_maze(mlx_ptr, win_ptr, gen, configs)
    if keynum == 119:
        fill_square(mlx_ptr, win_ptr, (0, 0), (configs.height * 20, configs.width * 20), 0xFFFFFFFF)


def gere_close(dummy):
    _ = dummy
    m.mlx_loop_exit(mlx_ptr)


m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 1280, 720, "A-Maze-ing")

(ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
print(f"Got screen size {w} x {h} .")


configs = valid_config(parser("config_test.txt"))

entry = configs.entry
exit = configs.exit


def regen_maze(mlx_ptr, win_ptr, generator: Any, configs:  Any) -> Any:
    """regenerates maze with new set up"""
    maze = generator.generate(perfect=configs.perfect)
    grids = generator.grid_list
    short_path = shortest_path(maze, configs.entry, configs.exit)
    path = _path_to_cells(configs.entry, short_path)
    for grid in grids:
        display_maze_mlx(mlx_ptr, win_ptr, grid, None, configs)
        sleep(0.02)
    display_maze_mlx(mlx_ptr, win_ptr, maze, path, configs)
    print_maze(maze, configs.entry, configs.exit, short_path)
    return maze


def display_maze_mlx(mlx_ptr, win_ptr, maze, path, configs):

    entry = configs.entry
    exit = configs.exit
    if path is None:
        path = []
    m.mlx_clear_window(mlx_ptr, win_ptr)
    fill_square(mlx_ptr, win_ptr, (0, 0), (configs.width * 20, configs.height * 20), 0xFFFFFFFF)

    for y in range(configs.height):
        real_y = y*20
        for x in range(configs.width):
            real_x = x*20
            cell = maze[y][x]

            if (x, y) == entry:
                fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 20), 0xFF00FF00)
            elif (x, y) == exit:
                fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 20), 0xFFFF0000)
            elif (x, y) in path and cell != 0b1111:
                fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 20), 0xFF00E5FF)

            if cell & (1 << 3):  # check N wall
                print("hellllp")
                fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 3), 0x0000000)

            if cell & (1 << 2):  # check E wall
                fill_square(mlx_ptr, win_ptr, (real_x + 17, real_y), (real_x + 20, real_y + 20), 0x0000000)

            if cell & (1 << 1):  # check S wall
                fill_square(mlx_ptr, win_ptr, (real_x, real_y + 17), (real_x + 20, real_y + 20), 0x0000000)

            if cell & 1:  # check W wall
                fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 3, real_y + 20), 0x0000000)

            if cell == 0b1111:
                for xx in range(20):
                    for yy in range(20):
                        m.mlx_pixel_put(mlx_ptr, win_ptr,
                                        real_x + xx, real_y + yy, 0x00000000)


gen = MazeGenerator(width=configs.width, height=configs.height,
                    entry=configs.entry, exit=configs.exit,
                    seed=configs.seed)

maze1 = gen.generate(perfect=configs.perfect)
grids = gen.grid_list
path = shortest_path(maze1, entry=configs.entry, exit=configs.exit)

path_cells = _path_to_cells(entry, path)
stuff = [1, 2]

m.mlx_mouse_hook(win_ptr, mymouse, None)
m.mlx_hook(win_ptr, 33, 0, gere_close, None)
m.mlx_key_hook(win_ptr, mykey, stuff)


def fill_square(mlx_ptr: Any, win_ptr: Any,
                start: Tuple[int, int], end: Tuple[int, int], color: int):
    st_x, st_y = start
    fn_x, fn_y = end

    for xx in range(st_x, fn_x):
        for yy in range(st_y, fn_y):
            m.mlx_pixel_put(mlx_ptr, win_ptr, xx, yy, color)
            #print(f"painted {xx},{yy} with {color}")


for y in range(configs.height * 20):
    for x in range(configs.width * 20):
        m.mlx_pixel_put(mlx_ptr, win_ptr, x, y, 0xFFFFFFFF)

for y in range(configs.height):
    real_y = y*20
    for x in range(configs.width):
        real_x = x*20
        cell = maze1[y][x]

        if (x, y) == entry:
            fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 20), 0xFF00FF00)
        elif (x, y) == exit:
            fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 20), 0xFFFF0000)
        elif (x, y) in path_cells and cell != 0b1111:
            fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 20), 0xFF00E5FF)

        if cell & (1 << 3):  # check N wall
            fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 20, real_y + 3), 0x0000000)

        if cell & (1 << 2):  # check E wall
            fill_square(mlx_ptr, win_ptr, (real_x + 17, real_y), (real_x + 20, real_y + 20), 0x0000000)

        if cell & (1 << 1):  # check S wall
            fill_square(mlx_ptr, win_ptr, (real_x, real_y + 17), (real_x + 20, real_y + 20), 0x0000000)

        if cell & 1:  # check W wall
            fill_square(mlx_ptr, win_ptr, (real_x, real_y), (real_x + 3, real_y + 20), 0x0000000)

        if cell == 0b1111:
            for xx in range(20):
                for yy in range(20):
                    m.mlx_pixel_put(mlx_ptr, win_ptr,
                                    real_x + xx, real_y + yy, 0x00000000)

x = m.mlx_new_image(mlx_ptr, 40, 40)
m.mlx_loop(mlx_ptr)
print("destroy window")
m.mlx_destroy_window(mlx_ptr, win_ptr)
