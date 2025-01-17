import pygame
from pygame import mixer
import os
import random
import math

# Initialize Pygame
pygame.init()
mixer.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Window settings
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MP3 Player with Tornado Visualization")

# Font
font = pygame.font.Font(None, 36)

class GlowingButton:
    def __init__(self, x, y, width, height, text, base_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.is_hover = False
        self.glow_time = random.uniform(0, 2 * math.pi)
        self.glow_speed = random.uniform(0.05, 0.15)

    def draw(self, surface):
        self.glow_time += self.glow_speed
        glow = (math.sin(self.glow_time) + 1) / 2
        color = self.base_color

        if self.is_hover:
            glow_amount = int(60 * glow)
            color = tuple(min(255, c + glow_amount) for c in self.base_color)
            
            # Edge glow effect
            for i in range(5):
                glow_rect = self.rect.inflate(i * 6, i * 6)
                glow_color = tuple(max(0, min(255, c - 40 + glow_amount)) for c in self.base_color)
                pygame.draw.rect(surface, glow_color, glow_rect, border_radius=15)

        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hover = self.rect.collidepoint(event.pos)
        return event.type == pygame.MOUSEBUTTONDOWN and self.is_hover

class TornadoVisualizer:
    def __init__(self):
        self.tornados = []
        self.create_tornados(1)
        self.last_split_time = pygame.time.get_ticks()
        self.split_interval = 2000  # 2 seconds
        self.current_count = 1
        self.increasing = True

    def create_tornados(self, count):
        positions = []
        if count <= 3:
            # Single row
            for i in range(count):
                x = WINDOW_WIDTH * (i + 1) / (count + 1)
                positions.append((x, WINDOW_HEIGHT // 2))
        elif count <= 6:
            # Two rows
            row1 = min(3, count)
            row2 = count - row1
            for i in range(row1):
                x = WINDOW_WIDTH * (i + 1) / (row1 + 1)
                positions.append((x, WINDOW_HEIGHT // 3))
            for i in range(row2):
                x = WINDOW_WIDTH * (i + 1) / (row2 + 1)
                positions.append((x, 2 * WINDOW_HEIGHT // 3))
        else:
            # Three rows
            for i in range(3):
                x = WINDOW_WIDTH * (i + 1) / 4
                positions.append((x, WINDOW_HEIGHT // 4))
            for i in range(3):
                x = WINDOW_WIDTH * (i + 1) / 4
                positions.append((x, WINDOW_HEIGHT // 2))
            for i in range(count - 6):
                x = WINDOW_WIDTH * (i + 1) / 4
                positions.append((x, 3 * WINDOW_HEIGHT // 4))

        self.tornados = []
        size_multiplier = 1.5 / (count ** 0.5)  # Tornados get smaller as count increases
        
        for x, y in positions:
            tornado = {
                'x': x,
                'y': y,
                'particles': [],
                'color': random.choice(COLORS),
                'rotation_speed': random.uniform(0.02, 0.05),
                'size': size_multiplier
            }
            self.tornados.append(tornado)

    def create_particle(self, x, y, color, size):
        return {
            'x': x,
            'y': y,
            'angle': random.uniform(0, 2 * math.pi),
            'radius': random.uniform(10, 50) * size,
            'speed': random.uniform(2, 5),
            'color': color,
            'size': random.randint(2, 6) * size,
            'brightness': random.randint(100, 255)
        }

    def update(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_split_time > self.split_interval:
            self.last_split_time = current_time
            if self.increasing:
                self.current_count += 1
                if self.current_count >= 9:
                    self.increasing = False
            else:
                self.current_count = 1
                self.increasing = True
            self.create_tornados(self.current_count)

        for tornado in self.tornados:
            # Add new particles
            for _ in range(20):
                tornado['particles'].append(
                    self.create_particle(tornado['x'], tornado['y'], tornado['color'], tornado['size']))

            # Update particle positions and properties
            for particle in tornado['particles']:
                particle['angle'] += tornado['rotation_speed']
                particle['radius'] -= particle['speed'] * 0.1
                particle['brightness'] = max(0, particle['brightness'] - random.uniform(1, 3))
                particle['x'] = tornado['x'] + particle['radius'] * math.cos(particle['angle'])
                particle['y'] = tornado['y'] + particle['radius'] * math.sin(particle['angle'])

            # Remove faded particles
            tornado['particles'] = [p for p in tornado['particles'] if p['brightness'] > 0 and p['radius'] > 5]

    def draw(self, surface):
        for tornado in self.tornados:
            for particle in tornado['particles']:
                color = tuple(int(c * particle['brightness'] / 255) for c in particle['color'])
                pos = (int(particle['x']), int(particle['y']))
                pygame.draw.circle(surface, color, pos, int(particle['size']))

def load_music_files():
    return [f for f in os.listdir('.') if f.endswith('.mp3')]

def main():
    # Create buttons
    play_button = GlowingButton(50, 650, 100, 40, "Play", (0, 180, 0))
    pause_button = GlowingButton(170, 650, 100, 40, "Pause", (180, 180, 0))
    stop_button = GlowingButton(290, 650, 100, 40, "Stop", (180, 0, 0))
    loop_button = GlowingButton(410, 650, 100, 40, "Loop", (0, 0, 180))
    volume_up = GlowingButton(530, 650, 100, 40, "Vol +", (0, 180, 180))
    volume_down = GlowingButton(650, 650, 100, 40, "Vol -", (180, 0, 180))

    # Progress bar
    progress_rect = pygame.Rect(50, 600, 700, 15)
    
    # Initial states
    is_playing = False
    is_looping = False
    current_volume = 0.5
    mixer.music.set_volume(current_volume)

    # Load music files
    music_files = load_music_files()
    if not music_files:
        print("No MP3 files found in directory")
        return

    current_track = 0
    mixer.music.load(music_files[current_track])
    track_length = mixer.Sound(music_files[current_track]).get_length()

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
                    visualizer = TornadoVisualizer()

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
                visualizer = TornadoVisualizer()

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

        screen.fill(BLACK)

        # Update and draw visualization
        if is_playing:
            visualizer.update()
        visualizer.draw(screen)

        # Draw progress bar
        pygame.draw.rect(screen, (40, 40, 40), progress_rect)
        if is_playing:
            progress = mixer.music.get_pos() / 1000
            progress_width = min(progress / track_length * progress_rect.width, progress_rect.width)
            pygame.draw.rect(screen, (100, 200, 255), 
                           (progress_rect.x, progress_rect.y, progress_width, progress_rect.height))

        # Draw buttons
        play_button.draw(screen)
        pause_button.draw(screen)
        stop_button.draw(screen)
        loop_button.draw(screen)
        volume_up.draw(screen)
        volume_down.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
