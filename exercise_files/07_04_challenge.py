import os
import time
from termcolor import colored
import math
import random


class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[" " for _ in range(self._y)] for _ in range(self._x)]
        self._x_labels = {x: str(x) for x in range(0, self._x, 5)}
        self._y_labels = {y: str(y) for y in range(0, self._y, 5)}
        self._label_positions = set()
        self._compute_label_positions()

    def _compute_label_positions(self):
        for x in self._x_labels:
            self._label_positions.add((x, 0))  # Reserve X-axis label positions

    def hitsWall(self, point):
        x, y = round(point[0]), round(point[1])
        return x < 0 or x >= self._x or y < 0 or y >= self._y

    def getReflection(self, point):
        x, y = round(point[0]), round(point[1])
        return [-1 if x < 0 or x >= self._x else 1, -1 if y < 0 or y >= self._y else 1]

    def setPos(self, pos, mark):
        x, y = round(pos[0]), round(pos[1])
        if (x, y) in self._label_positions:
            return  # Avoid overwriting axis labels
        if 0 <= x < self._x and 0 <= y < self._y:
            self._canvas[x][y] = mark

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print(self):
        self.clear()
        for y in reversed(range(self._y)):
            label = (
                self._y_labels.get(y, "").rjust(3) + " "
                if y in self._y_labels
                else "    "
            )
            row = "".join(self._canvas[x][y] for x in range(self._x))
            print(label + row)
        # Print X-axis labels
        footer = "    "  # Padding for Y-axis
        for x in range(self._x):
            footer += self._x_labels.get(x, " ")
        print(footer)


class BaseScribe:
    def __init__(
        self,
        canvas,
        pos=[0, 0],
        direction=[0, 1],
        framerate=0.05,
        mark="*",
        trail=".",
        color="red",
    ):
        self.canvas = canvas
        self.pos = pos
        self.direction = direction
        self.framerate = framerate
        self.mark = mark
        self.trail = trail
        self.color = color

    def setPosition(self, pos):
        self.pos = pos

    def setDirection(self, direction):
        self.direction = direction

    def setDegrees(self, degrees):
        radians = math.radians(degrees)
        self.direction = [math.sin(radians), -math.cos(radians)]

    def setFramerate(self, framerate):
        self.framerate = framerate

    def setColor(self, color):
        self.color = color

    def draw(self, pos):
        # Draw the trail at the previous position in the same color
        colored_trail = colored(self.trail, self.color)
        self.canvas.setPos(self.pos, colored_trail)

        # Move to the new position and draw the mark
        self.pos = pos
        colored_mark = colored(self.mark, self.color)
        self.canvas.setPos(self.pos, colored_mark)

        self.canvas.print()
        time.sleep(self.framerate)

    def drawCircle(self, center, radius, steps=200):  # Increased from 100 to 200
        for i in range(steps + 1):
            angle = 2 * math.pi * i / steps
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            if not self.canvas.hitsWall([x, y]):
                self.draw([x, y])

    def drawLine(self, start, end, steps=50):
        for i in range(steps + 1):
            t = i / steps
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            if not self.canvas.hitsWall([x, y]):
                self.draw([x, y])

    def drawTriangle(self, p1, p2, p3):
        self.drawLine(p1, p2)
        self.drawLine(p2, p3)
        self.drawLine(p3, p1)

    def bounce(self, pos):
        reflection = self.canvas.getReflection(pos)
        self.direction = [
            self.direction[0] * reflection[0],
            self.direction[1] * reflection[1],
        ]

    def forward(self, distance):
        for _ in range(distance):
            next_pos = [
                self.pos[0] + self.direction[0],
                self.pos[1] + self.direction[1],
            ]
            if self.canvas.hitsWall(next_pos):
                self.bounce(next_pos)
                next_pos = [
                    self.pos[0] + self.direction[0],
                    self.pos[1] + self.direction[1],
                ]
            self.draw(next_pos)


class GraphingScribe(BaseScribe):
    def plotX(self, func):
        for x in range(self.canvas._x):
            y = func(x)
            if y is not None and not self.canvas.hitsWall([x, y]):
                self.draw([x, y])


