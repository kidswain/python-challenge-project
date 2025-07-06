from scribes import TerminalScribe, RobotScribe  # Ensure terminal_scribe.py is in the same directory or adjust the path accordingly
from canvas import Canvas  # Ensure canvas.py is in the same directory or adjust the path accordingly

scribe = TerminalScribe(color="green")
scribe.forward(10)
robotScribe = RobotScribe(color="yellow")
robotScribe.drawSquare(20)

canvas = Canvas(40, 40, scribes=[scribe, robotScribe])

canvas.toFile("solution_file")

newCanvas = Canvas.fromFile("solution_file")
newCanvas.go()
