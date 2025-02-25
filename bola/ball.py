import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Moving Ball Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
ball_x = WINDOW_WIDTH // 2
ball_y = WINDOW_HEIGHT // 2
ball_radius = 20
ball_speed = 5
jump_speed = -15
gravity = 0.8

# Initial velocity
velocity_y = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Jump when spacebar is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ball_y >= WINDOW_HEIGHT - ball_radius:
                velocity_y = jump_speed

    # Get keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT]:
        ball_x += ball_speed
    if keys[pygame.K_UP]:
        ball_y -= ball_speed
    if keys[pygame.K_DOWN]:
        ball_y += ball_speed

    # Apply gravity
    velocity_y += gravity
    ball_y += velocity_y

    # Keep ball within screen bounds
    ball_x = max(ball_radius, min(ball_x, WINDOW_WIDTH - ball_radius))
    ball_y = max(ball_radius, min(ball_y, WINDOW_HEIGHT - ball_radius))

    # If ball hits the ground, stop vertical movement
    if ball_y >= WINDOW_HEIGHT - ball_radius:
        ball_y = WINDOW_HEIGHT - ball_radius
        velocity_y = 0

    # Clear screen
    screen.fill(WHITE)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    # Update display
    pygame.display.flip()

    # Control game speed
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()