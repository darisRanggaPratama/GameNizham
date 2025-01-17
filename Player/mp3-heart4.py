import pygame
import sys
import random
from pygame.locals import *

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
FONT = pygame.font.Font(None, 30)
BACKGROUND_COLOR = (30, 30, 30)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE, (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MP3 Player with Heartbeat Visualization")

# Load music
pygame.mixer.init()
pygame.mixer.music.load("music3.mp3")  # Replace with your MP3 file

# Button positions
buttons = {
    "play": pygame.Rect(50, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT),
    "pause": pygame.Rect(160, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT),
    "stop": pygame.Rect(270, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT),
    "loop": pygame.Rect(380, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT),
    "volume_up": pygame.Rect(490, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT),
    "volume_down": pygame.Rect(600, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT),
}

# Variables
running = True
visualization_on = False
looping = False
volume = 0.5
pygame.mixer.music.set_volume(volume)

# Function to draw buttons
def draw_buttons():
    for name, rect in buttons.items():
        pygame.draw.rect(screen, WHITE, rect, border_radius=5)
        text = FONT.render(name.replace("_", " ").capitalize(), True, BACKGROUND_COLOR)
        screen.blit(text, (rect.x + 10, rect.y + 5))

# Function to draw heartbeat visualization
def draw_heartbeat():
    for _ in range(20):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 200)
        size = random.randint(10, 50)
        color = random.choice(COLORS)
        pygame.draw.circle(screen, color, (x, y), size)

# Main loop
while running:
    screen.fill(BACKGROUND_COLOR)

    # Draw buttons
    draw_buttons()

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if buttons["play"].collidepoint(event.pos):
                pygame.mixer.music.play()
                visualization_on = True
            elif buttons["pause"].collidepoint(event.pos):
                pygame.mixer.music.pause()
                visualization_on = False
            elif buttons["stop"].collidepoint(event.pos):
                pygame.mixer.music.stop()
                visualization_on = False
            elif buttons["loop"].collidepoint(event.pos):
                looping = not looping
                pygame.mixer.music.play(-1 if looping else 0)
            elif buttons["volume_up"].collidepoint(event.pos):
                volume = min(1.0, volume + 0.1)
                pygame.mixer.music.set_volume(volume)
            elif buttons["volume_down"].collidepoint(event.pos):
                volume = max(0.0, volume - 0.1)
                pygame.mixer.music.set_volume(volume)

    # Draw heartbeat visualization
    if visualization_on:
        draw_heartbeat()

    # Update the screen
    pygame.display.flip()

# Quit PyGame
pygame.quit()
sys.exit()
