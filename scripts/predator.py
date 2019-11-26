from random import randint
from pygame.math import Vector2
import pygame
import numpy as np

if __name__ == "__main__" or __name__ == "predator":
    from utility import doughnut, view_dist_coef, find_intercept, point_distance, slope_intercept
    from boid import Boid
else:
    from scripts.utility import doughnut, view_dist_coef, find_intercept, point_distance, slope_intercept
    from scripts.boid import Boid


class Predator(Boid):

    def accelerate(self, flock, predators=None):
    
        # Get steering forces
        #seek2 = self.seek(flock, True, True)
        #avoid2 = self.avoid(flock, True)
        #align2 = self.align(flock, True)
        seek, avoid, align = self.seek_avoid_align(flock)

        # Fear if predator
        fear = self.escape(predators)

        # Apply weights
        avoid = avoid * 0.01
        seek = seek * 0.4
        align = align * 0
        fear = fear * 1
        
        acceleration = avoid + seek + align + fear
        
        if acceleration.magnitude() > 0:
            self.velocity = self.velocity + acceleration
        else:
            self.velocity = self.velocity

    def eat(self, flock):

        current_pos = self.pos
        local_flock = flock

        for i, boid in enumerate(flock):
            distance = point_distance(boid.pos, current_pos)

            if distance < 10:
                local_flock.pop(i)

        return local_flock
