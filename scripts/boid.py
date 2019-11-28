from random import randint
from pygame.math import Vector2
import pygame
import numpy as np

if __name__ == "__main__" or __name__ == "boid":
    from utility import doughnut, view_dist_coef, find_intercept, point_distance, slope_intercept
else:
    from scripts.utility import doughnut, view_dist_coef, find_intercept, point_distance, slope_intercept


class Boid(pygame.sprite.Sprite):

    def __init__(self, scale, max_speed, color, vector, dimensions, pos=None):
        pygame.sprite.Sprite.__init__(self)
        if not pos:
            self.pos = Vector2(randint(1, dimensions[0]), randint(1, dimensions[1]))
        else:
            self.pos = Vector2(pos)
        #self.init_pos = (dimensions[0]/2, dimensions[1]/2)
        self.surface_dim = dimensions

        self.color = color

        self.scale = scale
        self.height = int(15*scale // 1)
        self.width = int(10*scale // 1)

        self.rect = pygame.Rect(self.pos[0] + self.width/2, self.pos[1] + self.height/2, self.width, self.height)
        self.boundaries = [self.rect.midtop, self.rect.bottomleft, self.rect.bottomright]

        # Movement and steering attributes
        # Position is embedded in the .rect attribute
        self.velocity = Vector2()
        self.velocity.from_polar(vector)
        self.acceleration = Vector2()

        self.maxspeed = max_speed
        self.maxforce = 0.02
        
        # Vision and radius
        self.view_distance = 75
        self.vision()
        #self.radius = point_distance(self.rect.center, self.ahead2) * 50 # Will be half of the ahead2 distance, default is 25


    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.boundaries)
        #pygame.draw.line(surface, self.color, self.pos, self.ahead)


    def calcnewbounds(self):
        # Tip of the boid
        velocity = self.velocity.as_polar()
        head = self.rect.center
        wing_len = int(15*self.scale // 1)

        left_angle = velocity[1] + 160
        right_angle = velocity[1] + 200

        left_vector = Vector2()
        left_vector.from_polar((wing_len, left_angle))
        right_vector = Vector2()
        right_vector.from_polar((wing_len, right_angle))
        
        # Apply offset and return new boundaries
        left_wing = (head[0] + left_vector[0], head[1] + left_vector[1])
        right_wing = (head[0] + right_vector[0], head[1] + right_vector[1])
        
        return [head, left_wing, right_wing]

    
    def accelerate(self, flock, predators=None):

        # Get steering forces
        #seek2 = self.seek(flock, True, True)
        #avoid2 = self.avoid(flock, True)
        #align2 = self.align(flock, True)
        seek, avoid, align = self.seek_avoid_align(flock)

        # Fear if predator
        fear = self.escape(predators)

        # Stay in Enclave
        stay = self.stay_in_enclave()

        # Apply weights
        avoid = avoid * 1
        seek = seek * 0.4
        align = align * 0.8
        fear = fear * 1.6
        stay = stay * 0.7
        
        acceleration = avoid + seek + align + fear + stay
        
        if acceleration.magnitude() > 0:
            self.velocity = self.velocity + acceleration
        else:
            self.velocity = self.velocity
        


    def update(self):
        # Find new position based on velocity from the calcnewpos method
        newpos = self.calcnewpos(self.rect, self.velocity)

        # Treat space as a doughnut (i.e. make sure boids that fly out come out through the opposite side of the screen)
        (x, y) =  doughnut(newpos.centerx, newpos.centery, (self.surface_dim))
        newpos.centerx, newpos.centery, newpos.center = x, y, (x, y)

        # Assign the rect attribute to be the new position and redefine the boundaries of the boid
        self.rect = newpos
        self.pos = Vector2(self.rect.center)
        self.boundaries = self.calcnewbounds()
        
        # Reinitialise acceleration for next frame
        self.acceleration = Vector2()

        # Vision : defined as ahead and ahead 2
        self.vision()


    def calcnewpos(self, rect, vector):
        return rect.move(vector[0], vector[1])


    def seek(self, target, flock=False, outcome=False):
        if flock:
            flock_pos = Vector2()
            for boid in target:
                flock_pos += boid.pos
            target_pos = flock_pos / len(target)
        else:
            target_pos = Vector2(target.pos)

        current_pos = Vector2(self.pos)

        if target_pos == current_pos:
            #self.randomise_pos()
            #current_pos = Vector2(self.rect.center)
            return

        velocity = self.velocity

        desired_velocity = (target_pos - current_pos).normalize() * self.maxspeed
        steer = (desired_velocity - velocity) * self.maxforce

        # If outcome parameter is True return the steering force
        if outcome:
            return steer
        else:
            new_velocity = velocity + steer
            self.velocity = new_velocity


    def avoid(self, flock, outcome=False):

        current_pos = self.pos
        optimal_distance = 50
        velocity = self.velocity

        steers = Vector2()
        count = 0
        for boid in flock:
            distance = point_distance(boid.pos, current_pos)
            if distance < optimal_distance and distance > 1:

                avoid_pos = boid.pos
                steering = (current_pos - avoid_pos) 
                steering = steering.normalize() / distance
                steers = steers + steering

                count += 1
        
        if steers.magnitude() != 0:
            mean_steering = steers / count
            mean_steering = mean_steering.normalize()

            desired_velocity = mean_steering * self.maxspeed
            steer = (desired_velocity - velocity) * self.maxforce

            if outcome:
                return steer
            else:
                new_velocity = velocity + steer
                self.velocity = new_velocity
        else:
            return steers


    def align(self, flock, outcome=False):
        current_pos = self.pos
        optimal_distance = 75
        velocity = self.velocity

        steers = Vector2()
        count = 0
        for boid in flock:
            distance = point_distance(boid.pos, current_pos)
            if distance < optimal_distance and distance > 1:

                steering = boid.velocity
                steering = steering.normalize() / distance
                steers = steers + steering

                count += 1
        
        if steers.magnitude() != 0:
            mean_steering = steers / count
            mean_steering = mean_steering.normalize()

            desired_velocity = mean_steering * self.maxspeed
            steer = (desired_velocity - velocity) * self.maxforce

            if outcome:
                return steer
            else:
                new_velocity = velocity + steer
                self.velocity = new_velocity
        else:
            return steers


    # Method that groups Seek, Avoid and Align in one to loop only once through the flock
    # Attempt at factorising the code
    def seek_avoid_align(self, flock):
        # Boid variables
        current_pos = self.pos
        velocity = self.velocity

        # Seek variables
        flock_pos = Vector2()

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

        return seek_force, avoid_force, align_force


    def escape(self, predators=None):

        if not predators:
            return Vector2()
        
        # Boid variables
        current_pos = self.pos
        velocity = self.velocity

        # escape variables
        escape_distance = 75
        escape_steers = Vector2()
        escape_count = 0
        
        for predator in predators:
            distance = point_distance(predator.pos, current_pos)

            # escape: escape steering for current boid
            if distance > 0 and distance < escape_distance:
                escape_steering = (current_pos - predator.pos) / distance
                escape_steering = escape_steering.normalize() 

                escape_steers += escape_steering
                escape_count += 1


        if escape_steers.magnitude() != 0:
            mean_escape = escape_steers / escape_count
            escape = mean_escape.normalize()

            desired_escape = escape * self.maxspeed
            escape_force = (desired_escape - velocity) * self.maxforce
        
        else:
            escape_force = escape_steers

        return escape_force


    # Method that calculates two vectors that are pointing in front of the boid. The first one's length is the view_distance and the other one's is half of the first
    def vision(self):

        velocity = self.velocity
        dist_coef = view_dist_coef(velocity, self.view_distance)

        self.ahead = (self.rect.centerx + velocity[0]*dist_coef, self.rect.centery + velocity[1]*dist_coef)
        self.ahead2 = (self.rect.centerx + velocity[0]*dist_coef*0.5, self.rect.centery + velocity[1]*dist_coef*0.5) # Is always half of ahead.


    def stay_in_enclave(self):

        current_pos = self.pos
        velocity = self.velocity

        if self.ahead[0] > self.surface_dim[0] or self.ahead[0] < 0 or self.ahead[1] > self.surface_dim[1] or self.ahead[1] < 0:
            if self.ahead[0] > self.surface_dim[0]:
                danger = Vector2(self.surface_dim[0], self.ahead[1])
                aim = danger - self.ahead
            elif self.ahead[0] < 0:
                danger = Vector2(0, self.ahead[1])
                aim = danger - self.ahead
            elif self.ahead[1] > self.surface_dim[1]:
                danger = Vector2(self.ahead[0], self.surface_dim[1])
                aim = danger - self.ahead
            elif self.ahead[1] < 0:
                danger = Vector2(self.ahead[0], 0)
                aim = danger - self.ahead

            distance = point_distance(current_pos, aim)
            stay_steering = (aim) / distance
            stay_steering = stay_steering.normalize()

            desired_stay = stay_steering * self.maxspeed
            stay_force = (desired_stay - velocity) * self.maxforce
            return stay_force

        else:
            return Vector2()
            

    def randomise_pos(self):

        self.init_pos = (randint(1, self.surface_dim[0]), randint(1, self.surface_dim[1]))
        self.rect = pygame.Rect(self.init_pos[0], self.init_pos[1], self.width, self.height)

        self.velocity = (randint(5, 8), randint(2, 360))


    def rebound(self, flock):
        
        # Principle :
        # Look at the distance between the boid and all colliding boids, the stearing force should be a factor of all avoidances force and the current velocity
        # Ends up generating rebounds more than steering
        optimal_distance = 30
        force_distance = np.array([self.velocity[0]])
        force_angle = np.array([self.velocity[1]])
        proximity = False
        for boid in flock:
            distance, x, y = point_distance(boid.rect.center, self.rect.center, True)
            if distance < optimal_distance and distance > 0:
                proximity = True
                force_normalised = Vector2(-1*x, -1*y).normalize().as_polar()
                force = (force_normalised[0]*abs(optimal_distance - distance), force_normalised[1])
                #force = (force_normalised[0], force_normalised[1] / distance)
                force_distance = np.append(force_distance, force[0])
                force_angle = np.append(force_angle, force[1])
        
        if proximity:
            self.velocity = (self.velocity[0], np.mean(force_angle))
            #diff = self.velocity[1] - np.mean(force_angle)
            #if diff / self.velocity[1] > 0.2:
            #    diff = self.velocity[1] * 0.2
            #self.velocity = (self.velocity[0], self.velocity[1] + diff)


