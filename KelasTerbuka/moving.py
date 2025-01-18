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

# Black hole properties
idle_timer = 0
idle_threshold = 2  # Seconds before black hole appears
black_hole_radius = 0
max_black_hole_radius = 300
black_hole_growth_speed = 2
black_hole_active = False
game_over = False

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def draw_pentagon(surface, color, x, y, size):
    points = []
    for i in range(5):
        angle = math.radians(i * 72 - 18)
        points.append((
            x + size * math.cos(angle),
            y + size * math.sin(angle)
        ))
    pygame.draw.polygon(surface, color, points)

def draw_triangle(surface, color, x, y, size):
    points = [
        (x, y - size),
        (x - size, y + size),
        (x + size, y + size)
    ]
    pygame.draw.polygon(surface, color, points)
    for i in range(3):
        glow_color = (min(color[0] + 50, 255), 
                     min(color[1] + 50, 255), 
                     min(color[2] + 50, 255))
        pygame.draw.lines(surface, glow_color, True, points, 2 - i)

def draw_black_hole(surface, center_x, center_y, radius):
    # Draw multiple circles with different colors for the black hole effect
    colors = [
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
        for _ in range(5)
    ]
    
    # Draw outer glowing rings
    for i in range(5):
        outer_radius = radius - (i * 10)
        if outer_radius > 0:
            pygame.draw.circle(surface, colors[i], (center_x, center_y), outer_radius)
    
    # Draw the black center
    pygame.draw.circle(surface, BLACK, (center_x, center_y), max(radius - 50, 0))
    
    # Add twinkling stars effect around the black hole
    for _ in range(20):
        star_x = center_x + random.randint(-int(radius*1.2), int(radius*1.2))
        star_y = center_y + random.randint(-int(radius*1.2), int(radius*1.2))
        star_color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        pygame.draw.circle(surface, star_color, (star_x, star_y), random.randint(1, 3))

def draw_game_over(surface):
    font = pygame.font.Font(None, 74)
    text = font.render('GAME OVER', True, RED)
    text_rect = text.get_rect(center=(winWidth/2, winHeight/2))
    surface.blit(text, text_rect)

# Game loop
clock = pygame.time.Clock()
current_color = RED
shape_type = "rectangle"
last_color_change = time()
color_change_interval = 0.2
last_position = (x, y)
last_movement_time = time()

running = True
while running:
    clock.tick(60)
    current_time = time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        moved = False
        
        if keys[pygame.K_LEFT] and x > 0:
            x -= speed
            current_color = BLACK
            moved = True
            
        if keys[pygame.K_RIGHT] and x < winWidth - width:
            x += speed
            current_color = RED
            moved = True
            
        if keys[pygame.K_DOWN] and y < winHeight - height:
            y += speed
            current_color = BLUE
            moved = True
            
        if keys[pygame.K_UP] and y > 0:
            y -= speed
            current_color = GREEN
            moved = True

        # Check for special combinations
        if (keys[pygame.K_LEFT] and keys[pygame.K_UP]) or (keys[pygame.K_UP] and keys[pygame.K_RIGHT]):
            shape_type = "pentagon"
            if current_time - last_color_change >= color_change_interval:
                current_color = get_random_color()
                last_color_change = current_time
        
        elif (keys[pygame.K_LEFT] and keys[pygame.K_DOWN]) or (keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]):
            shape_type = "triangle"
            if current_time - last_color_change >= color_change_interval:
                current_color = get_random_color()
                last_color_change = current_time
        
        else:
            shape_type = "rectangle"

        # Check if object has moved
        current_position = (x, y)
        if current_position != last_position:
            last_movement_time = current_time
            black_hole_active = False
            black_hole_radius = 0
        last_position = current_position

        # Check for idle time
        if current_time - last_movement_time > idle_threshold:
            black_hole_active = True

    # Drawing
    window.fill(WHITE)
    
    if not game_over:
        # Draw the player shape
        if shape_type == "rectangle":
            pygame.draw.rect(window, current_color, (x, y, height, width))
        elif shape_type == "pentagon":
            draw_pentagon(window, current_color, x + width//2, y + height//2, max(height, width))
        elif shape_type == "triangle":
            draw_triangle(window, current_color, x + width//2, y + height//2, max(height, width))
    
    # Draw black hole if active
    if black_hole_active:
        black_hole_radius = min(black_hole_radius + black_hole_growth_speed, max_black_hole_radius)
        draw_black_hole(window, x + width//2, y + height//2, black_hole_radius)
        
        # Check if black hole has consumed the object
        if black_hole_radius >= max_black_hole_radius:
            game_over = True

    # Draw game over text
    if game_over:
        draw_game_over(window)
    
    pygame.display.update()

pygame.quit()
