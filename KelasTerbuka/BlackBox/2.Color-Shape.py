import pygame

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Window title
pygame.display.set_caption("Color & Shape")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw rectangles
    pygame.draw.rect(screen, RED, (50, 50, 100, 100))
    pygame.draw.rect(screen, ORANGE, (200, 50, 100, 100))
    pygame.draw.rect(screen, BROWN, (350, 50, 100, 100))

    # Draw circles
    pygame.draw.circle(screen, RED, (50, 250), 50)
    pygame.draw.circle(screen, ORANGE, (200, 250), 50)
    pygame.draw.circle(screen, BROWN, (350, 250), 50)

    # Draw lines
    pygame.draw.line(screen, RED, (50, 450), (150, 450), 5)
    pygame.draw.line(screen, ORANGE, (200, 450), (300, 450), 5)
    pygame.draw.line(screen, BROWN, (350, 450), (450, 450), 5)


    # Update the display
    pygame.display.flip()
