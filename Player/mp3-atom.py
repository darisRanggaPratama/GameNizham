import pygame
import math
import random
from pygame import mixer
import os

# Inisialisasi PyGame
pygame.init()
mixer.init()

# Konstanta warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Pengaturan layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Atomic Music Player")

# Class untuk Atom
class Atom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.electrons = []
        self.num_electrons = random.randint(2, 5)
        self.angles = [0] * self.num_electrons
        self.radii = [random.randint(30, 60) for _ in range(self.num_electrons)]
        self.speeds = [random.uniform(0.02, 0.05) for _ in range(self.num_electrons)]
        
    def update(self):
        for i in range(self.num_electrons):
            self.angles[i] += self.speeds[i]
            
    def draw(self, surface):
        # Gambar inti atom
        pygame.draw.circle(surface, RED, (self.x, self.y), 15)
        
        # Gambar elektron dan orbitnya
        for i in range(self.num_electrons):
            # Gambar orbit
            pygame.draw.circle(surface, GRAY, (self.x, self.y), self.radii[i], 1)
            
            # Hitung posisi elektron
            electron_x = self.x + math.cos(self.angles[i]) * self.radii[i]
            electron_y = self.y + math.sin(self.angles[i]) * self.radii[i]
            
            # Gambar elektron
            pygame.draw.circle(surface, BLUE, (int(electron_x), int(electron_y)), 5)

# Class untuk Button
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Buat atom-atom
atoms = [
    Atom(200, 200),
    Atom(400, 300),
    Atom(600, 200)
]

# Buat buttons
play_button = Button(50, 500, 100, 40, "Play", WHITE)
pause_button = Button(160, 500, 100, 40, "Pause", WHITE)
stop_button = Button(270, 500, 100, 40, "Stop", WHITE)
loop_button = Button(380, 500, 100, 40, "Loop", WHITE)
vol_up_button = Button(490, 500, 100, 40, "Vol +", WHITE)
vol_down_button = Button(600, 500, 100, 40, "Vol -", WHITE)

# Progress bar
progress_rect = pygame.Rect(50, 450, 700, 20)

# Load musik (ganti dengan path file MP3 Anda)
try:
    mixer.music.load("music.mp3")
except:
    print("Please place a music.mp3 file in the same directory")

# Variabel kontrol
is_playing = False
is_looping = False
volume = 0.5
mixer.music.set_volume(volume)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle button clicks
            if play_button.is_clicked(mouse_pos):
                if not is_playing:
                    mixer.music.play()
                    is_playing = True
                    
            elif pause_button.is_clicked(mouse_pos):
                if is_playing:
                    mixer.music.pause()
                    is_playing = False
                else:
                    mixer.music.unpause()
                    is_playing = True
                    
            elif stop_button.is_clicked(mouse_pos):
                mixer.music.stop()
                is_playing = False
                
            elif loop_button.is_clicked(mouse_pos):
                is_looping = not is_looping
                mixer.music.set_loop(is_looping)
                
            elif vol_up_button.is_clicked(mouse_pos):
                volume = min(1.0, volume + 0.1)
                mixer.music.set_volume(volume)
                
            elif vol_down_button.is_clicked(mouse_pos):
                volume = max(0.0, volume - 0.1)
                mixer.music.set_volume(volume)
                
            # Handle progress bar click
            elif progress_rect.collidepoint(mouse_pos):
                click_pos = (mouse_pos[0] - progress_rect.x) / progress_rect.width
                mixer.music.set_pos(click_pos * mixer.Sound("music.mp3").get_length())
    
    # Update
    if is_playing:
        for atom in atoms:
            atom.update()
    
    # Draw
    screen.fill(BLACK)
    
    # Draw atoms
    for atom in atoms:
        atom.draw(screen)
    
    # Draw controls
    play_button.draw(screen)
    pause_button.draw(screen)
    stop_button.draw(screen)
    loop_button.draw(screen)
    vol_up_button.draw(screen)
    vol_down_button.draw(screen)
    
    # Draw progress bar
    pygame.draw.rect(screen, GRAY, progress_rect)
    if mixer.music.get_busy():
        try:
            current_time = mixer.music.get_pos() / 1000  # Convert to seconds
            total_time = mixer.Sound("music.mp3").get_length()
            progress_width = (current_time / total_time) * progress_rect.width
            pygame.draw.rect(screen, WHITE, (progress_rect.x, progress_rect.y, progress_width, progress_rect.height))
        except:
            pass
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
