import os
import time
from termcolor import colored
import math 


class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def hitsWall(self, point):
        x, y = round(point[0]), round(point[1])
        if x < 0 or x >= self._x:
           return [1, 0]  # normal for vertical wall
        if y < 0 or y >= self._y:
           return [0, 1]  # normal for horizontal wall
        return None

    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))

class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.05
        self.pos = [0, 0]

        self.direction = [0, 1]

    def setDegrees(self, degrees):
        radians = (degrees/180) * math.pi 
        self.direction = [math.sin(radians), -math.cos(radians)]

    def up(self):
        self.direction = [0, -1]
        self.forward()

    def down(self):
        self.direction = [0, 1]
        self.forward()

    def right(self):
        self.direction = [1, 0]
        self.forward()

    def left(self):
        self.direction = [-1, 0]
        self.forward()

    def forward(self, distance=1):
        for _ in range(distance):
            next_pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            normal = self.canvas.hitsWall(next_pos)

            if normal:
                # Reflect direction: R = D - 2 * (D ⋅ N) * N
                dot = self.direction[0]*normal[0] + self.direction[1]*normal[1]
                self.direction[0] -= 2 * dot * normal[0]
                self.direction[1] -= 2 * dot * normal[1]
                next_pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]

        self.draw(next_pos)

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

canvas = Canvas(30, 30)
scribe = TerminalScribe(canvas)
scribe.setDegrees(150)
for i in range(100):
    scribe.forward()

