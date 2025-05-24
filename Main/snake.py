# this is the snake class
import pygame
import colors

class Snake:
    def __init__(self, width=20, height=40, x=0, y=0, speed=1, color=colors.RED):
        self.width = width
        self.height = height
        self.speed = speed
        self.body = [(x + 20, y), (x,y)]
        self.direction = "DOWN"
        self.x = x
        self.y = y
        self.color = color
        self.score = 0

    def draw(self, screen):
        # draw each body part in the screen

        for x, y in self.body:
            pygame.draw.rect(screen, self.color, (x, y, 20, 20))

    def move(self):
        head_x, head_y = self.body[0] # decompose the tuple to two components

        if self.direction == "UP":
            new_head = (head_x, head_y - 20)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + 20)
        elif self.direction == "RIGHT":
            new_head = (head_x + 20, head_y)
        elif self.direction == "LEFT":
            new_head = (head_x - 20, head_y)

        self.body = [new_head] + self.body[:-1]

    def grow(self, food):
        self.body.append(food)

    def position(self):
        return self.body

    def count(self):
        c = 0

        for x in self.body:
            c += 1

        return c
