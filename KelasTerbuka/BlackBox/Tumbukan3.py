import pygame
import sys
from pygame import Vector2

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 400
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)  # Warna untuk setelah tumbukan

# Physics parameters
m1 = 2000  # kg
m2 = 500  # kg
v1i = 120 / 3.6  # Convert 120 km/h to m/s
v2i = 0  # m/s

# Calculate final velocity using completely inelastic collision formula
v_final = (m1 * v1i + m2 * v2i) / (m1 + m2)  # = 96 km/h = 26.67 m/s

# Scale factor for visualization (pixels per meter)
SCALE = 2


class Box:
    def __init__(self, x, y, width, height, velocity):
        self.pos = Vector2(x, y)
        self.width = width
        self.height = height
        self.velocity = velocity
        self.color = RED
        self.collided = False

    def update(self):
        self.pos.x += self.velocity * SCALE / FPS

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.pos.x, self.pos.y, self.width, self.height))


class Circle:
    def __init__(self, x, y, radius, velocity):
        self.pos = Vector2(x, y)
        self.radius = radius
        self.velocity = velocity
        self.color = BLUE
        self.collided = False

    def update(self):
        self.pos.x += self.velocity * SCALE / FPS

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (int(self.pos.x), int(self.pos.y)), self.radius)


# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Completely Inelastic Collision Simulation")
clock = pygame.time.Clock()

# Create objects
box = Box(50, HEIGHT // 2 - 25, 50, 50, v1i)
circle = Circle(600, HEIGHT // 2, 25, v2i)

# Main game loop
running = True
collision_occurred = False

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for collision
    if not collision_occurred:
        box_right = box.pos.x + box.width
        circle_left = circle.pos.x - circle.radius

        if box_right >= circle_left:
            collision_occurred = True
            # After collision, both objects move together with the same velocity
            box.velocity = v_final
            circle.velocity = v_final
            # Change colors to indicate collision
            box.color = PURPLE
            circle.color = PURPLE

    # Update positions
    box.update()
    circle.update()

    # Draw
    screen.fill(WHITE)
    box.draw(screen)
    circle.draw(screen)

    # Display velocities
    font = pygame.font.Font(None, 36)
    velocity_kmh = box.velocity * 3.6  # Convert m/s to km/h
    if not collision_occurred:
        box_text = font.render(f"Box: {velocity_kmh:.1f} km/h", True, RED)
        circle_text = font.render(f"Circle: 0 km/h", True, BLUE)
    else:
        combined_text = font.render(f"Combined velocity: {velocity_kmh:.1f} km/h", True, PURPLE)
        screen.blit(combined_text, (10, 10))

    if not collision_occurred:
        screen.blit(box_text, (10, 10))
        screen.blit(circle_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()