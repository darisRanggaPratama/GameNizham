import pygame
import numpy as np
from pygame import mixer
import os
import math
from tkinter import filedialog
import tkinter as tk

class MP3Player:
    def __init__(self):
        # Initialize Pygame and mixer
        pygame.init()
        mixer.init()
        
        # Window settings
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("MP3 Player with Visualization")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        
        # Player state
        self.playing = False
        self.looping = False
        self.current_volume = 0.5
        self.current_pos = 0
        self.song_length = 0
        self.current_file = None
        
        # Button dimensions
        self.button_width = 60
        self.button_height = 30
        self.button_margin = 20
        
        # Initialize buttons
        self.init_buttons()
        
        # Visualization parameters
        self.viz_points = 50
        self.viz_radius = 150
        self.heart_points = self.generate_heart_points()
    
    def generate_heart_points(self):
        points = []
        for t in np.linspace(0, 2*np.pi, 30):
            x = 16 * math.sin(t)**3
            y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
            points.append((x, y))
        return points
    
    def init_buttons(self):
        # Button positions
        button_y = self.HEIGHT - 100
        self.buttons = {
            'play': pygame.Rect(200, button_y, self.button_width, self.button_height),
            'pause': pygame.Rect(280, button_y, self.button_width, self.button_height),
            'stop': pygame.Rect(360, button_y, self.button_width, self.button_height),
            'loop': pygame.Rect(440, button_y, self.button_width, self.button_height),
            'vol_up': pygame.Rect(520, button_y, self.button_width, self.button_height),
            'vol_down': pygame.Rect(600, button_y, self.button_width, self.button_height)
        }
        
        # Progress bar
        self.progress_bar = pygame.Rect(100, button_y - 50, self.WIDTH - 200, 10)
    
    def draw_buttons(self):
        # Draw all buttons
        for name, rect in self.buttons.items():
            color = self.RED if (name == 'loop' and self.looping) else self.WHITE
            pygame.draw.rect(self.screen, color, rect, 2)
            font = pygame.font.Font(None, 24)
            text = font.render(name.replace('_', ' ').title(), True, self.WHITE)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def draw_progress_bar(self):
        # Draw progress bar background
        pygame.draw.rect(self.screen, self.WHITE, self.progress_bar, 2)
        
        if self.song_length > 0:
            # Draw progress
            progress_width = (self.current_pos / self.song_length) * self.progress_bar.width
            progress_rect = pygame.Rect(
                self.progress_bar.left,
                self.progress_bar.top,
                progress_width,
                self.progress_bar.height
            )
            pygame.draw.rect(self.screen, self.RED, progress_rect)
    
    def draw_visualization(self):
        if not self.playing:
            return
            
        # Generate fake audio data for visualization
        t = pygame.time.get_ticks() / 1000.0
        audio_data = [math.sin(2 * math.pi * (t + i/10)) for i in range(self.viz_points)]
        
        # Draw heart outline
        center_x, center_y = self.WIDTH // 2, self.HEIGHT // 2
        scale = 10
        
        # Scale and transform heart points
        transformed_points = [(center_x + p[0]*scale, center_y + p[1]*scale) for p in self.heart_points]
        
        # Draw heart
        pygame.draw.lines(self.screen, self.RED, False, transformed_points, 2)
        
        # Draw visualization lines
        for i, value in enumerate(audio_data):
            angle = (2 * math.pi * i) / len(audio_data)
            length = self.viz_radius * (0.5 + 0.5 * value)
            end_x = center_x + length * math.cos(angle)
            end_y = center_y + length * math.sin(angle)
            pygame.draw.line(self.screen, self.RED, (center_x, center_y), (end_x, end_y), 1)
    
    def handle_click(self, pos):
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if name == 'play':
                    self.play()
                elif name == 'pause':
                    self.pause()
                elif name == 'stop':
                    self.stop()
                elif name == 'loop':
                    self.looping = not self.looping
                elif name == 'vol_up':
                    self.change_volume(0.1)
                elif name == 'vol_down':
                    self.change_volume(-0.1)
                return
                
        if self.progress_bar.collidepoint(pos):
            # Calculate position in song based on click position
            rel_x = pos[0] - self.progress_bar.left
            self.current_pos = (rel_x / self.progress_bar.width) * self.song_length
            mixer.music.set_pos(self.current_pos)
    
    def play(self):
        if not self.current_file:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
            if file_path:
                self.current_file = file_path
                mixer.music.load(self.current_file)
                self.song_length = mixer.Sound(self.current_file).get_length()
        
        if self.current_file:
            mixer.music.play(-1 if self.looping else 0)
            self.playing = True
    
    def pause(self):
        if self.playing:
            mixer.music.pause()
            self.playing = False
        else:
            mixer.music.unpause()
            self.playing = True
    
    def stop(self):
        mixer.music.stop()
        self.playing = False
        self.current_pos = 0
    
    def change_volume(self, delta):
        self.current_volume = max(0.0, min(1.0, self.current_volume + delta))
        mixer.music.set_volume(self.current_volume)
    
    def update(self):
        if self.playing:
            self.current_pos = mixer.music.get_pos() / 1000.0
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            # Update
            self.update()
            
            # Draw
            self.screen.fill(self.BLACK)
            self.draw_visualization()
            self.draw_buttons()
            self.draw_progress_bar()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    player = MP3Player()
    player.run()