class VectorScribe(BaseScribe):
    def move(self, steps=100, func=None):
        for _ in range(steps):
            if func:
                new_pos = func(self.pos[0], self.pos[1])
                if not self.canvas.hitsWall(new_pos):
                    self.draw(new_pos)


class RobotScribe(BaseScribe):
    def up(self):
        self.setDirection([0, -1])
        self.forward(1)

    def down(self):
        self.setDirection([0, 1])
        self.forward(1)

    def left(self):
        self.setDirection([-1, 0])
        self.forward(1)

    def right(self):
        self.setDirection([1, 0])
        self.forward(1)

    def drawSquare(self, size):
        for _ in range(size):
            self.right()
        for _ in range(size):
            self.down()
        for _ in range(size):
            self.left()
        for _ in range(size):
            self.up()


class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = "."
        self.mark = "*"
        self.framerate = 0.05
        self.pos = [0, 0]

        self.direction = [0, 1]

    def setPosition(self, pos):
        self.pos = pos

    def setDegrees(self, degrees):
        radians = (degrees / 180) * math.pi
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
        self.direction = [
            self.direction[0] * reflection[0],
            self.direction[1] * reflection[1],
        ]

    def forward(self, distance):
        for i in range(distance):
            pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            if self.canvas.hitsWall(pos):
                self.bounce(pos)
                pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            self.draw(pos)

    def plotX(self, function):
        for x in range(self.canvas._x):
            pos = [x, function(x)]
            if pos[1] and not self.canvas.hitsWall(pos):
                self.draw(pos)

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
        self.canvas.setPos(self.pos, colored(self.mark, "red"))
        # print(self.pos)
        self.canvas.print()
        time.sleep(self.framerate)


class WanderScribe(BaseScribe):
    def __init__(
        self,
        canvas,
        pos=[0, 0],
        angle=0,
        distance=100,
        framerate=0.05,
        mark="*",
        trail=".",
        color="blue",
    ):
        super().__init__(
            canvas, pos=pos, framerate=framerate, mark=mark, trail=trail, color=color
        )
        self.setDegrees(angle)
        self.total_distance = distance

    def wander(self):
        for _ in range(self.total_distance):
            next_pos = [
                self.pos[0] + self.direction[0],
                self.pos[1] + self.direction[1],
            ]
            if self.canvas.hitsWall(next_pos):
                self.bounce(next_pos)
                next_pos = [
                    self.pos[0] + self.direction[0],
                    self.pos[1] + self.direction[1],
                ]
            self.draw(next_pos)


def sine(x):
    return 5 * math.sin(x / 4) + 15


def cosine(x):
    return 5 * math.cos(x / 4) + 15


def circleTop(x):
    r, c = 10, 20
    if c - r < x < c + r:
        return c - math.sqrt(r**2 - (x - c) ** 2)


def circleBottom(x):
    r, c = 10, 20
    if c - r < x < c + r:
        return c + math.sqrt(r**2 - (x - c) ** 2)


def spiral(x, y):
    angle = math.atan2(y - 15, x - 20) + 0.2
    radius = math.hypot(x - 20, y - 15) + 0.5
    return [20 + radius * math.cos(angle), 15 + radius * math.sin(angle)]


def main():
    canvas = Canvas(60, 30)

    # Graphing
    g = GraphingScribe(canvas, color="cyan")
    g.plotX(sine)
    g.setColor("yellow")
    g.plotX(cosine)
    g.setColor("green")
    g.plotX(circleTop)
    g.plotX(circleBottom)

    # Robot
    scribe = RobotScribe(canvas, pos=[5, 5], color="magenta")
    scribe.drawSquare(10)
    scribe.setColor("white")
    scribe.setPosition([5, 5])
    scribe.drawCircle(center=[10, 10], radius=10)
    scribe.setPosition([20, 10])
    scribe.setColor("red")
    scribe.drawTriangle(p1=[20, 10], p2=[25, 15], p3=[15, 15])

    # Vector
    v = VectorScribe(canvas, pos=[20, 15], color="blue")
    v.move(steps=80, func=spiral)

    # Wanderer
    wanderer = WanderScribe(canvas, pos=[10, 10], angle=33, distance=250, color="grey")
    wanderer.wander()


if __name__ == "__main__":
    main()
