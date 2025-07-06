import unittest
from scribes.plot import PlotScribe
from utils.functions import sine
from canvas.base import Canvas


class TestPlotScribe(unittest.TestCase):
    def test_plot_sine(self):
        scribe = PlotScribe(domain=[0, 10], color="cyan")
        scribe.plotX(sine)
        self.assertGreater(len(scribe.moves), 0)

        canvas = Canvas(20, 20, scribes=[scribe])
        canvas.go()
