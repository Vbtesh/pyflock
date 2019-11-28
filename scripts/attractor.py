from random import randint
from pygame.math import Vector2
import pygame
import numpy as np

if __name__ == "__main__":
    from utility import doughnut, view_dist_coef, find_intercept, point_distance, slope_intercept
else:
    from scripts.utility import doughnut, view_dist_coef, find_intercept, point_distance, slope_intercept


class Attractor(pygame.sprite.Sprite):

    def __init__(self, colour, position, shapetype="circle", velocity=None):
        pygame.sprite.Sprite.__init__(self)
        
        self.pos = position
        self.posx = position[0]
        self.posy = position[1]

        self.colour = colour

        if shapetype == "circle":
            self.radius = 40
            self.center = position

        self.velocity = velocity


    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, self.pos, self.radius)
