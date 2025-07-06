import time
import os

def clear():
    # Clear the console screen
    os.system('cls' if os.name == 'nt' else 'clear')

for i in range (0,20):
    print("\n\n\n\n")
    print(" " * i + ".")
    time.sleep(0.1)
    clear()

class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def clear(self):
        # Clear the console screen
        os.system('cls' if os.name == 'nt' else 'clear')

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

canvas = Canvas(20, 20)
scribe = TerminalScribe(canvas)

for i in range(0, 10):
    for j in range(0, 10):
        scribe.draw((i, j))
        time.sleep(0.1)