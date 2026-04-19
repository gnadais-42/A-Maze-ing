from mlx import Mlx

class Display:
    def __init__(self, width: int = 1280, height: int = 720, name: str = "A_Maze_ing") -> None:
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(self.mlx_ptr, width, height, name)

    def new(width: int = 1280, height: int = 720):
        self.mlx.mlx_destroy_window(mlx_ptr, win_ptr)
