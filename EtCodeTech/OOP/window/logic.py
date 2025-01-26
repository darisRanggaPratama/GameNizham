# file: logic.py
class Circle:
    """Class to manage circle data."""
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


class Line:
    """Class to manage line data."""
    def __init__(self, x, y, length, width, color):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.color = color