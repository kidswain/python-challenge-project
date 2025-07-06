from .exceptions import TerminalScribeException, InvalidParameter
from utils.validation import is_number
import os, time, threading, json
from threading import Thread
from inspect import getmembers, ismethod


class Canvas:
    def __init__(self, width, height, scribes=[], framerate=0.05):
        if not is_number(width):
            raise InvalidParameter("Width must be a number")
        self._x = width
        if not is_number(height):
            raise InvalidParameter("Height must be a number")
        self._y = height
        self._canvas = [[" " for y in range(self._y)] for x in range(self._x)]
        self.scribes = scribes

        if not is_number(framerate):
            raise InvalidParameter("Framerate must be a number")
        self.framerate = framerate

    def toDict(self):
        return {
            "classname": type(self).__name__,
            "x": self._x,
            "y": self._y,
            "canvas": self._canvas,
            "scribes": [scribe.toDict() for scribe in self.scribes],
        }

    @staticmethod
    def fromDict(data):
        if not isinstance(data, dict):
            raise TerminalScribeException("Input to fromDict must be a dictionary")
        canvas_class = globals()[data["classname"]]
        scribes = []
        for scribe in data["scribes"]:
            scribe_classname = (
                scribe["classname"]
                if isinstance(scribe, dict)
                else getattr(scribe, "classname", None)
            )
            if not isinstance(scribe_classname, str):
                raise TerminalScribeException("Scribe classname is missing or invalid")
            scribe_class = globals()[scribe_classname]
            scribes.append(scribe_class.fromDict(scribe))
        canvas = canvas_class(data["x"], data["y"], scribes=scribes)
        canvas._canvas = data["canvas"]
        return canvas

    def toFile(self, name):
        with open(name + ".json", "w") as f:
            f.write(json.dumps(self.toDict()))

    @staticmethod
    def fromFile(name):
        with open(name + ".json", "r") as f:
            try:
                return Canvas.fromDict(json.loads(f.readline()))
            except:
                raise TerminalScribeException(
                    "File {}.json is not a valid Scribe file".format(name)
                )

    def hitsVerticalWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x

    def hitsHorizontalWall(self, point):
        return round(point[1]) < 0 or round(point[1]) >= self._y

    def hitsWall(self, point):
        return self.hitsVerticalWall(point) or self.hitsHorizontalWall(point)

    def getReflection(self, point):
        return [
            -1 if self.hitsVerticalWall(point) else 1,
            -1 if self.hitsHorizontalWall(point) else 1,
        ]

    def setPos(self, pos, mark):
        try:
            self._canvas[round(pos[0])][round(pos[1])] = mark
        except Exception as e:
            raise TerminalScribeException(str(e))

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def go(self):
        max_moves = max([len(scribe.moves) for scribe in self.scribes])
        for i in range(max_moves):
            for scribe in self.scribes:
                threads = []
                if len(scribe.moves) > i:
                    args = scribe.moves[i][1] + [self]
                    threads.append(Thread(target=scribe.moves[i][0], args=args))
                [thread.start() for thread in threads]
                [thread.join() for thread in threads]
            self.print()
            time.sleep(self.framerate)

    def print(self):
        self.clear()
        for y in range(self._y):
            print(" ".join([col[y] for col in self._canvas]))


class CanvasAxis(Canvas):
    # Pads 1-digit numbers with an extra space
    def formatAxisNumber(self, num):
        if num % 5 != 0:
            return "  "
        if num < 10:
            return " " + str(num)
        return str(num)

    def print(self):
        self.clear()
        for y in range(self._y):
            print(self.formatAxisNumber(y) + " ".join([col[y] for col in self._canvas]))

        print(" ".join([self.formatAxisNumber(x) for x in range(self._x)]))
