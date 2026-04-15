from mlx import Mlx
from generator import MazeGenerator
from shortest_path import shortest_path
from parser import valid_config, parser


def mymouse(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at {x},{y}.")


def mykey(keynum, mystuff):
    print(f"Got key {keynum}, and got my stuff back:")
    print(mystuff)
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)


m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 1280, 720, "toto")

(ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
print(f"Got screen size {w} x {h} .")

wall0, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/0000Wall.png"
)

wall1, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/0001Wall.png"
)


wall2, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/0010Wall.png"
)

wall3, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/0011Wall.png"
)

wall4, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/0100Wall.png"
)


wall5, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/0101Wall.png"
)

wall6, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/0110Wall.png"
)

wall7, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/0111Wall.png"
)

wall8, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/1000Wall.png"
)

wall9, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/1001Wall.png"
)

wall10, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/1010Wall.png"
)

wall11, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/1011Wall.png"
)

wall12, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/1100Wall.png"
)

wall13, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/1101Wall.png"
)

wall14, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/1110Wall.png"
)

wall15, _, _ = m.mlx_png_file_to_image(
    mlx_ptr,
    "assets/1111Wall.png"
)


configs = valid_config(parser("config_test.txt"))


print(configs)
gen = MazeGenerator(width=configs.width, height=configs.height,
                    entry=configs.entry, exit=configs.exit,
                    seed=configs.seed)

maze = gen.generate(perfect=configs.perfect)
print(maze)
path = shortest_path(maze, entry=configs.entry, exit=configs.exit)

stuff = [1, 2]
m.mlx_mouse_hook(win_ptr, mymouse, None)
m.mlx_key_hook(win_ptr, mykey, stuff)
print(maze[0][0], maze[0][1], maze[1][0])
for y in range(configs.height):
    real_y = 100 + y*40
    for x in range(configs.width):
        real_x = 450 + x*40
        if (maze[y][x] == 0):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall0, real_x, real_y)
        if (maze[y][x] == 1):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall1, real_x, real_y)
        if (maze[y][x] == 2):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall2, real_x, real_y)
        if (maze[y][x] == 3):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall3, real_x, real_y)
        if (maze[y][x] == 4):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall4, real_x, real_y)
        if (maze[y][x] == 5):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall5, real_x, real_y)
        if (maze[y][x] == 6):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall6, real_x, real_y)
        if (maze[y][x] == 7):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall7, real_x, real_y)
        if (maze[y][x] == 8):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall8, real_x, real_y)
        if (maze[y][x] == 9):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall9, real_x, real_y)
        if (maze[y][x] == 10):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall10, real_x, real_y)
        if (maze[y][x] == 11):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall11, real_x, real_y)
        if (maze[y][x] == 12):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall12, real_x, real_y)
        if (maze[y][x] == 13):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall13, real_x, real_y)
        if (maze[y][x] == 14):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall14, real_x, real_y)
        if (maze[y][x] == 15):
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, wall15, real_x, real_y)

m.mlx_loop(mlx_ptr)
