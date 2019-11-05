from random import randint
from pygame.math import Vector2
import pygame

if __name__ == "__main__":
    from utility import doughnut, view_dist_coef, find_intercept, point_distance, slope_intercept
else:
    from assets.utility import doughnut, view_dist_coef, find_intercept, point_distance, slope_intercept


class Boid(pygame.sprite.Sprite):

    def __init__(self, scale, color, vector, dimensions):
        pygame.sprite.Sprite.__init__(self)
        self.init_pos = (randint(1, dimensions[0]), randint(1, dimensions[1]))
        #self.init_pos = (dimensions[0]/2, dimensions[1]/2)
        self.surface_dim = dimensions

        self.color = color

        self.scale = scale
        self.height = int(15*scale // 1)
        self.width = int(10*scale // 1)

        self.rect = pygame.Rect(self.init_pos[0], self.init_pos[1], self.width, self.height)
        self.boundaries = [self.rect.midtop, self.rect.bottomleft, self.rect.bottomright]

        self.velocity = vector
        self.vision()
        self.radius = point_distance(self.rect.center, self.ahead2)


    def draw(self, surface):

        pygame.draw.polygon(surface, self.color, self.boundaries)
        #for ray in self.view:
        #    pygame.draw.line(surface, self.color, self.rect.center, ray[0], 1)

        #pygame.draw.circle(surface, self.color, self.rect.center, 100, 1)
        #pygame.draw.line(surface, self.color, self.rect.center, self.ahead, 1)

        #pygame.draw.aalines(surface, self.color, True, self.boundaries)
        
        #pygame.draw.circle(surface, white, (int(self.boundaries[0][0]), int(self.boundaries[0][1])), 2)
        #pygame.draw.circle(surface, red, (int(self.boundaries[1][0]), int(self.boundaries[1][1])), 2)
        #pygame.draw.circle(surface, blue, (int(self.boundaries[2][0]), int(self.boundaries[2][1])), 2)


    def calcnewbounds(self, rect):
        # Tip of the boid
        head = rect.center

        left_angle = self.velocity[1] + 160
        right_angle = self.velocity[1] + 200

        left_vector = Vector2()
        left_vector.from_polar((15, left_angle))
        right_vector = Vector2()
        right_vector.from_polar((15, right_angle))
        

        # Apply offset and return new boundaries
        left_wing = (head[0] + left_vector[0], head[1] + left_vector[1])
        right_wing = (head[0] + right_vector[0], head[1] + right_vector[1])
        

        return [head, left_wing, right_wing]


    def update(self):
        
        newpos = self.calcnewpos(self.rect, self.velocity)
        # Treat space as a doughnut
        (x, y) =  doughnut(newpos.centerx, newpos.centery, (self.surface_dim))
        newpos.centerx, newpos.centery, newpos.center = x, y, (x, y)

        self.rect = newpos
        self.vision()
        #self.boundaries = [self.rect.midtop, self.rect.bottomright, self.rect.bottomleft]
        self.boundaries = self.calcnewbounds(self.rect)
        #self.boundaries = [self.calcnewbounds(self.rect, offset)[0], self.rect.bottomright, self.rect.bottomleft]


    def calcnewpos(self, rect, vector):

        offset = Vector2()
        offset.from_polar(vector)

        return rect.move(offset[0], offset[1])


    def vision(self):

        velocity = Vector2()
        velocity.from_polar(self.velocity)
        dist_coef = view_dist_coef(velocity, 100)

        self.ahead = (self.rect.centerx + velocity[0]*dist_coef, self.rect.centery + velocity[1]*dist_coef)
        self.ahead2 = (self.rect.centerx + velocity[0]*dist_coef*0.5, self.rect.centery + velocity[1]*dist_coef*0.5) # Is always half of ahead.


    def adjust_velocity(self, new_direction):
        velocity = Vector2()
        velocity.from_polar(self.velocity)
        adjust = Vector2(new_direction)
        self.velocity = Vector2(velocity[0] + adjust[0], velocity[1] + adjust[1]).as_polar()


    def avoid_collision(self, boid):
        
        optimal_distance = 30
        if pygame.sprite.collide_circle(self, boid):




            


