from random import randint
from pygame.math import Vector2
import pygame
import numpy as np

if __name__ == "__main__":
    from utility import doughnut, view_dist_coef, find_intercept, point_distance, slope_intercept
else:
    from scripts.utility import doughnut, view_dist_coef, find_intercept, point_distance, slope_intercept


class Wall(pygame.sprite.Sprite):
    
    def __init__(self, colour, start_pos, end_pos):
        pygame.sprite.Sprite.__init__(self)

        self.edge1 = Vector2((start_pos[0], start_pos[1]))
        self.edge2 = Vector2((end_pos[0], end_pos[1]))

        self.colour = colour

    def draw(self, surface):
        pygame.draw.line(surface, self.colour, self.edge1, self.edge2)


class Enclave():

    def __init__(self, dimensions, colour):

        self.colour = colour

        self.width = dimensions[0]
        self.height = dimensions[1]

        self.top_left = Vector2((0, 0))
        self.top_right = Vector2((self.width-1, 0))
        self.bottom_left = Vector2((0, self.height-1))
        self.bottom_right = Vector2((self.width-1, self.height-1))

        self.walls = [
            Wall(self.colour, self.top_left, self.top_right),
            Wall(self.colour, self.top_left, self.bottom_left),
            Wall(self.colour, self.bottom_right, self.top_right),
            Wall(self.colour, self.bottom_left, self.bottom_right)
        ]


    def draw(self, surface):

        for wall in self.walls:
            wall.draw(surface)
