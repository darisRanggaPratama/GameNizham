import pygame
import random
import math
import os
from pygame import mixer

# Inisialisasi pygame
pygame.init()
mixer.init()

# Konstanta warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]

# Setup window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MP3 Player dengan Heartbeat Visualizer")

# Font
font = pygame.font.Font(None, 36)

# Class untuk button
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False

    def draw(self, surface):
        color = (self.color[0]+30, self.color[1]+30, self.color[2]+30) if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
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

# Class untuk heartbeat visualizer
class HeartbeatVisualizer:
    def __init__(self):
        self.points = []
        self.colors = []
        self.phase = 0
        self.amplitude = 50
        
    def update(self):
        self.phase += 0.1
        if len(self.points) > 150:
            self.points.pop(0)
            self.colors.pop(0)
            
        new_y = math.sin(self.phase) * self.amplitude
        if len(self.points) > 0:
            last_y = self.points[-1][1]
            if abs(new_y - last_y) > 30:
                new_y = last_y + (30 if new_y > last_y else -30)
                
        self.points.append((len(self.points) * 5, WINDOW_HEIGHT//2 + new_y))
        self.colors.append(random.choice(COLORS))
        
    def draw(self, surface):
        if len(self.points) > 1:
            for i in range(len(self.points)-1):
                pygame.draw.line(surface, self.colors[i], 
                               self.points[i], self.points[i+1], 3)

# Buttons
play_button = Button(50, 500, 100, 40, "Play", (0, 128, 0))
pause_button = Button(170, 500, 100, 40, "Pause", (128, 128, 0))
stop_button = Button(290, 500, 100, 40, "Stop", (128, 0, 0))
loop_button = Button(410, 500, 100, 40, "Loop", (0, 0, 128))
volume_up = Button(530, 500, 100, 40, "Vol +", (0, 128, 128))
volume_down = Button(650, 500, 100, 40, "Vol -", (128, 0, 128))

# Progress bar
progress_rect = pygame.Rect(50, 450, 700, 10)

# Visualizer
visualizer = HeartbeatVisualizer()

# Music state
is_playing = False
is_looping = False
current_volume = 0.5
mixer.music.set_volume(current_volume)

# Main game loop
def main():
    global is_playing, is_looping, current_volume
    
    # Load music file (ganti dengan path file MP3 Anda)
    try:
        mixer.music.load("music3.mp3")
    except:
        print("Harap pastikan file 'music.mp3' ada di direktori yang sama")
        return

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle button events
            if play_button.handle_event(event):
                if not is_playing:
                    mixer.music.play(-1 if is_looping else 0)
                    is_playing = True
                    
            if pause_button.handle_event(event):
                if is_playing:
                    mixer.music.pause()
                    is_playing = False
                else:
                    mixer.music.unpause()
                    is_playing = True
                    
            if stop_button.handle_event(event):
                mixer.music.stop()
                is_playing = False
                
            if loop_button.handle_event(event):
                is_looping = not is_looping
                if is_playing:
                    mixer.music.play(-1 if is_looping else 0)
                    
            if volume_up.handle_event(event):
                current_volume = min(1.0, current_volume + 0.1)
                mixer.music.set_volume(current_volume)
                
            if volume_down.handle_event(event):
                current_volume = max(0.0, current_volume - 0.1)
                mixer.music.set_volume(current_volume)

        # Update screen
        screen.fill(BLACK)
        
        # Update and draw visualizer if music is playing
        if is_playing:
            visualizer.update()
        visualizer.draw(screen)
        
        # Draw progress bar
        pygame.draw.rect(screen, (64, 64, 64), progress_rect)
        if is_playing:
            progress = mixer.music.get_pos() / 1000  # Convert to seconds
            width = (progress % 60) / 60 * progress_rect.width
            pygame.draw.rect(screen, WHITE, 
                           (progress_rect.x, progress_rect.y, width, progress_rect.height))
        
        # Draw buttons
        play_button.draw(screen)
        pause_button.draw(screen)
        stop_button.draw(screen)
        loop_button.draw(screen)
        volume_up.draw(screen)
        volume_down.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
