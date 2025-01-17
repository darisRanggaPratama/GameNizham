import pygame
import random
import numpy as np
from pygame import mixer
import os
from pygame.locals import *

# Inisialisasi pygame
pygame.init()
mixer.init()

# Konstanta
WIDTH = 800
HEIGHT = 600
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MP3 Player dengan Visualisasi")
clock = pygame.time.Clock()

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

class Particle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(2, 8)
        self.color = (random.randint(50, 255), 
                     random.randint(50, 255), 
                     random.randint(50, 255))
        self.speed = random.randint(1, 5)
        
    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
            
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)

class MusicPlayer:
    def __init__(self):
        self.is_playing = False
        self.current_song = None
        self.particles = [Particle() for _ in range(100)]
        
        # Membuat tombol
        self.play_button = Button(250, 500, 100, 50, "Play", GREEN)
        self.pause_button = Button(360, 500, 100, 50, "Pause", BLUE)
        self.stop_button = Button(470, 500, 100, 50, "Stop", RED)
        
    def load_music(self, music_file):
        if os.path.exists(music_file):
            mixer.music.load(music_file)
            self.current_song = music_file
            
    def play(self):
        if not self.is_playing and self.current_song:
            mixer.music.play()
            self.is_playing = True
            
    def pause(self):
        if self.is_playing:
            mixer.music.pause()
            self.is_playing = False
        else:
            mixer.music.unpause()
            self.is_playing = True
            
    def stop(self):
        mixer.music.stop()
        self.is_playing = False
        
    def update_visualization(self):
        for particle in self.particles:
            particle.move()
            
    def draw(self, surface):
        # Menggambar background hitam
        surface.fill(BLACK)
        
        # Menggambar partikel
        if self.is_playing:
            for particle in self.particles:
                particle.draw(surface)
                
        # Menggambar tombol
        self.play_button.draw(surface)
        self.pause_button.draw(surface)
        self.stop_button.draw(surface)

def main():
    player = MusicPlayer()
    # Ganti dengan path file MP3 Anda
    player.load_music("music.mp3")
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if player.play_button.is_clicked(mouse_pos):
                    player.play()
                elif player.pause_button.is_clicked(mouse_pos):
                    player.pause()
                elif player.stop_button.is_clicked(mouse_pos):
                    player.stop()
        
        player.update_visualization()
        player.draw(screen)
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()
