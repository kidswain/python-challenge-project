import json
# Update the import path below if 'Canvas' is located elsewhere
from canvas import Canvas, CanvasAxis


def save_canvas_to_json(canvas, filename):
    with open(filename, "w") as f:
        json.dump(canvas.toDict(), f, indent=2)


def load_canvas_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return Canvas.fromDict(data)
