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
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

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
        self.glow_timer = random.uniform(0, 2 * math.pi)
        self.glow_speed = random.uniform(0.05, 0.15)

    def draw(self, surface):
        self.glow_timer += self.glow_speed
        glow = (math.sin(self.glow_timer) + 1) / 2
        color = self.base_color
        if self.is_hovered:
            glow_amount = int(60 * glow)
            color = tuple(min(255, c + glow_amount) for c in self.base_color)
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
            self.is_hovered = self.rect.collidepoint(event.pos)
        return event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered

class TornadoVisualizer:
    def __init__(self):
        self.tornados = []
        self.create_tornado(1)

    def create_tornado(self, count):
        self.tornados = []
        for _ in range(count):
            tornado = {
                'x': WINDOW_WIDTH // 2,
                'y': WINDOW_HEIGHT // 2,
                'particles': [],
                'color': random.choice(COLORS),
                'rotation_speed': random.uniform(0.02, 0.05),
                'size_multiplier': 1.0
            }
            self.tornados.append(tornado)

    def create_particle(self, x, y, color, size_multiplier):
        return {
            'x': x,
            'y': y,
            'angle': random.uniform(0, 2 * math.pi),
            'radius': random.uniform(10, 50) * size_multiplier,
            'speed': random.uniform(2, 5),
            'color': color,
            'size': random.randint(2, 6) * size_multiplier,
            'brightness': random.randint(100, 255)
        }

    def update(self):
        if len(self.tornados) < 9:
            self.tornados.append(self.tornados[-1].copy())

        for tornado in self.tornados:
            for _ in range(20):
                tornado['particles'].append(
                    self.create_particle(tornado['x'], tornado['y'], tornado['color'], tornado['size_multiplier']))

            for particle in tornado['particles']:
                particle['angle'] += tornado['rotation_speed']
                particle['radius'] -= particle['speed'] * 0.1
                particle['brightness'] = max(0, particle['brightness'] - random.uniform(1, 3))
                particle['x'] = tornado['x'] + particle['radius'] * math.cos(particle['angle'])
                particle['y'] = tornado['y'] + particle['radius'] * math.sin(particle['angle'])

            tornado['particles'] = [p for p in tornado['particles'] if p['brightness'] > 0 and p['radius'] > 5]

    def draw(self, surface):
        for tornado in self.tornados:
            for particle in tornado['particles']:
                color = tuple(int(c * particle['brightness'] / 255) for c in tornado['color'])
                pos = (int(particle['x']), int(particle['y']))
                pygame.draw.circle(surface, color, pos, int(particle['size']))

def load_music_files():
    return [file for file in os.listdir('.') if file.endswith('.mp3')]

def main():
    play_button = GlowingButton(50, 500, 100, 40, "Play", (0, 180, 0))
    pause_button = GlowingButton(170, 500, 100, 40, "Pause", (180, 180, 0))
    stop_button = GlowingButton(290, 500, 100, 40, "Stop", (180, 0, 0))
    loop_button = GlowingButton(410, 500, 100, 40, "Loop", (0, 0, 180))
    volume_up = GlowingButton(530, 500, 100, 40, "Vol +", (0, 180, 180))
    volume_down = GlowingButton(650, 500, 100, 40, "Vol -", (180, 0, 180))

    progress_rect = pygame.Rect(50, 450, 700, 15)
    is_playing = False
    is_looping = False
    current_volume = 0.5
    mixer.music.set_volume(current_volume)

    music_files = load_music_files()
    if not music_files:
        print("No MP3 files found in the current directory")
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
                visualizer = TornadoVisualizer()

            if loop_button.handle_event(event):
                is_looping = not is_looping

            if volume_up.handle_event(event):
                current_volume = min(1.0, current_volume + 0.1)
                mixer.music.set_volume(current_volume)

            if volume_down.handle_event(event):
                current_volume = max(0.0, current_volume - 0.1)
                mixer.music.set_volume(current_volume)

        screen.fill(BLACK)

        if is_playing:
            visualizer.update()
        visualizer.draw(screen)

        pygame.draw.rect(screen, (40, 40, 40), progress_rect)
        if is_playing:
            progress = mixer.music.get_pos() / 1000
            progress_width = min(progress / track_length * progress_rect.width, progress_rect.width)
            pygame.draw.rect(screen, (100, 200, 255), (progress_rect.x, progress_rect.y, progress_width, progress_rect.height))

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
