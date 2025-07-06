import unittest
import os
from canvas.base import CanvasAxis
from scribes.base import TerminalScribe
from scribes.robot import RobotScribe
from utils.io import save_canvas_to_json, load_canvas_from_json


class TestSerialization(unittest.TestCase):
    def setUp(self):
        self.scribe = TerminalScribe(color="green")
        self.scribe.forward(10)

        self.robot = RobotScribe(color="yellow")
        self.robot.drawSquare(5)

        self.canvas = CanvasAxis(40, 40, scribes=[self.scribe, self.robot])
        self.test_file = "test_canvas.json"

    def test_save_and_load_canvas(self):
        save_canvas_to_json(self.canvas, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        loaded = load_canvas_from_json(self.test_file)
        self.assertEqual(len(loaded.scribes), 2)
        self.assertEqual(loaded._x, 40)
        self.assertEqual(loaded._y, 40)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
