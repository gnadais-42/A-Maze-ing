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

def gere_close(dummy):
    _ = dummy
    m.mlx_loop_exit(mlx_ptr)


m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 1280, 720, "toto")

(ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
print(f"Got screen size {w} x {h} .")

tiles = []

for i in range(16):
    tile, _, _ = m.mlx_png_file_to_image(
        mlx_ptr,
        f"assets/{i}Wall.png"
    )

    tiles.append(tile)


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
m.mlx_hook(win_ptr, 33, 0, gere_close, None)
m.mlx_key_hook(win_ptr, mykey, stuff)
print(maze[0][0], maze[0][1], maze[1][0])
for y in range(configs.height):
    real_y = y*40
    for x in range(configs.width):
        real_x = x*40
        i = maze[y][x]
        m.mlx_put_image_to_window(mlx_ptr, win_ptr, tiles[i], real_x, real_y)

x = m.mlx_new_image(mlx_ptr, 40, 40)
m.mlx_loop(mlx_ptr)
print("destroy png")
for tile in tiles:
    m.mlx_destroy_image(mlx_ptr, tile)
