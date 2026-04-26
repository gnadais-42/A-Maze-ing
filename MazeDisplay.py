from mlx import Mlx
from maze import MazeGenerator, MazeConfiguration, Player, shortest_path
from maze import path_to_cells
from parser import parser
from typing import Tuple, Any
from collections import deque
import time


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
    """Structure for displaying the Maze graphically. Uses minilibx.
    Everything from the initial maze gen to opening the windows and calculating
    the shortest path, or getting screen dimensions is done at initialization.
    All it needs are valid configs for the maze.

    The size of the second window, colorsets and most other static variables
    are attributes of this class."""
    def __init__(self, configs: MazeConfiguration) -> None:
        self.configs = configs
        self.generator = MazeGenerator(width=configs.width,
                                       height=configs.height,
                                       entry=configs.entry,
                                       exit=configs.exit,
                                       seed=configs.seed)
        self.player = Player(self.generator, configs.entry)
        self.path_shown = False
        self.mlx = Mlx()
        self.maze = self.generator.generate(configs.perfect)
        pathstr = shortest_path(self.maze, entry=configs.entry,
                                exit=configs.exit)
        self.path = path_to_cells(configs.entry, pathstr)
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

        self.colorsets = deque([[0x00000, 0xFFFFFFFF, 0xFF00E5FF],
                               [0xFFFF8E0F, 0xFF7F0FFF, 0xFF00E5FF],
                               [0xFFFF0F97, 0xFF1814F5, 0xFF00E5FF],
                               [0xFF238F18, 0xFFCBFF30, 0xFF00E5FF]])
        self.horses = deque()
        self.carrot = None
        self.stable = None

        self.anim_step = 0

    def _generate_horses(self) -> deque:
        """Generates the images of the horse sprites from asset pngs"""
        horses_img = deque()
        horses_png = [
            "sprites/horse-1.png",
            "sprites/horse-2.png",
            "sprites/horse-3.png",
            "sprites/horse-4.png",
            "sprites/horse-5.png"
        ]
        for sprite in horses_png:
            horse, _, __ = self.mlx.mlx_png_file_to_image(self.mlx_ptr, sprite)
            horses_img.append(horse)

        return horses_img

    def shuffle_horses(self) -> None:
        """Shuffles/rotates through the available horse sprites"""
        self.horses.rotate(-1)

    def shuffle_colors(self) -> None:
        """Shuffles/rotates through the available colorsets"""
        self.colorsets.rotate(-1)

    def mykey(self, keynum, stuff: Any) -> None:
        """Detects various keyboard inputs
        and calls the relevant programs for each input"""
        _ = stuff
        #  print(f"Got key {keynum}")
        if keynum == 103:
            self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr1)
            self.fill_square(self.img_ptr,
                             (0, 0),
                             (self.configs.width * 20,
                              self.configs.height * 20),
                             self.colorsets[0][0])
            self.regen_maze()
            self.anim_step = 0
        if keynum == 104:
            self.shuffle_horses()
            self.display_maze()
        if keynum == 99:
            self.shuffle_colors()
            if (self.anim_step >= len(self.generator.cells_generated)):
                self.display_maze()
        if keynum == 112:
            self.toggle_path()
        if keynum == 115:
            self.anim_step = len(self.generator.cells_generated)
        if keynum == 65307:
            self.gere_close([1, 2])
        if keynum == 65361:
            self.player.move(3)
            self.display_maze()
        if keynum == 65362:
            self.player.move(0)
            self.display_maze()
        if keynum == 65363:
            self.player.move(1)
            self.display_maze()
        if keynum == 65364:
            self.player.move(2)
            self.display_maze()

    def toggle_path(self) -> None:
        """Toggles whether the shortest path is visible or not
        by painting over it"""
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

        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr1,
                                         self.stable,
                                         self.configs.entry[0] * 20,
                                         self.configs.entry[1] * 20)

        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr1,
                                         self.horses[0],
                                         self.player.coords[0] * 20,
                                         self.player.coords[1] * 20)

        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr1,
                                         self.carrot,
                                         self.configs.exit[0] * 20,
                                         self.configs.exit[1] * 20)
        self.path_shown = not self.path_shown

    def gere_close(self, stuff: Any) -> None:
        """Closes the display loop"""
        _ = stuff
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        print("loop exited")

    def gere_close2(self, stuff: Any) -> None:
        """Coses the second window"""
        _ = stuff
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr2)
        print("window2 destroyed")

    def regen_maze(self) -> None:
        """Generates new maze from the same config
        Also calculates the new shortest paths and resets the game"""
        self.maze = self.generator.generate(perfect=self.configs.perfect)
        short_path = shortest_path(self.maze,
                                   self.configs.entry, self.configs.exit)
        self.path = path_to_cells(self.configs.entry, short_path)
        self.path_shown = False
        self.player.reset()
        #  print_maze(self.maze, self.configs.entry,
        #             self.configs.exit, short_path)  # delete later

    def fill_square(self, img: ImgData, start: Tuple[int, int],
                    end: Tuple[int, int], color: int) -> None:
        """Changes the color values of pixels in a square,
         directly in the image buffer.
         It's the only tool used to draw the maze backgrounds and walls"""

        st_x, st_y = start
        fn_x, fn_y = end

        stride = img.sl
        bpp = img.bpp // 8
        for y in range(st_y, fn_y):
            for x in range(st_x, fn_x):
                offset = y * stride + x * bpp
                img.data[offset:offset + bpp] = color.to_bytes(4, 'little')

    def animated_generation(self, stuff: Any) -> None:
        """Animates the backtracking algorithm that generates the maze.
        It works from inside the loop, running at every frame/asap.
        Tracks its own progress with the anim_step attribute
        Has an artificial delay."""

        # IDEIA - mudar o delay na animacao conforme o tamanho do maze

        if self.anim_step == len(self.generator.cells_generated):
            self.display_maze()
            self.anim_step += 1

        if self.anim_step >= len(self.generator.cells_generated):
            return

        _ = stuff
        wall_color, back_color, path_color = self.colorsets[0]

        cell = self.generator.cells_generated[self.anim_step]
        x, y = cell
        x_pixel = 20*x
        y_pixel = 20*y

        time.sleep(0.01)

        self.fill_square(self.img_ptr, (x_pixel, y_pixel),
                         (x_pixel + 20, y_pixel + 20), back_color)

        grid_value = self.maze[y][x]

        if grid_value & (1 << 3):  # check N wall
            self.fill_square(self.img_ptr, (x_pixel, y_pixel),
                             (x_pixel + 20, y_pixel + 3),
                             wall_color)

        if grid_value & (1 << 2):  # check E wall
            self.fill_square(self.img_ptr, (x_pixel + 17, y_pixel),
                             (x_pixel + 20, y_pixel + 20),
                             wall_color)

        if grid_value & (1 << 1):  # check S wall
            self.fill_square(self.img_ptr, (x_pixel, y_pixel + 17),
                             (x_pixel + 20, y_pixel + 20),
                             wall_color)

        if grid_value & 1:  # check W wall
            self.fill_square(self.img_ptr, (x_pixel, y_pixel),
                             (x_pixel + 3, y_pixel + 20),
                             wall_color)

        #  self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr1)

        self.anim_step += 1
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr1,
                                         self.img_ptr.img, 0, 0)

    def display_maze(self) -> None:
        """Displays the completed maze.
        Goes through the generated maze
        and paints the cells according to the generated wall set up."""

        wall_color, back_color, path_color = self.colorsets[0]
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

                if (self. path_shown and (x, y) in self.path
                   and cell != 0b1111 and (x, y) not in (entry, exit)):
                    self.fill_square(self.img_ptr, (real_x, real_y),
                                     (real_x + 20, real_y + 20), path_color)

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
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr1,
                                         self.stable,
                                         entry[0] * 20, entry[1] * 20)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr1,
                                         self.horses[0],
                                         self.player.coords[0] * 20,
                                         self.player.coords[1] * 20)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr1,
                                         self.carrot,
                                         exit[0] * 20, exit[1] * 20)

    def start_display(self) -> None:
        """Initializes the graphical display.
        Responsible for introducing the instruction strings,
        the exit/entry sprites, and setting up all the hooks
        That mlx uses to capture user inputs"""

        stuff = [1, 2]

        self.horses = self._generate_horses()

        self.stable, _, __ = \
            self.mlx.mlx_png_file_to_image(self.mlx_ptr,
                                           "sprites/stable.png")

        self.carrot, _, __ = \
            self.mlx.mlx_png_file_to_image(self.mlx_ptr,
                                           "sprites/carrot.png")

        self.mlx.mlx_hook(self.win_ptr1, 33, 0, self.gere_close, stuff)
        self.mlx.mlx_hook(self.win_ptr2, 33, 0, self.gere_close2, stuff)
        self.mlx.mlx_key_hook(self.win_ptr1, self.mykey, stuff)

        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr2, 4, 5,
                                0xFFFFFFFF, "G - Regen Maze")
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr2, 4, 30,
                                0xFFFFFFFF, "P - Show/Hide Path")
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr2, 4, 55,
                                0xFFFFFFFF, "C - Change Colorset")
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr2, 4, 80,
                                0xFFFFFFFF, "H - Change Horse")
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr2, 4, 105,
                                0xFFFFFFFF, "S - Skip Animation")
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr2, 15, 170,
                                0xFFFFFFFF, "Esc - End Program")

        wall_color, back_color, path_color = self.colorsets[0]
        self.fill_square(self.img_ptr,
                         (0, 0),
                         (self.configs.width * 20, self.configs.height * 20),
                         wall_color)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.animated_generation, None)
        self.mlx.mlx_loop(self.mlx_ptr)
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img_ptr.img)
        print("destroy image")
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr1)
        print("destroy window1")
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr2)
        print("destroy window2")


if __name__ == "__main__":

    config_data = parser("config.txt")

    dsp = MazeDisplay(config_data)

    dsp.start_display()
