import math


def sine(x):
    return 5 * math.sin(x / 4) + 15


def cosine(x):
    return 5 * math.cos(x / 4) + 15


def circleTop(x):
    radius = 10
    center = 20
    if x > center - radius and x < center + radius:
        return center - math.sqrt(radius**2 - (x - center) ** 2)


def circleBottom(x):
    radius = 10
    center = 20
    if x > center - radius and x < center + radius:
        return center + math.sqrt(radius**2 - (x - center) ** 2)
