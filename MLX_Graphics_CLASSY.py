from mlx import Mlx
from generator import MazeGenerator
from shortest_path import shortest_path
from maze_printer import _path_to_cells
from parser import valid_config, parser, MazeConfiguration
from typing import Tuple, Any
from maze_printer import print_maze
from collections import deque


class ImgData:
    """Structure for image data"""
    def __init__(self, img: Any, width: int,
                 height: int, mlx: Mlx) -> None:

        self.img = img
        self.width = width
        self.height = height
        self.data, self.bpp, self.sl, self.iformat = \
            mlx.mlx_get_data_addr(self.img)


class MazeDisplay:
    """Structure for main vars"""
    def __init__(self, configs: MazeConfiguration) -> None:
        self.configs = configs
        self.generator = MazeGenerator(width=config_data.width,
                                       height=config_data.height,
                                       entry=config_data.entry,
                                       exit=config_data.exit,
                                       seed=config_data.seed)
        self.path_shown = False
        self.mlx = Mlx()
        self.maze = self.generator.generate(configs.perfect)
        pathstr = shortest_path(self.maze, entry=config_data.entry,
                                exit=config_data.exit)
        self.path = _path_to_cells(configs.entry, pathstr)
        self.configs = configs
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr1 = self.mlx.mlx_new_window(self.mlx_ptr,
                                                configs.width*20,
                                                configs.height*20,
                                                "A-maze-ing")

        self.win_ptr2 = self.mlx.mlx_new_window(self.mlx_ptr,
                                                200,
                                                200,
                                                "Commands")

        self.img_ptr = ImgData(self.mlx.mlx_new_image(self.mlx_ptr,
                               self.configs.width*20,
                               (configs.height + 5)*20),
                               self.configs.width*20,
                               self.configs.height*20,
                               self.mlx
                               )

        _, self.screen_w, self.screen_h = \
            self.mlx.mlx_get_screen_size(self.mlx_ptr)

        self.colorsets = deque([[0x00000, 0xFFFFFFFF],
                               [0xFFFF8E0F, 0xFF7F0FFF],
                               [0xFFFF0F97, 0xFF1814F5],
                               [0xFF238F18, 0xFFCBFF30]])

    def shuffle_colors(self) -> None:
        self.colorsets.rotate(-1)
        self.display_maze()

    def mykey(self, keynum, stuff: Any) -> None:
        _ = stuff
        #  print(f"Got key {keynum}")
        if keynum == 32:
            self.mlx.mlx_mouse_hook(self.win_ptr, None, None)
        if keynum == 103:
            self.regen_maze()
        if keynum == 99:
            self.shuffle_colors()
            self.display_maze()
        if keynum == 112:
            self.toggle_path()
        if keynum == 65307:
            self.gere_close([1, 2])

    def toggle_path(self) -> None:
        #  print(self.path_shown)
        if self.path_shown:
            new_color = self.colorsets[0][1]
        else:
            new_color = 0xFF00E5FF

        wall_color = self.colorsets[0][0]

        for path_cell in self.path:
            if path_cell not in [self.configs.entry, self.configs.exit]:
                x, y = path_cell
                real_y = y*20
                real_x = x*20
                cell = self.maze[y][x]
                self.fill_square(self.img_ptr, (real_x, real_y),
                                 (real_x + 20, real_y + 20), new_color)
                if cell & (1 << 3):  # check N wall
                    self.fill_square(self.img_ptr, (real_x, real_y),
                                     (real_x + 20, real_y + 3), wall_color)

                if cell & (1 << 2):  # check E wall
                    self.fill_square(self.img_ptr, (real_x + 17, real_y),
                                     (real_x + 20, real_y + 20), wall_color)

                if cell & (1 << 1):  # check S wall
                    self.fill_square(self.img_ptr, (real_x, real_y + 17),
                                     (real_x + 20, real_y + 20), wall_color)

                if cell & 1:  # check W wall
                    self.fill_square(self.img_ptr, (real_x, real_y),
                                     (real_x + 3, real_y + 20), wall_color)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr1,
                                         self.img_ptr.img, 0, 0)
        self.path_shown = not self.path_shown

    def gere_close(self, stuff: Any) -> None:
        _ = stuff
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        print("loop exited")

    def gere_close2(self, stuff: Any) -> None:
        _ = stuff
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr2)
        print("window2 destroyed")

    def regen_maze(self) -> None:
        """regenerates maze with new set up"""
        self.maze = self.generator.generate(perfect=self.configs.perfect)
        short_path = shortest_path(self.maze,
                                   self.configs.entry, self.configs.exit)
        self.path = _path_to_cells(self.configs.entry, short_path)
        self.path_shown = False
        self.display_maze()
        print_maze(self.maze, self.configs.entry,
                   self.configs.exit, short_path)  # delete later

    def fill_square(self, img: ImgData, start: Tuple[int, int],
                    end: Tuple[int, int], color: int) -> None:

        st_x, st_y = start
        fn_x, fn_y = end

        stride = img.sl
        bpp = img.bpp // 8
        for y in range(st_y, fn_y):
            for x in range(st_x, fn_x):
                offset = y * stride + x * bpp
                img.data[offset:offset + bpp] = color.to_bytes(4, 'little')

    def display_maze(self) -> None:

        wall_color, back_color = self.colorsets[0]
        entry = self.configs.entry
        exit = self.configs.exit

        self.fill_square(self.img_ptr,
                         (0, 0),
                         (self.configs.width * 20, self.configs.height * 20),
                         back_color)

        for y in range(self.configs.height):
            real_y = y*20
            for x in range(self.configs.width):
                real_x = x*20
                cell = self.maze[y][x]

                if (x, y) == entry:
                    self.fill_square(self.img_ptr, (real_x, real_y),
                                     (real_x + 20, real_y + 20), 0xFF00FF00)

                elif (x, y) == exit:
                    self.fill_square(self.img_ptr, (real_x, real_y),
                                     (real_x + 20, real_y + 20), 0xFFFF0000)

                elif (self.path_shown and (x, y) in self.path
                      and cell != 0b1111):
                    self.fill_square(self.img_ptr, (real_x, real_y),
                                     (real_x + 20, real_y + 20), 0xFF00E5FF)

                if cell == 0b1111:
                    self.fill_square(self.img_ptr, (real_x, real_y),
                                     (real_x + 20, real_y + 20), wall_color)

                else:

                    if cell & (1 << 3):  # check N wall
                        self.fill_square(self.img_ptr, (real_x, real_y),
                                         (real_x + 20, real_y + 3),
                                         wall_color)

                    if cell & (1 << 2):  # check E wall
                        self.fill_square(self.img_ptr, (real_x + 17, real_y),
                                         (real_x + 20, real_y + 20),
                                         wall_color)

                    if cell & (1 << 1):  # check S wall
                        self.fill_square(self.img_ptr, (real_x, real_y + 17),
                                         (real_x + 20, real_y + 20),
                                         wall_color)

                    if cell & 1:  # check W wall
                        self.fill_square(self.img_ptr, (real_x, real_y),
                                         (real_x + 3, real_y + 20),
                                         wall_color)

        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr1)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr1,
                                         self.img_ptr.img, 0, 0)

    def start_display(self) -> None:
        stuff = [1, 2]

        self.mlx.mlx_hook(self.win_ptr1, 33, 0, self.gere_close, stuff)
        self.mlx.mlx_hook(self.win_ptr2, 33, 0, self.gere_close2, stuff)
        self.mlx.mlx_key_hook(self.win_ptr1, self.mykey, stuff)

        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr2, 4, 5,
                                0xFFFFFFFF, "G - Regen Maze")
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr2, 4, 30,
                                0xFFFFFFFF, "P - Show/Hide Path")
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr2, 4, 55,
                                0xFFFFFFFF, "C - Change Colorset")
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr2, 15, 170,
                                0xFFFFFFFF, "Esc - End Program")

        self.display_maze()

        self.mlx.mlx_loop(self.mlx_ptr)
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img_ptr.img)
        print("destroy image")
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr1)
        print("destroy window1")
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr2)
        print("destroy window2")


if __name__ == "__main__":

    config_data = valid_config(parser("config_test.txt"))

    dsp = MazeDisplay(config_data)

    dsp.start_display()
