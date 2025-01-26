# file: ui.py
import pygame as pg
from logic import Circle, Line


class GameUI:
    """Class to manage the PyGame UI."""
    def __init__(self, width, height):
        # Initialize PyGame and screen settings
        pg.init()
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((self.width, self.height))
        # Window title
        pg.display.set_caption("Basic Window: OOP")
        # Logo/icon
        icon = pg.image.load("cat.png")
        pg.display.set_icon(icon)
        self.clock = pg.time.Clock()
        self.running = True

        # Colors
        self.lightCoral = (240, 128, 128)
        self.lavender = (230, 230, 250)
        self.indigo = (75, 0, 130)

        # Background color
        self.background_color = self.lightCoral  # lightCoral

        # Create game objects
        self.circle = Circle(250, 400, 49, self.lavender)  # lavender
        self.line = Line(250, 400, 50, 5, self.indigo)  # indigo

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Limit FPS to 60

        pg.quit()

    def handle_events(self):
        """Handle events like quitting the game."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        """Update game state."""
        pass  # No dynamic updates in this example

    def draw(self):
        """Draw everything on the screen."""
        self.screen.fill(self.background_color)  # Fill background
        self.draw_circle(self.circle)
        self.draw_line(self.line)
        pg.display.update()

    def draw_circle(self, circle):
        """Draw the circle on the screen."""
        pg.draw.circle(self.screen, circle.color, (circle.x, circle.y), circle.radius)

    def draw_line(self, line):
        """Draw the line on the screen."""
        start_pos = (line.x, line.y - line.length)
        end_pos = (line.x, line.y + line.length)
        pg.draw.line(self.screen, line.color, start_pos, end_pos, line.width)
