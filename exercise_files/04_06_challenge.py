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
        return round(point[0]) < 0 or round(point[0]) >= self._x or round(point[1]) < 0 or round(point[1]) >= self._y

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

    def forward(self):
        pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        if not self.canvas.hitsWall(pos):
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
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)

def run_scribes(canvas, scribe_data):
    for s_data in scribe_data:
        scribe = TerminalScribe(canvas)
        scribe.pos = s_data["start_pos"]
        scribe.setDegrees(s_data["degrees"])
        delay = s_data.get("delay", 0.1)

        for instr in s_data["instructions"]:
            if isinstance(instr, dict):
                # Support instructions with arguments like {'drawSquare': 5}
                for command, arg in instr.items():
                    getattr(scribe, command)(arg)
            else:
                getattr(scribe, instr)()
            time.sleep(delay)


canvas = Canvas(30, 30)

instructions = [
    {
        "start_pos": [5, 5],
        "degrees": 0,
        "instructions": ["forward", "forward", {"drawSquare": 3}],
        "delay": 0.1,
    },
    {
        "start_pos": [15, 15],
        "degrees": 90,
        "instructions": [
            "forward",
            "forward",
            "left",
            "forward",
            "right",
            {"drawSquare": 2},
        ],
        "delay": 0.05,
    },
    {"start_pos": [25, 25], "degrees": 225, "instructions": ["forward"] * 10},
]

run_scribes(canvas, instructions)

