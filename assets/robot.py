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
        self.view = self.vision()
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
        
        # Generate two vectors for each points
        #if self.velocity[1] > 160:
        #    left_angle = self.velocity[1] - 160
        #else:
        #    left_angle = self.velocity[1] + 160
        #
        #if self.velocity[1] > 200:
        #    right_angle = self.velocity[1] - 200
        #else:
        #    right_angle = self.velocity[1] + 200

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
        self.view = self.vision()
        #self.boundaries = [self.rect.midtop, self.rect.bottomright, self.rect.bottomleft]
        self.boundaries = self.calcnewbounds(self.rect)
        #self.boundaries = [self.calcnewbounds(self.rect, offset)[0], self.rect.bottomright, self.rect.bottomleft]


    def calcnewpos(self, rect, vector):

        offset = Vector2()
        offset.from_polar(vector)

        return rect.move(offset[0], offset[1])


    def vision(self, view_angle=141):

        velocity = Vector2()
        velocity.from_polar(self.velocity)
        self.ahead = (self.rect.centerx + velocity[0]*view_dist_coef(velocity), self.rect.centery + velocity[1]*view_dist_coef(velocity))
        self.ahead2 = (self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.5, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.5))

        left_vision = []
        for angle in range(0, view_angle, 10):
            velocity = Vector2()
            velocity.from_polar((self.velocity[0], self.velocity[1] + angle))
            
            ahead = []
            ahead.append((self.rect.centerx + velocity[0]*view_dist_coef(velocity), self.rect.centery + velocity[1]*view_dist_coef(velocity)))
            ahead.append((self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.80, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.80)))
            ahead.append((self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.60, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.60)))
            ahead.append((self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.40, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.40)))
            ahead.append((self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.20, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.20)))
            ahead.append((self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.10, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.10)))

            left_vision.append(ahead)

        right_vision = []
        for angle in range(0, view_angle, 10):
            velocity = Vector2()
            velocity.from_polar((self.velocity[0], self.velocity[1] - angle))

            ahead = []
            ahead.append((self.rect.centerx + velocity[0]*view_dist_coef(velocity), self.rect.centery + velocity[1]*view_dist_coef(velocity)))
            ahead.append((self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.80, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.80)))
            ahead.append((self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.60, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.60)))
            ahead.append((self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.40, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.40)))
            ahead.append((self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.20, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.20)))
            ahead.append((self.rect.centerx + (velocity[0]*view_dist_coef(velocity))*0.10, self.rect.centery + (velocity[1]*view_dist_coef(velocity)*0.10)))

            right_vision.append(ahead)

        vision = [view for view in reversed(left_vision)]
        vision += right_vision[1:]

        return vision


    def adjust_velocity(self, new_direction):
        velocity = Vector2()
        velocity.from_polar(self.velocity)
        adjust = Vector2(new_direction)
        self.velocity = Vector2(velocity[0] + adjust[0], velocity[1] + adjust[1]).as_polar()


    def check_collision(self, boid, surface):

        #if pygame.sprite.collide_circle(self, boid):
        #    pygame.draw.line(surface, (255,0,0), self.rect.center, boid.rect.center, 1)
        #    avoidance = ()
        
        intercept = find_intercept(self.rect.center, self.ahead, boid.rect.center, boid.ahead)
        if intercept:
            crash_distance = point_distance(self.rect.center, intercept)
            if crash_distance < 50:
                avoidance = (self.ahead2[0] - intercept[0], self.ahead2[1] - intercept[1])
                self.adjust_velocity(avoidance)


    def observe(self, flock):
        
        in_view = []
        close_flock = [boid for boid in flock if pygame.sprite.collide_circle(self, boid)]
        for boid in close_flock:
            for ray in self.view:
                size_ray = ray[0]
                for close, point in zip(range(len(ray), ray)):
                    if boid.rect.collidepoint(point):
                        size_ray = ray[close]
                in_view.append(size_ray)


            


