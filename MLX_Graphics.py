from mlx import Mlx
from maze import MazeGenerator, MazeConfiguration, shortest_path, path_to_cells, print_maze
from parser import parser
from typing import Tuple, Any
from collections import deque


# maybe instead of individual colors,
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
        self.path_shown = False
        self.mlx = Mlx()
        self.maze = None
        self.path = None
        self.configs = None
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr1 = None
        self.win_ptr2 = None
        self.img = ImgData()
        self.screen_w = 1920
        self.screen_h = 1080
        self.colorsets = deque([[0x0000000, 0xFFFFFFFF],
                               [0xFFFF8E0F, 0xFF7F0FFF],
                               [0xFFFF0F97, 0xFF1814F5],
                               [0xFF238F18, 0xFFCBFF30]])

        # maybe instead of individual colors,
        # do colorsets that also affect the background

    def shuffle_colors(self) -> None:
        self.colorsets.rotate(-1)
        display_maze(self, self.configs)


def mymouse(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at {x},{y}.")


def mykey(keynum, dsp: MazeDisplay):
    print(f"Got key {keynum}, and got my stuff back:")
    if keynum == 32:
        dsp.mlx.mlx_mouse_hook(dsp.win_ptr, None, None)
    if keynum == 103:
        regen_maze(dsp, gen, configs)
    if keynum == 99:
        dsp.shuffle_colors()
        display_maze(dsp, dsp.configs)
    if keynum == 112:
        toggle_path(dsp)
    if keynum == 119:
        fill_square(dsp.img(0, 0),
                    (configs.height * 20, configs.width * 20), 0xFFFFFFFF)


def toggle_path(dsp: MazeDisplay):
    print(dsp.path_shown)
    if dsp.path_shown:
        new_color = dsp.colorsets[0][1]
    else:
        new_color = 0xFF00E5FF

    wall_color = dsp.colorsets[0][0]

    for path_cell in dsp.path:
        if path_cell not in [dsp.configs.entry, dsp.configs.exit]:
            x, y = path_cell
            real_y = y*20
            real_x = x*20
            cell = dsp.maze[y][x]
            fill_square(dsp.img, (real_x, real_y),
                        (real_x + 20, real_y + 20), new_color)
            if cell & (1 << 3):  # check N wall
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 20, real_y + 3), wall_color)

            if cell & (1 << 2):  # check E wall
                fill_square(dsp.img, (real_x + 17, real_y),
                            (real_x + 20, real_y + 20), wall_color)

            if cell & (1 << 1):  # check S wall
                fill_square(dsp.img, (real_x, real_y + 17),
                            (real_x + 20, real_y + 20), wall_color)

            if cell & 1:  # check W wall
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 3, real_y + 20), wall_color)
    dsp.mlx.mlx_put_image_to_window(dsp.mlx_ptr, dsp.win_ptr1,
                                    dsp.img.img, 0, 0)
    dsp.path_shown = not dsp.path_shown


def gere_close(dsp: MazeDisplay):
    dsp.mlx.mlx_loop_exit(dsp.mlx_ptr)
    print("loop exited")


def gere_close2(dsp: MazeDisplay):
    dsp.mlx.mlx_destroy_window(dsp.mlx_ptr, dsp.win_ptr2)
    print("window2 destroyed")


def regen_maze(dsp: MazeDisplay, generator: MazeGenerator, configs:  Any):
    """regenerates maze with new set up"""
    dsp.maze = generator.generate(perfect=configs.perfect)
    short_path = shortest_path(dsp.maze, configs.entry, configs.exit)
    dsp.path = path_to_cells(configs.entry, short_path)
    dsp.path_shown = False
    display_maze(dsp, dsp.configs)
    print_maze(dsp.maze, configs.entry,
               configs.exit, short_path)  # delete later


def fill_square(img: ImgData, start: Tuple[int, int],
                end: Tuple[int, int], color: int):

    st_x, st_y = start
    fn_x, fn_y = end

    stride = img.sl
    bpp = img.bpp // 8
    for y in range(st_y, fn_y):
        for x in range(st_x, fn_x):
            offset = y * stride + x * bpp
            img.data[offset:offset + bpp] = color.to_bytes(4, 'little')


