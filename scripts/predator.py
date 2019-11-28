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
        seek, avoid, align, chase = self.seek_avoid_align(flock)

        # Fear if predator
        fear = self.escape(predators)

        # Stay in Enclave
        stay = self.stay_in_enclave()

        # Apply weights
        avoid = avoid * 0
        seek = seek * 0.6
        align = align * 0
        fear = fear * 0
        chase = chase * 0.6
        stay = stay * 1

        acceleration = avoid + seek + align + fear + chase + stay
        
        if acceleration.magnitude() > 0:
            self.velocity = self.velocity + acceleration
        else:
            self.velocity = self.velocity


    # Method that groups Seek, Avoid and Align in one to loop only once through the flock
    # Attempt at factorising the code
    def seek_avoid_align(self, flock):
        # Boid variables
        current_pos = self.pos
        velocity = self.velocity

        # Seek variables
        flock_pos = Vector2()

        # Chase variables
        flock_pos_chase = Vector2()
        chase_distance = 75
        chase_count = 0

        # Avoid variables
        avoid_distance = 25
        avoid_steers = Vector2()
        avoid_count = 0

        # Align variables
        align_distance = 50
        align_steers = Vector2()
        align_count = 0
        
        for boid in flock:
            distance = point_distance(boid.pos, current_pos)

            # Seek: Add current boid position to group vector2
            flock_pos += boid.pos

            # Chase: force towards the nearest cluster of boids
            if distance < chase_distance:
                weight = 1 + (1 / distance)
                chase_steering = boid.pos / weight
                flock_pos_chase += chase_steering
                chase_count += 1

            # Avoid: avoidance steering for current boid
            if distance > 0 and distance < avoid_distance:
                avoid_steering = (current_pos - boid.pos) / distance
                avoid_steering = avoid_steering.normalize() 

                avoid_steers += avoid_steering
                avoid_count += 1
            
            # Align: alignment steering for current boid
            elif distance > 0 and distance < align_distance:
                align_steering = boid.velocity / distance
                align_steering = align_steering.normalize() 

                align_steers += align_steering
                align_count += 1

        # Seek
        target_pos = flock_pos / len(flock)
        desired_seek = (target_pos - current_pos).normalize() * self.maxspeed
        seek_force = (desired_seek - velocity) * self.maxforce

        # Chase
        if chase_count == 0:
            chase_force = flock_pos_chase
        else:
            target_pos_chase = flock_pos_chase / chase_count
            desired_chase = (target_pos_chase - current_pos).normalize() * self.maxspeed
            chase_force = (desired_chase - velocity) * self.maxforce

        # Avoid
        if avoid_steers.magnitude() != 0:
            mean_avoid = avoid_steers / avoid_count
            avoid = mean_avoid.normalize()

            desired_avoid = avoid * self.maxspeed
            avoid_force = (desired_avoid - velocity) * self.maxforce
        else:
            avoid_force = avoid_steers

        # Align
        if align_steers.magnitude() != 0:
            mean_align = align_steers / align_count
            align = mean_align.normalize()

            desired_align = align * self.maxspeed
            align_force = (desired_align - velocity) * self.maxforce
        else:
            align_force = align_steers

        return seek_force, avoid_force, align_force, chase_force


    def eat(self, flock):

        current_pos = self.pos
        local_flock = flock

        for i, boid in enumerate(flock):
            distance = point_distance(boid.pos, current_pos)

            if distance < 10:
                local_flock.pop(i)

        return local_flock
