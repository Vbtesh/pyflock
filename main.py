import time
from random import randint
import pygame 
from scripts.boid import Boid
from scripts.predator import Predator
from scripts.attractor import Attractor
from scripts.interface import Slider
from scripts.wall import Enclave

def generate_vector():
    #return (8, randint(2, 360))
    return (randint(2, 3), randint(2, 360))
    #return (2, 45)


# Display dimensions
display_width = 800
display_height = 480 
dimensions = (display_width, display_height)

# Basic colors 
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

background_color = (95,158,160)
boid_colors = [(224,238,238), (127,255,212), (152,245,255)]
predator_colors = [(205,51,51), (238,59,59)]

# Flock of boids initialisation
boid_number = 130
boid_scale = 0.5
max_speed = 6
#flock = [Boid(boid_scale, boid_colors[randint(0, len(boid_colors)-1)], boid_vector, dimensions) for i in range(boid_number)]
#flock = [Boid(boid_scale, max_speed, boid_colors[randint(0, len(boid_colors)-1)], generate_vector(), dimensions) for i in range(boid_number)]
flock = [Boid(boid_scale, max_speed, boid_colors[randint(0, len(boid_colors)-1)], generate_vector(), dimensions) for i in range(2)]

# Predator list initialisation
predators = []

# Enclave initialisation
enclave = Enclave(dimensions, red)

# Attractor initialisation
attractor_num = 1
attractors = [Attractor((235, 210, 135), (display_width//2, display_height//2))]

# Slider
slider_pos = (10, 10)
slides = [Slider("Boids: ", boid_number, 1, 300, slider_pos)]

# Initialise main window
pygame.init()
font = pygame.font.SysFont("Verdana", 12)
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Boids")
clock = pygame.time.Clock()
screen.fill(background_color)
pygame.display.update()


# Set Mouse Buttons Values
LEFT = 1
RIGHT = 3

game_exit = False

while not game_exit:

    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            pos = pygame.mouse.get_pos()
            flock.append(Boid(boid_scale, max_speed, boid_colors[randint(0, len(boid_colors)-1)], generate_vector(), dimensions, pos))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            pos = pygame.mouse.get_pos()
            predators.append(Predator(boid_scale*3, max_speed, predator_colors[randint(0, len(predator_colors)-1)], generate_vector(), dimensions, pos))

        #    for s in slides:
        #        if s.button_rect.collidepoint(pos):
        #            s.hit = True
        #elif event.type == pygame.MOUSEBUTTONUP:
        #    for s in slides:
        #        s.hit = False

    #prev_boids = slides[0].val

    # Move slides
    #for s in slides:
    #    if s.hit:
    #        s.move()

    # Check if boid number has changed and make or destroy boids in accordance
    #if slides[0].val < prev_boids:
    #    for i in range(0, int(abs(slides[0].val - prev_boids))):
    #        flock.pop()
    #elif slides[0].val > prev_boids:
    #    for i in range(0, int(abs(slides[0].val - prev_boids))):
    #        flock.append(Boid(boid_scale, max_speed, black, generate_vector(), dimensions))

    screen.fill(background_color)

    # Adjust sliders' visual position
    #for s in slides:
    #    s.draw(screen)

    # Draw a rectangle in the middle of the screen that will serve as an attractor
    for a in attractors:
        #a.draw(screen)
        continue

    # Draw walls
    #enclave.draw(screen)

    # Update and draw boids
    for boid in flock:
        boid.accelerate(flock, predators)
        boid.update()
        boid.draw(screen)
        #boid.avoid(flock)
        #boid.seek(attractors[0])
        #boid.seek(flock, True)
        #boid.rebound(flock)

    for predator in predators:
        predator.accelerate(flock)
        predator.update()
        predator.draw(screen)
        flock = predator.eat(flock)
            
    pygame.display.flip()

    

