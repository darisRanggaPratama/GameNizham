import pygame
import sys
import random
from pygame.locals import *

# Initialize PyGame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
HEARTBEAT_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MP3 Player with Heartbeat Visualization")

# Set up fonts
font = pygame.font.Font(None, 36)

# Load music
pygame.mixer.init()
pygame.mixer.music.load("music1.mp3")  # Replace with the path to your MP3 file

# Variables for music control
playing = False
loop = False
volume = 0.5
pygame.mixer.music.set_volume(volume)

# Progress bar
progress_bar_width = 400
progress_bar_height = 10
progress_bar_x = (WIDTH - progress_bar_width) // 2
progress_bar_y = HEIGHT - 100

# Heartbeat graphics
hearts = []
for _ in range(10):
    hearts.append({
        'x': random.randint(50, WIDTH - 50),
        'y': random.randint(50, HEIGHT - 200),
        'size': random.randint(20, 50),
        'color': random.choice(HEARTBEAT_COLORS),
        'blink': random.randint(1, 5)
    })

# Button dimensions
button_width, button_height = 100, 50
button_gap = 20

# Button positions
buttons = {
    "play": (50, HEIGHT - 70),
    "pause": (160, HEIGHT - 70),
    "stop": (270, HEIGHT - 70),
    "loop": (380, HEIGHT - 70),
    "vol_up": (500, HEIGHT - 70),
    "vol_down": (610, HEIGHT - 70)
}

# Main loop
clock = pygame.time.Clock()
while True:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if buttons["play"][0] <= x <= buttons["play"][0] + button_width and buttons["play"][1] <= y <= buttons["play"][1] + button_height:
                pygame.mixer.music.play(-1 if loop else 0)
                playing = True

            if buttons["pause"][0] <= x <= buttons["pause"][0] + button_width and buttons["pause"][1] <= y <= buttons["pause"][1] + button_height:
                pygame.mixer.music.pause()
                playing = False

            if buttons["stop"][0] <= x <= buttons["stop"][0] + button_width and buttons["stop"][1] <= y <= buttons["stop"][1] + button_height:
                pygame.mixer.music.stop()
                playing = False

            if buttons["loop"][0] <= x <= buttons["loop"][0] + button_width and buttons["loop"][1] <= y <= buttons["loop"][1] + button_height:
                loop = not loop

            if buttons["vol_up"][0] <= x <= buttons["vol_up"][0] + button_width and buttons["vol_up"][1] <= y <= buttons["vol_up"][1] + button_height:
                volume = min(volume + 0.1, 1.0)
                pygame.mixer.music.set_volume(volume)

            if buttons["vol_down"][0] <= x <= buttons["vol_down"][0] + button_width and buttons["vol_down"][1] <= y <= buttons["vol_down"][1] + button_height:
                volume = max(volume - 0.1, 0.0)
                pygame.mixer.music.set_volume(volume)

    # Draw buttons
    for name, (x, y) in buttons.items():
        pygame.draw.rect(screen, WHITE, (x, y, button_width, button_height))
        text = font.render(name.capitalize(), True, BLACK)
        screen.blit(text, (x + (button_width - text.get_width()) // 2, y + (button_height - text.get_height()) // 2))

    # Update and draw progress bar
    if playing:
        progress = pygame.mixer.music.get_pos() / 1000.0
        pygame.draw.rect(screen, WHITE, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
        progress_fill = (progress / pygame.mixer.Sound.get_length()) * progress_bar_width
        pygame.draw.rect(screen, WHITE, (progress_bar_x, progress_bar_y, progress_fill, progress_bar_height))

    # Draw heartbeat graphics
    for heart in hearts:
        pygame.draw.circle(screen, heart['color'], (heart['x'], heart['y']), heart['size'] // heart['blink'])
        heart['blink'] = heart['blink'] - 1 if heart['blink'] > 1 else random.randint(1, 5)

    pygame.display.flip()
    clock.tick(FPS)
