import os
import time
from termcolor import colored
import math 


class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def hitsVerticalWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x

    def hitsHorizontalWall(self, point):
        return round(point[1]) < 0 or round(point[1]) >= self._y

    def hitsWall(self, point):
        return self.hitsVerticalWall(point) or self.hitsHorizontalWall(point)

    def getReflection(self, point):
        return [-1 if self.hitsVerticalWall(point) else 1, -1 if self.hitsHorizontalWall(point) else 1]

    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))

    def draw_axes(self):
        mid_y = self._y // 2
        mid_x = self._x // 2
        for x in range(self._x):
            self._canvas[x][mid_y] = '-'  # X-axis
        for y in range(self._y):
            self._canvas[mid_x][y] = '|'  # Y-axis
        self._canvas[mid_x][mid_y] = '+'  # Origin

    def add_title(self, title):
        for i, char in enumerate(title):
            if i < self._x:
                self._canvas[i][0] = char

class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.05
        self.pos = [0, 0]

        self.direction = [0, 1]

    def setPosition(self, pos):
        self.pos = pos

    def setDegrees(self, degrees):
        radians = (degrees/180) * math.pi 
        self.direction = [math.sin(radians), -math.cos(radians)]

    def up(self):
        self.direction = [0, -1]
        self.forward(1)

    def down(self):
        self.direction = [0, 1]
        self.forward(1)

    def right(self):
        self.direction = [1, 0]
        self.forward(1)

    def left(self):
        self.direction = [-1, 0]
        self.forward(1)

    def bounce(self, pos):
        reflection = self.canvas.getReflection(pos)
        self.direction = [self.direction[0] * reflection[0], self.direction[1] * reflection[1]]

    def forward(self, distance):
        for i in range(distance):
            pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            if self.canvas.hitsWall(pos):
                self.bounce(pos)
                pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            self.draw(pos)

    def plotX(self, func, x_range):
        for x in x_range:
            y = func(x)
            if not self.canvas.hitsWall([x, y]):
                self.draw([x, y])

    def plotXY(self, func, steps=100):
        for _ in range(steps):
            new_pos = func(self.pos[0], self.pos[1])
            if not self.canvas.hitsWall(new_pos):
                self.draw(new_pos)

    def drawSquare(self, size):
        for i in range(size):
            self.right()
        for i in range(size):
            self.down()
        for i in range(size):
            self.left()
        for i in range(size):
            self.up()

    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)

def sine(x):
    return 5 * math.sin(x / 4) + 10  # Scaled and shifted to fit canvas

def cosine(x):
    return 5 * math.cos(x / 4) + 10  # Scaled and shifted to fit the canvas

def spiral(x, y):
    angle = math.atan2(y - 15, x - 15) + 0.2
    radius = math.hypot(x - 15, y - 15) + 0.5
    return [15 + radius * math.cos(angle), 15 + radius * math.sin(angle)]


canvas = Canvas(60, 60)
canvas.draw_axes()
canvas.add_title("Cosine, Sine and Spiral Waves")

scribe1 = TerminalScribe(canvas)
scribe1.setPosition([0, 15])
scribe2 = TerminalScribe(canvas)
scribe2.setPosition([30, 15])
scribe3 = TerminalScribe(canvas)
scribe3.setPosition([0, 15])

# Plot sine wave
scribe1.plotX(sine, range(60))

# Plot spiral
scribe2.plotXY(spiral, steps=100)

# Plot cosine wave
scribe3.plotX(cosine, range(60))
