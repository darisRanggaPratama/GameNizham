import pygame
import random
import math
import pygame.mixer
from pygame.locals import *
import tkinter as tk
from tkinter import filedialog
from mutagen.mp3 import MP3

# Inisialisasi PyGame
pygame.init()
pygame.mixer.init()

# Konstanta
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255)
]

# Setup window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MP3 Player with Fireworks")
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = random.uniform(2, 5)
        self.angle = random.uniform(0, 2 * math.pi)
        self.lifetime = 100
        self.size = 3
        
    def update(self):
        self.x += math.cos(self.angle) * self.velocity
        self.y += math.sin(self.angle) * self.velocity
        self.lifetime -= 1
        self.size = max(0, self.size * 0.95)
        
    def draw(self, surface):
        alpha = int((self.lifetime / 100) * 255)
        color = (*self.color, alpha)
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (self.size, self.size), self.size)
        surface.blit(surf, (self.x - self.size, self.y - self.size))

class Firework:
    def __init__(self, x, y):
        self.particles = []
        self.create_particles(x, y)
        
    def create_particles(self, x, y):
        color = random.choice(COLORS)
        for _ in range(50):
            self.particles.append(Particle(x, y, color))
            
    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
                
    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

class MusicPlayer:
    def __init__(self):
        self.current_file = None
        self.playing = False
        self.paused = False
        self.loop = False
        self.volume = 0.5
        self.fireworks = []
        self.progress = 0
        pygame.mixer.music.set_volume(self.volume)
        
    def load_file(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.current_file = file_path
            pygame.mixer.music.load(file_path)
            self.audio = MP3(file_path)
            self.duration = self.audio.info.length
            return True
        return False
    
    def play(self):
        if self.current_file:
            if self.paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
            self.playing = True
            self.paused = False
            
    def pause(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.paused = True
            self.playing = False
            
    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        
    def toggle_loop(self):
        self.loop = not self.loop
        
    def volume_up(self):
        self.volume = min(1.0, self.volume + 0.1)
        pygame.mixer.music.set_volume(self.volume)
        
    def volume_down(self):
        self.volume = max(0.0, self.volume - 0.1)
        pygame.mixer.music.set_volume(self.volume)
        
    def update(self):
        if self.playing:
            # Update progress
            self.progress = pygame.mixer.music.get_pos() / 1000
            
            # Create new fireworks randomly
            if random.random() < 0.05:
                x = random.randint(0, WINDOW_WIDTH)
                y = random.randint(WINDOW_HEIGHT//2, WINDOW_HEIGHT)
                self.fireworks.append(Firework(x, y))
                
            # Update existing fireworks
            for firework in self.fireworks[:]:
                firework.update()
                if not firework.particles:
                    self.fireworks.remove(firework)
                    
            # Check if song ended
            if not pygame.mixer.music.get_busy():
                if self.loop:
                    self.play()
                else:
                    self.stop()
                    
    def draw(self, surface):
        # Draw fireworks
        for firework in self.fireworks:
            firework.draw(surface)
            
        # Draw controls background
        controls_surface = pygame.Surface((WINDOW_WIDTH, 100))
        controls_surface.fill((50, 50, 50))
        surface.blit(controls_surface, (0, WINDOW_HEIGHT - 100))
        
        # Draw progress bar
        if self.current_file:
            progress_width = (self.progress / self.duration) * (WINDOW_WIDTH - 40)
            pygame.draw.rect(surface, WHITE, (20, WINDOW_HEIGHT - 90, WINDOW_WIDTH - 40, 10), 1)
            pygame.draw.rect(surface, WHITE, (20, WINDOW_HEIGHT - 90, progress_width, 10))
            
        # Draw buttons
        button_y = WINDOW_HEIGHT - 60
        buttons = [
            ("Play", 100), ("Pause", 200), ("Stop", 300),
            ("Loop", 400), ("Vol+", 500), ("Vol-", 600)
        ]
        
        for text, x in buttons:
            pygame.draw.rect(surface, WHITE, (x, button_y, 80, 30), 2)
            font = pygame.font.Font(None, 24)
            text_surface = font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(x + 40, button_y + 15))
            surface.blit(text_surface, text_rect)

def main():
    player = MusicPlayer()
    if not player.load_file():
        return
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if WINDOW_HEIGHT - 60 <= y <= WINDOW_HEIGHT - 30:
                    if 100 <= x <= 180:
                        player.play()
                    elif 200 <= x <= 280:
                        player.pause()
                    elif 300 <= x <= 380:
                        player.stop()
                    elif 400 <= x <= 480:
                        player.toggle_loop()
                    elif 500 <= x <= 580:
                        player.volume_up()
                    elif 600 <= x <= 680:
                        player.volume_down()
        
        screen.fill(BLACK)
        player.update()
        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    main()
