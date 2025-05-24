import game
import config
from sys import exit

if __name__ == '__main__':
    game = game.Game(config.WIDTH, config.HEIGHT, "Snake Game")
    game.run()
    exit()