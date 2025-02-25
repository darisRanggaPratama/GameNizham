import pygame
import sys
from game import Game

pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Impact")

# Initialize clock
clock = pygame.time.Clock()
FPS = 60

# Create game instance
game = Game(screen)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_input(event)
    
    # Update game state
    game.update()
    
    # Draw everything
    screen.fill((0, 0, 0))  # Fill screen with black
    game.draw()
    pygame.display.flip()
    
    # Control game speed
    clock.tick(FPS)