def display_init(configs) -> MazeDisplay:

    dsp = MazeDisplay()
    dsp.configs = configs
    dsp.mlx = Mlx()
    dsp.mlx_ptr = dsp.mlx.mlx_init()
    dsp.win_ptr1 = dsp.mlx.mlx_new_window(dsp.mlx_ptr,
                                          configs.width*20,
                                          configs.height*20,
                                          "A-maze-ing")

    dsp.win_ptr2 = dsp.mlx.mlx_new_window(dsp.mlx_ptr,
                                          200,
                                          200,
                                          "Commands")

    dsp.mlx.mlx_string_put(dsp.mlx_ptr, dsp.win_ptr2, 0, 0,
                           0xFFFFFFFF, "G - Regen Maze")
    dsp.mlx.mlx_string_put(dsp.mlx_ptr, dsp.win_ptr2, 0, 20,
                           0xFFFFFFFF, "P - Show/Hide Path")
    dsp.mlx.mlx_string_put(dsp.mlx_ptr, dsp.win_ptr2, 0, 40,
                           0xFFFFFFFF, "C - Change Colorset")
    (ret, w, h) = dsp.mlx.mlx_get_screen_size(dsp.mlx_ptr)
    dsp.img.img = dsp.mlx.mlx_new_image(dsp.mlx_ptr,
                                        configs.width*20,
                                        (configs.height + 5)*20)

    dsp.img.data, dsp.img.bpp, dsp.img.sl, dsp.img.iformat = \
        dsp.mlx.mlx_get_data_addr(dsp.img.img)
    return (dsp)


def display_maze(dsp: MazeDisplay,
                 configs: MazeConfiguration) -> None:

    wall_color, back_color = dsp.colorsets[0]
    entry = configs.entry
    exit = configs.exit
    dsp.mlx.mlx_clear_window(dsp.mlx_ptr, dsp.win_ptr1)

    fill_square(dsp.img, (0, 0),
                (configs.width * 20, configs.height * 20), back_color)

    for y in range(configs.height):
        real_y = y*20
        for x in range(configs.width):
            real_x = x*20
            cell = dsp.maze[y][x]

            if (x, y) == entry:
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 20, real_y + 20), 0xFF00FF00)
            elif (x, y) == exit:
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 20, real_y + 20), 0xFFFF0000)
            elif dsp.path_shown and (x, y) in dsp.path and cell != 0b1111:
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 20, real_y + 20), 0xFF00E5FF)

            if cell == 0b1111:
                fill_square(dsp.img, (real_x, real_y),
                            (real_x + 20, real_y + 20), wall_color)
            else:

                if cell & (1 << 3):  # check N wall
                    fill_square(dsp.img, (real_x, real_y),
                                (real_x + 20, real_y + 3), wall_color)

                if cell & (1 << 2):  # check E wall
                    fill_square(dsp.img, (real_x + 17, real_y),
                                (real_x + 20, real_y + 20), wall_color)

                if cell & (1 << 1):  # check S wall
                    fill_square(dsp.img, (real_x, real_y + 17),
                                (real_x + 20, real_y + 20), wall_color)

                if cell & 1:  # check W wall
                    fill_square(dsp.img, (real_x, real_y),
                                (real_x + 3, real_y + 20), wall_color)

    dsp.mlx.mlx_put_image_to_window(dsp.mlx_ptr, dsp.win_ptr1,
                                    dsp.img.img, 0, 0)


configs = parser("config.txt")
entry = configs.entry
exit = configs.exit
dsp = display_init(configs)

gen = MazeGenerator(width=configs.width, height=configs.height,
                    entry=configs.entry, exit=configs.exit,
                    seed=configs.seed)

dsp.maze = gen.generate(perfect=configs.perfect)
path = shortest_path(dsp.maze, entry=configs.entry, exit=configs.exit)

dsp.path = path_to_cells(entry, path)


stuff = [1, 2]

dsp.mlx.mlx_mouse_hook(dsp.win_ptr1, mymouse, None)
dsp.mlx.mlx_hook(dsp.win_ptr1, 33, 0, gere_close, dsp)
dsp.mlx.mlx_hook(dsp.win_ptr2, 33, 0, gere_close2, dsp)
dsp.mlx.mlx_key_hook(dsp.win_ptr1, mykey, dsp)


display_maze(dsp, configs)

dsp.mlx.mlx_loop(dsp.mlx_ptr)
print("destroy image")
dsp.mlx.mlx_destroy_image(dsp.mlx_ptr, dsp.img.img)
print("destroy window")
dsp.mlx.mlx_destroy_window(dsp.mlx_ptr, dsp.win_ptr1)
dsp.mlx.mlx_destroy_window(dsp.mlx_ptr, dsp.win_ptr2)
