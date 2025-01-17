import pygame
import pygame.mixer
import os
from math import sin, cos, radians
import tkinter as tk
from tkinter import filedialog

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

class MP3Player:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python MP3 Player with Sun Visualization")
        self.clock = pygame.time.Clock()
        
        # Music state
        self.current_song = None
        self.is_playing = False
        self.is_looping = False
        self.volume = 0.5
        
        # Sun animation
        self.sun_rays = 12
        self.ray_length = 50
        self.animation_angle = 0
        self.ray_extension = 0
        
        # Buttons
        self.buttons = {
            'play': pygame.Rect(350, 500, 40, 40),
            'stop': pygame.Rect(400, 500, 40, 40),
            'loop': pygame.Rect(450, 500, 40, 40),
            'volume_up': pygame.Rect(500, 500, 40, 40),
            'volume_down': pygame.Rect(300, 500, 40, 40)
        }
        
        # Progress bar
        self.progress_bar = pygame.Rect(200, 450, 400, 10)
        
    def draw_sun(self):
        # Draw main sun body
        pygame.draw.circle(self.screen, YELLOW, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 50)
        
        # Draw animated rays
        for i in range(self.sun_rays):
            angle = radians(i * (360 / self.sun_rays) + self.animation_angle)
            ray_length = self.ray_length + sin(self.ray_extension) * 20
            
            start_pos = (
                WINDOW_WIDTH // 2 + cos(angle) * 50,
                WINDOW_HEIGHT // 2 + sin(angle) * 50
            )
            end_pos = (
                WINDOW_WIDTH // 2 + cos(angle) * (50 + ray_length),
                WINDOW_HEIGHT // 2 + sin(angle) * (50 + ray_length)
            )
            
            # Create gradient effect for rays
            for j in range(10):
                progress = j / 10
                current_length = ray_length * progress
                current_pos = (
                    WINDOW_WIDTH // 2 + cos(angle) * (50 + current_length),
                    WINDOW_HEIGHT // 2 + sin(angle) * (50 + current_length)
                )
                color = (255, 255 - (j * 20), 0)
                pygame.draw.line(self.screen, color, start_pos, current_pos, 3)
    
    def draw_controls(self):
        # Draw buttons
        for button_name, button_rect in self.buttons.items():
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Draw button symbols
            if button_name == 'play':
                if self.is_playing:
                    # Pause symbol
                    pygame.draw.rect(self.screen, WHITE, (button_rect.x + 12, button_rect.y + 10, 6, 20))
                    pygame.draw.rect(self.screen, WHITE, (button_rect.x + 22, button_rect.y + 10, 6, 20))
                else:
                    # Play symbol
                    points = [(button_rect.x + 15, button_rect.y + 10),
                             (button_rect.x + 15, button_rect.y + 30),
                             (button_rect.x + 30, button_rect.y + 20)]
                    pygame.draw.polygon(self.screen, WHITE, points)
            
            elif button_name == 'stop':
                pygame.draw.rect(self.screen, WHITE, (button_rect.x + 12, button_rect.y + 12, 16, 16))
            
            elif button_name == 'loop':
                if self.is_looping:
                    color = YELLOW
                else:
                    color = WHITE
                pygame.draw.circle(self.screen, color, (button_rect.centerx, button_rect.centery), 10, 2)
        
        # Draw progress bar
        pygame.draw.rect(self.screen, WHITE, self.progress_bar, 2)
        if self.current_song:
            progress = pygame.mixer.music.get_pos() / 1000  # Convert to seconds
            width = (progress / self.song_length) * self.progress_bar.width
            pygame.draw.rect(self.screen, WHITE, 
                           (self.progress_bar.x, self.progress_bar.y, width, self.progress_bar.height))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Handle button clicks
                for button_name, button_rect in self.buttons.items():
                    if button_rect.collidepoint(mouse_pos):
                        if button_name == 'play':
                            self.toggle_play()
                        elif button_name == 'stop':
                            self.stop()
                        elif button_name == 'loop':
                            self.toggle_loop()
                        elif button_name == 'volume_up':
                            self.change_volume(0.1)
                        elif button_name == 'volume_down':
                            self.change_volume(-0.1)
                
                # Handle progress bar click
                if self.progress_bar.collidepoint(mouse_pos) and self.current_song:
                    click_pos = (mouse_pos[0] - self.progress_bar.x) / self.progress_bar.width
                    pygame.mixer.music.set_pos(click_pos * self.song_length)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.toggle_play()
                elif event.key == pygame.K_l:
                    self.toggle_loop()
                elif event.key == pygame.K_o:
                    self.open_file()
        
        return True
    
    def open_file(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            pygame.mixer.music.load(file_path)
            self.current_song = file_path
            self.song_length = pygame.mixer.Sound(file_path).get_length()
            self.play()
    
    def play(self):
        if self.current_song:
            pygame.mixer.music.play(-1 if self.is_looping else 0)
            self.is_playing = True
    
    def toggle_play(self):
        if not self.current_song:
            self.open_file()
        elif self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
    
    def stop(self):
        if self.current_song:
            pygame.mixer.music.stop()
            self.is_playing = False
    
    def toggle_loop(self):
        self.is_looping = not self.is_looping
        if self.current_song and self.is_playing:
            self.stop()
            self.play()
    
    def change_volume(self, delta):
        self.volume = max(0.0, min(1.0, self.volume + delta))
        pygame.mixer.music.set_volume(self.volume)
    
    def update(self):
        self.animation_angle += 1
        self.ray_extension += 0.1
        
        if self.is_playing:
            # Make sun pulse with the music
            # Note: This is a simple visualization, you could add frequency analysis for more complex effects
            self.ray_length = 50 + sin(self.ray_extension) * 20
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            # Update
            self.update()
            
            # Draw
            self.screen.fill(BLACK)
            self.draw_sun()
            self.draw_controls()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    player = MP3Player()
    player.run()
