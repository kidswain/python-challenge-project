import unittest
from canvas.base import Canvas
from scribes.base import TerminalScribe


class TestCanvas(unittest.TestCase):
    def test_canvas_bounds(self):
        canvas = Canvas(10, 10)
        self.assertTrue(canvas.hitsWall([-1, 5]))
        self.assertTrue(canvas.hitsWall([5, 10]))
        self.assertFalse(canvas.hitsWall([5, 5]))

    def test_set_and_get_position(self):
        canvas = Canvas(10, 10)
        scribe = TerminalScribe(color="blue")
        scribe.setPosition([5, 5])
        scribe.forward(1)
        canvas.scribes.append(scribe)
        canvas.go()
