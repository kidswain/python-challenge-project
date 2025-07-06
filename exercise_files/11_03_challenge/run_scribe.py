import sys
from utils.io import load_canvas_from_json


def main():
    if len(sys.argv) != 2:
        print("Usage: python run_scribe.py <canvas_file.json>")
        return

    filename = sys.argv[1]
    try:
        canvas = load_canvas_from_json(filename)
        canvas.go()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
