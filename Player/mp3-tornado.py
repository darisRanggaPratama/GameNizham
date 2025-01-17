import pygame
import os
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]

# Window setup
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MP3 Player with Tornado Visualizer")

# Font
font = pygame.font.Font(None, 36)

class GlowingButton:
    def __init__(self, x, y, width, height, text, base_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.is_hovered = False
        self.glow_timer = 0
        self.glow_speed = random.uniform(0.05, 0.1)
        
    def draw(self, surface):
        # Calculate glow effect
        self.glow_timer += self.glow_speed
        glow = (math.sin(self.glow_timer) + 1) / 2  # Value between 0 and 1
        
        # Create glowing color
        color = self.base_color
        if self.is_hovered:
            glow_amount = int(40 * glow)
            color = tuple(min(255, c + glow_amount) for c in self.base_color)
            
            # Draw glow effect
            for i in range(3):
                glow_rect = self.rect.inflate(i*4, i*4)
                glow_color = tuple(max(0, min(255, c - 40 + glow_amount)) for c in self.base_color)
                pygame.draw.rect(surface, glow_color, glow_rect, border_radius=12)
        
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        return event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered

class TornadoVisualizer:
    def __init__(self):
        self.tornados = []
        self.create_tornados()
        
    def create_tornados(self):
        # Create multiple tornados
        for i in range(3):
            tornado = {
                'x': WINDOW_WIDTH * (i + 1) // 4,
                'y': WINDOW_HEIGHT // 2,
                'particles': [],
                'color': random.choice(COLORS),
                'rotation_speed': random.uniform(0.02, 0.05)
            }
            self.tornados.append(tornado)
            
    def create_particle(self, x, y, color):
        return {
            'x': x,
            'y': y,
            'angle': random.uniform(0, 2 * math.pi),
            'radius': random.uniform(10, 50),
            'speed': random.uniform(2, 5),
            'color': color,
            'size': random.randint(2, 6),
            'brightness': random.randint(100, 255)
        }
    
    def update(self):
        for tornado in self.tornados:
            # Add new particles
            if len(tornado['particles']) < 50:
                tornado['particles'].append(
                    self.create_particle(tornado['x'], tornado['y'], tornado['color']))
            
            # Update particles
            for particle in tornado['particles']:
                # Spiral movement
                particle['angle'] += tornado['rotation_speed']
                particle['radius'] -= particle['speed'] * 0.1
                particle['brightness'] = max(0, particle['brightness'] - random.uniform(1, 3))
                
                # Calculate new position
                particle['x'] = tornado['x'] + particle['radius'] * math.cos(particle['angle'])
                particle['y'] = tornado['y'] + particle['radius'] * math.sin(particle['angle'])
            
            # Remove faded particles
            tornado['particles'] = [p for p in tornado['particles'] 
                                  if p['brightness'] > 0 and p['radius'] > 5]
            
            # Randomly change tornado color
            if random.random() < 0.01:
                tornado['color'] = random.choice(COLORS)
    
    def draw(self, surface):
        for tornado in self.tornados:
            for particle in tornado['particles']:
                color = tuple(int(c * particle['brightness'] / 255) 
                            for c in particle['color'])
                pos = (int(particle['x']), int(particle['y']))
                pygame.draw.circle(surface, color, pos, particle['size'])

def load_music_files():
    music_files = []
    for file in os.listdir('.'):
        if file.endswith('.mp3'):
            music_files.append(file)
    return music_files

def main():
    # Create buttons with different base colors
    play_button = GlowingButton(50, 500, 100, 40, "Play", (0, 128, 0))
    pause_button = GlowingButton(170, 500, 100, 40, "Pause", (128, 128, 0))
    stop_button = GlowingButton(290, 500, 100, 40, "Stop", (128, 0, 0))
    loop_button = GlowingButton(410, 500, 100, 40, "Loop", (0, 0, 128))
    volume_up = GlowingButton(530, 500, 100, 40, "Vol +", (0, 128, 128))
    volume_down = GlowingButton(650, 500, 100, 40, "Vol -", (128, 0, 128))

    # Progress bar
    progress_rect = pygame.Rect(50, 450, 700, 10)

    # Initialize states
    is_playing = False
    is_looping = False
    current_volume = 0.5
    mixer.music.set_volume(current_volume)
    
    # Load music files
    music_files = load_music_files()
    if not music_files:
        print("No MP3 files found in the current directory")
        return
    
    current_track = 0
    mixer.music.load(music_files[current_track])

    # Initialize visualizer
    visualizer = TornadoVisualizer()

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
        
        # Update and draw visualizer
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
