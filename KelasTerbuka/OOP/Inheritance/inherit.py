import pygame as pg
import sys

# Initialize Pygame
pg.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Inheritance")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Basic Class
class Shape:
    def __init__(self, color):
        self.color = color

    def area(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def perimeter(self):
        raise NotImplementedError("Subclass must implement abstract method")


class Square(Shape):
    def __init__(self, side, color):
        super().__init__(color)
        self.side = side

    def area(self):
        return self.side ** 2

    def perimeter(self):
        return 4 * self.side


class Rectangle(Shape):
    def __init__(self, width, height, color):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, base, height, color):
        super().__init__(color)
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

    def perimeter(self):
        return 2 * (self.base + self.height)


class Circle(Shape):
    def __init__(self, side, color):
        super().__init__(color)
        self.side = side

    def area(self):
        return 3.14 * self.side ** 2

    def perimeter(self):
        return 2 * 3.14 * self.side


# Using class
shapes = [Square(100, YELLOW),
          Rectangle(150, 80, RED),
          Triangle(100, 80, BLUE),
          Circle(50, GREEN)]


# Functions: Create shapes
def draw_shapes(shapes):
    screen.fill(WHITE)
    y_offset = 50

    for shape in shapes:
        if isinstance(shape, Square):
            pg.draw.rect(screen, shape.color, (100, y_offset, shape.side, shape.side))
            text = f"Square: Area = {shape.area()}, Perimeter = {shape.perimeter()}"
        elif isinstance(shape, Rectangle):
            pg.draw.rect(screen, shape.color, (300, y_offset, shape.width, shape.height))
            text = f"Rectangle: Area = {shape.area()}, Perimeter = {shape.perimeter()}"
        elif isinstance(shape, Triangle):
            pg.draw.polygon(screen, shape.color, [(400, y_offset + shape.height), (400 - shape.base // 2, y_offset),
                                                  (400 + shape.base // 2, y_offset)])
            text = f"Triangle: Area = {shape.area()}, Perimeter = {shape.perimeter()}"
        elif isinstance(shape, Circle):
            pg.draw.circle(screen, shape.color, (600, y_offset + shape.side), shape.side)
            text = f"Circle: Area = {shape.area()}, Perimeter = {shape.perimeter()}"
        else:
            raise ValueError("Invalid shape type")

        # Show text
        font = pg.font.Font(None, 36)
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (50, y_offset + 20))
        y_offset += 100

    pg.display.flip()


# Main loop
def main():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        draw_shapes(shapes)


# Run program
if __name__ == "__main__":
    main()
