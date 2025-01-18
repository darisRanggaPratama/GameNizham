import pygame
import random
import math
from time import time

# Initialize Pygame
pygame.init()

# Display settings
winHeight = 600
winWidth = 600
window = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Shape Shifter Game")

# Object properties
x = 300
y = 300
height = 20
width = 20
speed = 1

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def draw_pentagon(surface, color, x, y, size):
    points = []
    for i in range(5):
        angle = math.radians(i * 72 - 18)  # -18 to rotate slightly
        points.append((
            x + size * math.cos(angle),
            y + size * math.sin(angle)
        ))
    pygame.draw.polygon(surface, color, points)

def draw_triangle(surface, color, x, y, size):
    points = [
        (x, y - size),  # Top
        (x - size, y + size),  # Bottom left
        (x + size, y + size)  # Bottom right
    ]
    pygame.draw.polygon(surface, color, points)
    # Draw glowing border
    for i in range(3):
        glow_color = (min(color[0] + 50, 255), 
                     min(color[1] + 50, 255), 
                     min(color[2] + 50, 255))
        pygame.draw.lines(surface, glow_color, True, points, 2 - i)

# Game loop
clock = pygame.time.Clock()
current_color = RED
shape_type = "rectangle"  # Default shape
last_color_change = time()
color_change_interval = 0.2  # Seconds between color changes

running = True
while running:
    # Delay for consistent frame rate
    clock.tick(60)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keyboard input
    keys = pygame.key.get_pressed()
    
    # Movement and color logic
    if keys[pygame.K_LEFT] and x > 0:
        x -= speed
        current_color = BLACK
        
    if keys[pygame.K_RIGHT] and x < winWidth - width:
        x += speed
        current_color = RED
        
    if keys[pygame.K_DOWN] and y < winHeight - height:
        y += speed
        current_color = BLUE
        
    if keys[pygame.K_UP] and y > 0:
        y -= speed
        current_color = GREEN

    # Special combinations
    if (keys[pygame.K_LEFT] and keys[pygame.K_UP]) or (keys[pygame.K_UP] and keys[pygame.K_RIGHT]):
        shape_type = "pentagon"
        if time() - last_color_change >= color_change_interval:
            current_color = get_random_color()
            last_color_change = time()
    
    elif (keys[pygame.K_LEFT] and keys[pygame.K_DOWN]) or (keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]):
        shape_type = "triangle"
        if time() - last_color_change >= color_change_interval:
            current_color = get_random_color()
            last_color_change = time()
    
    else:
        shape_type = "rectangle"

    # Drawing
    window.fill(WHITE)
    
    if shape_type == "rectangle":
        pygame.draw.rect(window, current_color, (x, y, height, width))
    elif shape_type == "pentagon":
        draw_pentagon(window, current_color, x + width//2, y + height//2, max(height, width))
    elif shape_type == "triangle":
        draw_triangle(window, current_color, x + width//2, y + height//2, max(height, width))
    
    # Update display
    pygame.display.update()

# Quit game
pygame.quit()
