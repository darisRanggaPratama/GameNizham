import pygame as pg

class Game:
    def __init__(self, width, height):
        # Initialize pygame and game settings
        pg.init()
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Window Basic: OOP")
        self.clock = pg.time.Clock()
        self.running = True

        # Background color
        self.background_color = (240, 128, 128)  # lightCoral

        # Create game objects
        self.circle = Circle(250, 400, 49, (230, 230, 250))  # lavender
        self.line = Line(250, 400, 50, 5, (75, 0, 130))  # indigo

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
        self.circle.draw(self.screen)
        self.line.draw(self.screen)
        pg.display.update()


class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface):
        """Draw the circle on the given surface."""
        pg.draw.circle(surface, self.color, (self.x, self.y), self.radius)


class Line:
    def __init__(self, x, y, length, width, color):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.color = color

    def draw(self, surface):
        """Draw the line on the given surface."""
        start_pos = (self.x, self.y - self.length)
        end_pos = (self.x, self.y + self.length)
        pg.draw.line(surface, self.color, start_pos, end_pos, self.width)


# Main entry point
if __name__ == "__main__":
    game = Game(800, 600)
    game.run()
