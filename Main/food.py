import pygame
import colors
import random
import config

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# I used multiple inheritance
# What each function does is basically selects a random spot in each 20 * 20 grid
# and spawns food in that spot

class Apple(Food):
    @staticmethod
    def spawn(screen):
        rand_x = random.choice(range(0, config.WIDTH, 20))
        rand_y = random.choice(range(0, config.HEIGHT, 20))

        pygame.draw.rect(screen, colors.GREEN,
                         rect=(rand_x, rand_y, 20, 20))

        return rand_x, rand_y


class GoldenApple(Food):

    @staticmethod
    def spawn(screen):
        rand_x = random.choice(range(0, config.WIDTH, 20))
        rand_y = random.choice(range(0, config.HEIGHT, 20))

        pygame.draw.rect(screen, colors.YELLOW, rect=(rand_x, rand_y, 20, 20))

        return rand_x, rand_y

