import pygame
import pygame.gfxdraw
import math
import random
from pygame import mixer
import os

class HexagonMusicPlayer:
    def __init__(self):
        pygame.init()
        mixer.init()
        
        # Window setup
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hexagon Music Player")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        
        # Button dimensions
        self.button_width = 60
        self.button_height = 30
        
        # Music control variables
        self.playing = False
        self.looping = False
        self.volume = 0.5
        self.current_time = 0
        self.total_time = 0
        
        # Hexagon parameters
        self.hexagons = []
        self.setup_hexagons()
        
        # Load default song (replace with your MP3 file)
        self.current_song = "music.mp3"  # Make sure this file exists
        mixer.music.load(self.current_song)
        mixer.music.set_volume(self.volume)
        
        # Font
        self.font = pygame.font.Font(None, 24)
        
    def setup_hexagons(self):
        # Create a grid of hexagons
        hex_radius = 30
        horizontal_spacing = hex_radius * 3
        vertical_spacing = hex_radius * 1.7
        
        for row in range(6):
            for col in range(8):
                x = col * horizontal_spacing + (row % 2) * (horizontal_spacing / 2) + 100
                y = row * vertical_spacing + 100
                color = self.random_color()
                self.hexagons.append({"x": x, "y": y, "radius": hex_radius, "color": color, "alpha": 255})
    
    def random_color(self):
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    
    def draw_hexagon(self, x, y, radius, color, alpha):
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.append((int(px), int(py)))
        
        # Create surface for alpha
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.polygon(surface, (*color, alpha), points)
        self.screen.blit(surface, (0, 0))
    
    def draw_button(self, x, y, width, height, text, active=False):
        color = self.GRAY if active else self.WHITE
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
        self.screen.blit(text_surface, text_rect)
        return pygame.Rect(x, y, width, height)
    
    def draw_progress_bar(self):
        # Draw progress bar background
        pygame.draw.rect(self.screen, self.GRAY, (50, 500, 700, 10))
        if self.total_time > 0:
            progress = self.current_time / self.total_time
            pygame.draw.rect(self.screen, self.WHITE, (50, 500, 700 * progress, 10))
    
    def update_visualization(self):
        # Update hexagon colors and alpha based on music
        for hex in self.hexagons:
            if random.random() < 0.1:  # 10% chance to change color
                hex["color"] = self.random_color()
                hex["alpha"] = random.randint(100, 255)
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        # Button positions
        play_button = pygame.Rect(300, 550, self.button_width, self.button_height)
        stop_button = pygame.Rect(370, 550, self.button_width, self.button_height)
        loop_button = pygame.Rect(440, 550, self.button_width, self.button_height)
        vol_up_button = pygame.Rect(510, 550, self.button_width, self.button_height)
        vol_down_button = pygame.Rect(580, 550, self.button_width, self.button_height)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    # Play/Pause button
                    if play_button.collidepoint(mouse_pos):
                        if not self.playing:
                            mixer.music.play()
                            self.playing = True
                        else:
                            mixer.music.pause()
                            self.playing = False
                    
                    # Stop button
                    elif stop_button.collidepoint(mouse_pos):
                        mixer.music.stop()
                        self.playing = False
                        self.current_time = 0
                    
                    # Loop button
                    elif loop_button.collidepoint(mouse_pos):
                        self.looping = not self.looping
                        mixer.music.set_endevent(pygame.USEREVENT if self.looping else 0)
                    
                    # Volume controls
                    elif vol_up_button.collidepoint(mouse_pos):
                        self.volume = min(1.0, self.volume + 0.1)
                        mixer.music.set_volume(self.volume)
                    
                    elif vol_down_button.collidepoint(mouse_pos):
                        self.volume = max(0.0, self.volume - 0.1)
                        mixer.music.set_volume(self.volume)
                    
                    # Progress bar click
                    elif 50 <= mouse_pos[0] <= 750 and 495 <= mouse_pos[1] <= 505:
                        click_position = (mouse_pos[0] - 50) / 700
                        self.current_time = self.total_time * click_position
                        mixer.music.play(start=self.current_time)
                        self.playing = True
            
            # Update current time
            if self.playing:
                self.current_time = mixer.music.get_pos() / 1000.0
            
            # Clear screen
            self.screen.fill(self.BLACK)
            
            # Update and draw visualization
            self.update_visualization()
            for hex in self.hexagons:
                self.draw_hexagon(hex["x"], hex["y"], hex["radius"], hex["color"], hex["alpha"])
            
            # Draw controls
            self.draw_button(300, 550, self.button_width, self.button_height, "Play" if not self.playing else "Pause", self.playing)
            self.draw_button(370, 550, self.button_width, self.button_height, "Stop")
            self.draw_button(440, 550, self.button_width, self.button_height, "Loop", self.looping)
            self.draw_button(510, 550, self.button_width, self.button_height, "Vol+")
            self.draw_button(580, 550, self.button_width, self.button_height, "Vol-")
            
            # Draw progress bar
            self.draw_progress_bar()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    player = HexagonMusicPlayer()
    player.run()
