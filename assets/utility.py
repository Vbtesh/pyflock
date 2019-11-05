from math import sqrt


def doughnut(x, y, dimensions):
    width = dimensions[0]
    height = dimensions[1]

    if x > width:
        new_x = 1
    elif x < 1:
        new_x = width - 1
    else:
        new_x = x

    if y > height:
        new_y = 1
    elif y < 1:
        new_y = height - 1
    else:
        new_y = y

    return (new_x, new_y)


def view_dist_coef(velocity, max_dist=100):
    dist = sqrt(velocity[0]**2 + velocity[1]**2)
    return max_dist / dist


def slope_intercept(p1, p2):
    try:
        slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
        return slope, p1[1] - slope * p1[0]
    except ZeroDivisionError:
        return None, None


def find_intercept(p1, p2, p3, p4):
    slope1, inter1 = slope_intercept(p1, p2)
    slope2, inter2 = slope_intercept(p3, p4)
    try:
        x = (inter1 - inter2) / (slope2 - slope1)
        y = slope1 * x + inter1
        return (x, y)
    except (ZeroDivisionError, TypeError):
        return None


def point_distance(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Basic colors 
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)