import pygame
import random
import pygame.mixer
from pygame.locals import *
import os
from mutagen.mp3 import MP3

# Inisialisasi pygame
pygame.init()
pygame.mixer.init()

# Konstanta
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MP3 Player dengan Visualisasi")
clock = pygame.time.Clock()

# Kelas untuk bola yang memantul
class BouncingBall:
    def __init__(self):
        self.radius = random.randint(5, 15)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.dx = random.choice([-4, -3, -2, 2, 3, 4])
        self.dy = random.choice([-4, -3, -2, 2, 3, 4])
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.alpha = 255
        self.fade_speed = random.randint(2, 5)

    def update(self):
        self.x += self.dx
        self.y += self.dy

        # Pantulan di tepi layar
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.dx *= -1
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.dy *= -1

        # Efek fade out
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            return True
        return False

    def draw(self, surface):
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, (*self.color, self.alpha), (int(self.x), int(self.y)), self.radius)
        surface.blit(temp_surface, (0, 0))

# Kelas untuk tombol
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

# Setup musik dan tombol
current_song = None
song_length = 0
song_pos = 0
is_playing = False
is_looping = False
volume = 0.5

# Buat tombol
play_button = Button(300, 500, 80, 40, "Play", WHITE)
pause_button = Button(400, 500, 80, 40, "Pause", WHITE)
stop_button = Button(500, 500, 80, 40, "Stop", WHITE)
loop_button = Button(200, 500, 80, 40, "Loop", GRAY)
vol_up_button = Button(600, 500, 40, 40, "+", WHITE)
vol_down_button = Button(650, 500, 40, 40, "-", WHITE)

# List untuk menyimpan bola-bola
balls = []

# Progress bar
progress_rect = pygame.Rect(50, 450, 700, 20)

def load_music(file_path):
    global current_song, song_length
    pygame.mixer.music.load(file_path)
    current_song = MP3(file_path)
    song_length = current_song.info.length

def play_music():
    global is_playing
    if not is_playing:
        pygame.mixer.music.play(-1 if is_looping else 0)
        is_playing = True

def pause_music():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
        is_playing = False
    else:
        pygame.mixer.music.unpause()
        is_playing = True

def stop_music():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False

def toggle_loop():
    global is_looping
    is_looping = not is_looping
    if is_playing:
        play_music()

def change_volume(delta):
    global volume
    volume = max(0.0, min(1.0, volume + delta))
    pygame.mixer.music.set_volume(volume)

# Load musik (ganti dengan path file MP3 Anda)
try:
    load_music("music.mp3")
except:
    print("Harap tentukan path file MP3 yang valid")

# Game loop
running = True
while running:
    clock.tick(FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if play_button.is_clicked(mouse_pos):
                play_music()
            elif pause_button.is_clicked(mouse_pos):
                pause_music()
            elif stop_button.is_clicked(mouse_pos):
                stop_music()
            elif loop_button.is_clicked(mouse_pos):
                toggle_loop()
            elif vol_up_button.is_clicked(mouse_pos):
                change_volume(0.1)
            elif vol_down_button.is_clicked(mouse_pos):
                change_volume(-0.1)
            elif progress_rect.collidepoint(mouse_pos):
                # Set posisi musik berdasarkan klik pada progress bar
                click_pos = (mouse_pos[0] - progress_rect.left) / progress_rect.width
                pygame.mixer.music.set_pos(song_length * click_pos)

    # Update
    # Tambah bola baru secara random
    if is_playing and random.random() < 0.1:
        balls.append(BouncingBall())

    # Update posisi bola dan hapus yang sudah fade out
    balls = [ball for ball in balls if not ball.update()]

    # Get posisi musik saat ini
    if is_playing:
        song_pos = pygame.mixer.music.get_pos() / 1000.0

    # Draw
    screen.fill(BLACK)
    
    # Draw bola-bola
    for ball in balls:
        ball.draw(screen)

    # Draw progress bar background
    pygame.draw.rect(screen, GRAY, progress_rect)
    
    # Draw progress
    if song_length > 0:
        progress_width = (song_pos / song_length) * progress_rect.width
        pygame.draw.rect(screen, WHITE, (progress_rect.left, progress_rect.top, progress_width, progress_rect.height))

    # Draw tombol-tombol
    play_button.draw(screen)
    pause_button.draw(screen)
    stop_button.draw(screen)
    loop_button.draw(screen)
    vol_up_button.draw(screen)
    vol_down_button.draw(screen)
    
    # Update display
    pygame.display.flip()

pygame.quit()
