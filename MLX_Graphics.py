from mlx import Mlx
from generator import MazeGenerator
from shortest_path import shortest_path
from maze_printer import _path_to_cells
from parser import valid_config, parser
from typing import Tuple, Any
from maze_printer import print_maze
from collections import deque


#maybe instead of individual colors, 
# do color sets that also affect the background

class ImgData:
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0


class MazeDisplay:
    """Structure for main vars"""
    def __init__(self):
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = None
        self.img = ImgData()
        self.screen_w = 1920
        self.screen_h = 1080
        self.colors = deque([0x0000000, 0xFFFF8E0F, 0xFF7F0FFF,
                            0xFFFF0F97, 0xFF1814F5, 0xFF238F18,
                            0xFFCBFF30])

        # maybe instead of individual colors,
        # do colorsets that also affect the background

        self.wallcolor = 0x0000000

    def shuffle_colors(self) -> None:
        self.colors.rotate(-1)
        self.wallcolor = self.colors[0]


def mymouse(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at {x},{y}.")


def mykey(keynum, dsp: MazeDisplay):
    print(f"Got key {keynum}, and got my stuff back:")
    if keynum == 32:
        dsp.mlx.mlx_mouse_hook(dsp.win_ptr, None, None)
    if keynum == 103:
        regen_maze(dsp, gen, configs)
    if keynum == 119:
        fill_square(dsp.img(0, 0),
                    (configs.height * 20, configs.width * 20), 0xFFFFFFFF)


def gere_close(dsp: MazeDisplay):
    dsp.mlx.mlx_loop_exit(dsp.mlx_ptr)
    print("loop exited")


def regen_maze(dsp: MazeDisplay, generator: Any, configs:  Any, ) -> Any:
    """regenerates maze with new set up"""
    maze = generator.generate(perfect=configs.perfect)
    short_path = shortest_path(maze, configs.entry, configs.exit)
    path = _path_to_cells(configs.entry, short_path)
    display_maze(dsp, maze, path, configs)
    print_maze(maze, configs.entry, configs.exit, short_path)
    return maze


def fill_square(img: ImgData, start: Tuple[int, int],
                end: Tuple[int, int], color: int):

    st_x, st_y = start
    fn_x, fn_y = end

    stride = img.sl
    bpp = img.bpp // 8
    for y in range(st_y, fn_y):
        for x in range(st_x, fn_x):
            offset = y * stride + x * bpp
            img.data[offset:offset + 4] = color.to_bytes(4, 'little')


def display_init(configs) -> MazeDisplay:

    dsp = MazeDisplay()
    dsp.mlx = Mlx()
    dsp.mlx_ptr = dsp.mlx.mlx_init()
    dsp.win_ptr = dsp.mlx.mlx_new_window(dsp.mlx_ptr,
                                         configs.width*20,
                                         (configs.height + 5)*20,
                                         "A-maze-ing")

    (ret, w, h) = dsp.mlx.mlx_get_screen_size(dsp.mlx_ptr)
    dsp.img.img = dsp.mlx.mlx_new_image(dsp.mlx_ptr,
                                        configs.width*20,
                                        (configs.height + 5)*20)

    dsp.img.data, dsp.img.bpp, dsp.img.sl, dsp.img.iformat = \
        dsp.mlx.mlx_get_data_addr(dsp.img.img)
    return (dsp)


def display_maze(dsp: MazeDisplay, maze, path, configs):

    entry = configs.entry
    exit = configs.exit
    dsp.mlx.mlx_clear_window(dsp.mlx_ptr, dsp.win_ptr)

    fill_square(dsp.img, (0, 0),
                (configs.width * 20, configs.height * 20), 0xFFFFFFFF)

    for y in range(configs.height):
        real_y = y*20
        for x in range(configs.width):
            real_x = x*20
            cell = maze[y][x]

            if (x, y) == entry:
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 20, real_y + 20), 0xFF00FF00)
            elif (x, y) == exit:
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 20, real_y + 20), 0xFFFF0000)
            elif (x, y) in path and cell != 0b1111:
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 20, real_y + 20), 0xFF00E5FF)

            if cell & (1 << 3):  # check N wall
                print(f"Parede N em {real_x},{real_y}")
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 20, real_y + 3), 0x0000000)

            if cell & (1 << 2):  # check E wall
                print(f"Parede E em {real_x},{real_y}")
                fill_square(dsp.img, (real_x + 17, real_y),
                            (real_x + 20, real_y + 20), 0x0000000)

            if cell & (1 << 1):  # check S wall
                print(f"Parede S em {real_x},{real_y}")
                fill_square(dsp.img, (real_x, real_y + 17),
                            (real_x + 20, real_y + 20), 0x0000000)

            if cell & 1:  # check W wall
                print(f"Parede W em {real_x},{real_y}")
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 3, real_y + 20), 0x0000000)

            if cell == 0b1111:
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 20, real_y + 20), 0x0000000)

    dsp.mlx.mlx_put_image_to_window(dsp.mlx_ptr, dsp.win_ptr,
                                    dsp.img.img, 0, 0)


configs = valid_config(parser("config_test.txt"))

entry = configs.entry
exit = configs.exit


gen = MazeGenerator(width=configs.width, height=configs.height,
                    entry=configs.entry, exit=configs.exit,
                    seed=configs.seed)

maze1 = gen.generate(perfect=configs.perfect)
path = shortest_path(maze1, entry=configs.entry, exit=configs.exit)

path_cells = _path_to_cells(entry, path)

dsp = display_init(configs)

stuff = [1, 2]

dsp.mlx.mlx_mouse_hook(dsp.win_ptr, mymouse, None)
dsp.mlx.mlx_hook(dsp.win_ptr, 33, 0, gere_close, dsp)
dsp.mlx.mlx_key_hook(dsp.win_ptr, mykey, dsp)


display_maze(dsp, maze1, path_cells, configs)

dsp.mlx.mlx_loop(dsp.mlx_ptr)
print("destroy image")
dsp.mlx.mlx_destroy_image(dsp.mlx_ptr, dsp.img.img)
print("destroy window")
dsp.mlx.mlx_destroy_window(dsp.mlx_ptr, dsp.win_ptr)
