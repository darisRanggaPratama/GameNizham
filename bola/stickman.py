import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Stickman Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Stickman properties
class Stickman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.jump_speed = -15
        self.velocity_y = 0
        self.gravity = 0.8
        self.is_jumping = False

    def draw(self):
        # Head
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 15)
        # Body
        pygame.draw.line(screen, BLACK, (self.x, self.y + 15), (self.x, self.y + 50), 2)
        # Arms
        pygame.draw.line(screen, BLACK, (self.x - 20, self.y + 30), (self.x + 20, self.y + 30), 2)
        # Legs
        pygame.draw.line(screen, BLACK, (self.x, self.y + 50), (self.x - 15, self.y + 80), 2)
        pygame.draw.line(screen, BLACK, (self.x, self.y + 50), (self.x + 15, self.y + 80), 2)

    def move(self, keys):
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Jump
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = self.jump_speed
            self.is_jumping = True

        # Apply gravity
        if self.is_jumping:
            self.y += self.velocity_y
            self.velocity_y += self.gravity

            # Check if landed
            if self.y >= WINDOW_HEIGHT - 100:
                self.y = WINDOW_HEIGHT - 100
                self.is_jumping = False
                self.velocity_y = 0

        # Keep stickman within screen bounds
        self.x = max(20, min(self.x, WINDOW_WIDTH - 20))
        self.y = max(20, min(self.y, WINDOW_HEIGHT - 100))

# Create stickman
stickman = Stickman(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get keyboard input
    keys = pygame.key.get_pressed()
    
    # Clear screen
    screen.fill(WHITE)
    
    # Update and draw stickman
    stickman.move(keys)
    stickman.draw()
    
    # Update display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(60)