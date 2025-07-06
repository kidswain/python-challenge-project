from pdb import main
import math
import time
import os


def clear():
    # Clear the console screen
    os.system("cls" if os.name == "nt" else "clear")


class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[" " for y in range(self._y)] for x in range(self._x)]

    def clear(self):
        # Clear the console screen
        os.system("cls" if os.name == "nt" else "clear")

    def setPos(self, pos, mark):
        self._canvas[pos[0]][pos[1]] = mark

    def print(self):
        self.clear()
        for y in range(self._y):
            print([" ".join(col[y] for col in self._canvas)])

    def draw(self):
        for row in self._canvas:
            print("".join(row))

    def set_pixel(self, x, y, char):
        if 0 <= x < self._x and 0 <= y < self._y:
            self._canvas[y][x] = char


class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.pos = [0, 0]  # Initial position at the top-left corner

        self.mark = "*"
        self.trail = "."

    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, self.mark)
        self.canvas.print()


def drawCircle(scribe, radius, delay=0.05, num_points=100):
    cx, cy = scribe.pos  # Circle center at current position

    for i in range(num_points + 1):
        angle = 2 * math.pi * i / num_points
        x = int(round(cx + radius * math.cos(angle)))
        y = int(round(cy + radius * math.sin(angle)))
        scribe.draw((x, y))
        time.sleep(delay)


def drawSquare(scribe, size, delay=0.1):
    x, y = scribe.pos  # starting position
    # Top side
    for i in range(size):
        scribe.draw((x + i, y))
        time.sleep(delay)
    # Right side
    for i in range(1, size):
        scribe.draw((x + size - 1, y + i))
        time.sleep(delay)
    # Bottom side
    for i in range(1, size):
        scribe.draw((x + size - 1 - i, y + size - 1))
        time.sleep(delay)
    # Left side
    for i in range(1, size - 1):
        scribe.draw((x, y + size - 1 - i))
        time.sleep(delay)


def main():

    # for i in range (0,20):
    #     print("\n\n\n\n")
    #     print(" " * i + ".")
    #     time.sleep(0.1)
    #     clear()

    clear()
    canvas = Canvas(20, 20)
    scribe = TerminalScribe(canvas)
    drawSquare(scribe, 5)
    time.sleep(10)
    scribe.pos = [10, 10]
    drawCircle(scribe, 5)

    # for i in range(0, 10):
    #     for j in range(0, 10):
    #         scribe.draw((i, j))
    #         time.sleep(0.1)


if __name__ == "__main__":
    main()
