from maze import MazeGenerator, print_maze, Player
from time import sleep


DIR_LETTER_TO_IDX = {"N": 0, "E": 1, "S": 2, "W": 3}


def test():
    entry = (0,0)
    exit = (10,10)
    gen = MazeGenerator(10, 10, entry, exit)
    gen.generate(True)

    maze = gen.grid
    player = Player(gen, entry)

    while (player.coords != exit):
        print_maze(maze, entry, exit, None, player)
        print(player.coords)
        d = DIR_LETTER_TO_IDX.get(input("Direction: ").upper())
        print(d)
        player.move(d)
        if player.wrong_turn:
            print_maze(maze, entry, exit, None, player)
            sleep(0.5)
            player.correct_turn()


if __name__ == "__main__":
    test()
