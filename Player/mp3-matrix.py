import pygame
import random
import string
import os
from pygame import mixer

# Inisialisasi pygame
pygame.init()
mixer.init()

# Konstanta
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Warna
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
WHITE = (255, 255, 255)

# Setup window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Matrix MP3 Player")
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 20)

class MatrixSymbol:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(5, 15)
        self.char = random.choice(string.ascii_letters + string.digits)
        self.brightness = 255

    def move(self):
        self.y += self.speed
        if self.y > WINDOW_HEIGHT:
            self.y = random.randint(-100, 0)
            self.x = random.randint(0, WINDOW_WIDTH)
        self.char = random.choice(string.ascii_letters + string.digits)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False

    def draw(self, surface):
        color = GREEN if self.is_hovered else DARK_GREEN
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# Buat simbol matrix
symbols = []
for i in range(100):
    x = random.randint(0, WINDOW_WIDTH)
    y = random.randint(0, WINDOW_HEIGHT)
    symbols.append(MatrixSymbol(x, y))

# Buat tombol
play_button = Button(250, 550, 60, 30, "Play")
pause_button = Button(320, 550, 60, 30, "Pause")
stop_button = Button(390, 550, 60, 30, "Stop")
loop_button = Button(460, 550, 60, 30, "Loop")

# Status music
is_playing = False
is_looping = False

def load_music(music_file="music.mp3"):
    if os.path.exists(music_file):
        mixer.music.load(music_file)
    else:
        print(f"Error: File {music_file} tidak ditemukan!")
        return False
    return True

def play_music():
    global is_playing
    if not is_playing:
        mixer.music.play(-1 if is_looping else 0)
        is_playing = True

def pause_music():
    global is_playing
    if is_playing:
        mixer.music.pause()
        is_playing = False
    else:
        mixer.music.unpause()
        is_playing = True

def stop_music():
    global is_playing
    mixer.music.stop()
    is_playing = False

def toggle_loop():
    global is_looping
    is_looping = not is_looping
    if is_playing:
        mixer.music.play(-1 if is_looping else 0)

# Main game loop
running = True
if load_music():  # Load music file
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if play_button.handle_event(event):
                play_music()
            elif pause_button.handle_event(event):
                pause_music()
            elif stop_button.handle_event(event):
                stop_music()
            elif loop_button.handle_event(event):
                toggle_loop()

        # Update
        screen.fill(BLACK)
        
        # Update and draw matrix symbols
        for symbol in symbols:
            if is_playing:  # Animasi hanya berjalan saat musik dimainkan
                symbol.move()
            text = font.render(symbol.char, True, (0, symbol.brightness, 0))
            screen.blit(text, (symbol.x, symbol.y))

        # Draw buttons
        play_button.draw(screen)
        pause_button.draw(screen)
        stop_button.draw(screen)
        loop_button.draw(screen)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
