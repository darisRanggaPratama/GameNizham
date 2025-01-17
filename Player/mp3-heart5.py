# File: mp3_player_visualizer.py

import pygame
import sys
import random
from pygame.locals import *

# Initialize PyGame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
FONT_SIZE = 20
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Heartbeat graphic settings
HEARTBEAT_COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MP3 Player with Heartbeat Visualizer")

# Load font
font = pygame.font.Font(None, FONT_SIZE)

# Music file
music_file = "music2.mp3"  # Replace with your MP3 file path
pygame.mixer.music.load(music_file)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=10)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
buttons = [
    Button(50, 500, BUTTON_WIDTH, BUTTON_HEIGHT, "Play", "play"),
    Button(200, 500, BUTTON_WIDTH, BUTTON_HEIGHT, "Pause", "pause"),
    Button(350, 500, BUTTON_WIDTH, BUTTON_HEIGHT, "Stop", "stop"),
    Button(500, 500, BUTTON_WIDTH, BUTTON_HEIGHT, "Loop", "loop"),
    Button(650, 500, BUTTON_WIDTH, BUTTON_HEIGHT, "Vol+", "vol_up"),
    Button(650, 560, BUTTON_WIDTH, BUTTON_HEIGHT, "Vol-", "vol_down"),
]

# Progress bar
def draw_progress_bar():
    if pygame.mixer.music.get_busy():
        pos = pygame.mixer.music.get_pos() / 1000
        length = pygame.mixer.Sound(music_file).get_length()
        progress = pos / length
        progress_width = SCREEN_WIDTH * progress
        pygame.draw.rect(screen, WHITE, (0, 450, SCREEN_WIDTH, 20))
        pygame.draw.rect(screen, GREEN, (0, 450, progress_width, 20))

# Heartbeat visualizer
def draw_heartbeat():
    for _ in range(20):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(50, 400)
        size = random.randint(5, 30)
        color = random.choice(HEARTBEAT_COLORS)
        pygame.draw.circle(screen, color, (x, y), size)

# Main loop
clock = pygame.time.Clock()
running = True
is_paused = False
loop_mode = False

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event.pos):
                    if button.action == "play":
                        pygame.mixer.music.play(loops=0 if not loop_mode else -1)
                        is_paused = False
                    elif button.action == "pause":
                        if not is_paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        is_paused = not is_paused
                    elif button.action == "stop":
                        pygame.mixer.music.stop()
                    elif button.action == "loop":
                        loop_mode = not loop_mode
                        pygame.mixer.music.play(loops=-1 if loop_mode else 0)
                    elif button.action == "vol_up":
                        volume = min(pygame.mixer.music.get_volume() + 0.1, 1.0)
                        pygame.mixer.music.set_volume(volume)
                    elif button.action == "vol_down":
                        volume = max(pygame.mixer.music.get_volume() - 0.1, 0.0)
                        pygame.mixer.music.set_volume(volume)

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Draw progress bar
    draw_progress_bar()

    # Draw heartbeat
    draw_heartbeat()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
