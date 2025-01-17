import pygame
import pygame.mixer
import math
import random
import tkinter as tk
from tkinter import filedialog
from mutagen.mp3 import MP3
import os

# Inisialisasi Pygame
pygame.init()
pygame.mixer.init()

# Konstanta
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), 
          (255,0,255), (0,255,255), (128,0,0), (0,128,0)]

# Setup window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MP3 Player dengan Visualisasi Honeycomb")
clock = pygame.time.Clock()

class MP3Player:
    def __init__(self):
        self.playing = False
        self.paused = False
        self.current_file = None
        self.volume = 0.5
        self.loop = False
        
        # Button rectangles
        self.play_button = pygame.Rect(350, 500, 50, 30)
        self.stop_button = pygame.Rect(410, 500, 50, 30)
        self.loop_button = pygame.Rect(470, 500, 50, 30)
        self.vol_up = pygame.Rect(530, 500, 30, 30)
        self.vol_down = pygame.Rect(570, 500, 30, 30)
        
        # Progress bar
        self.progress_rect = pygame.Rect(150, 460, 500, 10)
        
    def load_file(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            filetypes=[("MP3 files", "*.mp3")]
        )
        if file_path:
            self.current_file = file_path
            pygame.mixer.music.load(file_path)
            self.audio = MP3(file_path)
            self.duration = self.audio.info.length
            
    def play(self):
        if not self.playing and self.current_file:
            pygame.mixer.music.play(-1 if self.loop else 0)
            self.playing = True
            self.paused = False
        elif self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            
    def pause(self):
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            
    def stop(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False
            self.paused = False
            
    def toggle_loop(self):
        self.loop = not self.loop
        if self.playing:
            current_pos = pygame.mixer.music.get_pos() / 1000
            pygame.mixer.music.stop()
            pygame.mixer.music.play(-1 if self.loop else 0)
            pygame.mixer.music.set_pos(current_pos)
            
    def change_volume(self, up=True):
        if up and self.volume < 1.0:
            self.volume = min(1.0, self.volume + 0.1)
        elif not up and self.volume > 0.0:
            self.volume = max(0.0, self.volume - 0.1)
        pygame.mixer.music.set_volume(self.volume)
        
    def draw_honeycomb(self, screen, music_data):
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50
        radius = 150
        sides = 8
        layers = 4
        
        for layer in range(layers):
            angle = 2 * math.pi / sides
            for i in range(sides):
                current_angle = i * angle
                # Menghitung posisi vertex hexagon
                points = []
                for j in range(sides):
                    vertex_angle = current_angle + (j * angle)
                    x = center_x + (radius + layer * 40) * math.cos(vertex_angle)
                    y = center_y + (radius + layer * 40) * math.sin(vertex_angle)
                    points.append((int(x), int(y)))
                
                # Warna berdasarkan musik
                color_index = (i + layer) % len(COLORS)
                intensity = min(255, abs(int(music_data[i % len(music_data)] * 255)))
                color = tuple(min(255, c * intensity // 255) for c in COLORS[color_index])
                
                # Gambar polygon
                pygame.draw.polygon(screen, color, points)
                pygame.draw.polygon(screen, WHITE, points, 2)
    
    def draw_controls(self, screen):
        # Draw buttons
        pygame.draw.rect(screen, WHITE, self.play_button)
        pygame.draw.rect(screen, WHITE, self.stop_button)
        pygame.draw.rect(screen, WHITE if not self.loop else (0,255,0), self.loop_button)
        pygame.draw.rect(screen, WHITE, self.vol_up)
        pygame.draw.rect(screen, WHITE, self.vol_down)
        
        # Draw progress bar background
        pygame.draw.rect(screen, WHITE, self.progress_rect, 2)
        
        # Draw progress
        if self.playing and not self.paused:
            current_time = pygame.mixer.music.get_pos() / 1000
            progress_width = (current_time / self.duration) * self.progress_rect.width
            progress = pygame.Rect(self.progress_rect.left, self.progress_rect.top,
                                 progress_width, self.progress_rect.height)
            pygame.draw.rect(screen, WHITE, progress)
            
    def handle_click(self, pos):
        if self.play_button.collidepoint(pos):
            if self.paused or not self.playing:
                self.play()
            else:
                self.pause()
        elif self.stop_button.collidepoint(pos):
            self.stop()
        elif self.loop_button.collidepoint(pos):
            self.toggle_loop()
        elif self.vol_up.collidepoint(pos):
            self.change_volume(True)
        elif self.vol_down.collidepoint(pos):
            self.change_volume(False)
        elif self.progress_rect.collidepoint(pos):
            # Set position in song based on click position
            click_pos = (pos[0] - self.progress_rect.left) / self.progress_rect.width
            pygame.mixer.music.set_pos(click_pos * self.duration)

def main():
    player = MP3Player()
    player.load_file()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    player.handle_click(event.pos)
        
        # Clear screen
        screen.fill(BLACK)
        
        # Get music data for visualization
        if player.playing and not player.paused:
            # Simulasi data musik (dalam implementasi nyata, gunakan data dari pygame.mixer.music)
            music_data = [random.random() for _ in range(8)]
        else:
            music_data = [0] * 8
            
        # Draw visualizations and controls
        player.draw_honeycomb(screen, music_data)
        player.draw_controls(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    main()
