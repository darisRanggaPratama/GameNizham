import pygame
import os
import random
import math
from pygame import mixer

# Inisialisasi PyGame
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
pygame.display.set_caption("MP3 Player with Tornado Visualization")

# Font
font = pygame.font.Font(None, 36)

class GlowButton:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = color
        self.is_hovered = False
        self.glow_timer = random.uniform(0, 2 * math.pi)
        
    def draw(self, surface):
        # Efek berkedip
        self.glow_timer += 0.1
        glow = (math.sin(self.glow_timer) + 1) / 2
        
        # Warna button
        color = self.base_color
        if self.is_hovered:
            glow_amount = int(50 * glow)
            color = tuple(min(255, c + glow_amount) for c in self.base_color)
            
            # Efek sinar di pinggir
            for i in range(3):
                glow_rect = self.rect.inflate(i*8, i*8)
                glow_color = tuple(max(0, min(255, c - 30 + glow_amount)) for c in self.base_color)
                pygame.draw.rect(surface, glow_color, glow_rect, border_radius=10)
        
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
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
        self.num_tornados = 1
        self.tornado_timer = 0
        self.create_tornados()
        
    def create_tornados(self):
        self.tornados = []
        spacing = WINDOW_WIDTH / (self.num_tornados + 1)
        size = max(3.0 - (self.num_tornados * 0.3), 0.5)  # Ukuran mengecil seiring bertambahnya tornado
        
        for i in range(self.num_tornados):
            tornado = {
                'x': spacing * (i + 1),
                'y': WINDOW_HEIGHT // 2,
                'particles': [],
                'color': random.choice(COLORS),
                'rotation_speed': random.uniform(0.02, 0.05),
                'size': size
            }
            self.tornados.append(tornado)
    
    def update(self):
        self.tornado_timer += 1
        if self.tornado_timer >= 120:  # Ganti jumlah tornado setiap 2 detik
            self.tornado_timer = 0
            self.num_tornados = (self.num_tornados % 9) + 1
            self.create_tornados()
        
        for tornado in self.tornados:
            # Tambah partikel baru
            if len(tornado['particles']) < 80:
                particle = {
                    'x': tornado['x'],
                    'y': tornado['y'],
                    'angle': random.uniform(0, 2 * math.pi),
                    'radius': random.uniform(10, 50) * tornado['size'],
                    'speed': random.uniform(2, 4),
                    'color': tornado['color'],
                    'size': random.randint(2, 5),
                    'brightness': random.randint(100, 255)
                }
                tornado['particles'].append(particle)
            
            # Update partikel
            for particle in tornado['particles']:
                particle['angle'] += tornado['rotation_speed']
                particle['radius'] -= particle['speed'] * 0.1
                particle['brightness'] = max(0, particle['brightness'] - random.uniform(1, 3))
                
                particle['x'] = tornado['x'] + particle['radius'] * math.cos(particle['angle'])
                particle['y'] = tornado['y'] + particle['radius'] * math.sin(particle['angle'])
            
            # Hapus partikel yang sudah menghilang
            tornado['particles'] = [p for p in tornado['particles'] 
                                  if p['brightness'] > 0 and p['radius'] > 5]
            
            # Ganti warna secara random
            if random.random() < 0.02:
                tornado['color'] = random.choice(COLORS)
    
    def draw(self, surface):
        for tornado in self.tornados:
            for particle in tornado['particles']:
                color = tuple(int(c * particle['brightness'] / 255) 
                            for c in tornado['color'])
                pos = (int(particle['x']), int(particle['y']))
                pygame.draw.circle(surface, color, pos, particle['size'])

def load_music_files():
    music_files = []
    for file in os.listdir('.'):
        if file.endswith('.mp3'):
            music_files.append(file)
    return music_files

def main():
    # Buat button
    play_button = GlowButton(50, 500, 100, 40, "Play", (0, 200, 0))
    pause_button = GlowButton(170, 500, 100, 40, "Pause", (200, 200, 0))
    stop_button = GlowButton(290, 500, 100, 40, "Stop", (200, 0, 0))
    loop_button = GlowButton(410, 500, 100, 40, "Loop", (0, 0, 200))
    volume_up = GlowButton(530, 500, 100, 40, "Vol +", (0, 200, 200))
    volume_down = GlowButton(650, 500, 100, 40, "Vol -", (200, 0, 200))

    # Progress bar
    progress_rect = pygame.Rect(50, 450, 700, 15)

    # Inisialisasi status
    is_playing = False
    is_looping = False
    current_volume = 0.5
    mixer.music.set_volume(current_volume)
    
    # Load file musik
    music_files = load_music_files()
    if not music_files:
        print("Tidak ada file MP3 di direktori ini")
        return
    
    current_track = 0
    mixer.music.load(music_files[current_track])

    # Inisialisasi visualizer
    visualizer = TornadoVisualizer()

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle event button
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
        
        # Update dan gambar visualizer
        if is_playing:
            visualizer.update()
        visualizer.draw(screen)
        
        # Progress bar
        pygame.draw.rect(screen, (40, 40, 40), progress_rect)
        if is_playing:
            progress = mixer.music.get_pos() / 1000  # Konversi ke detik
            width = (progress % 60) / 60 * progress_rect.width
            progress_color = (100, 200, 255)
            pygame.draw.rect(screen, progress_color, 
                           (progress_rect.x, progress_rect.y, width, progress_rect.height))
            
            # Tampilkan waktu
            time_text = f"{int(progress)}s / 60s"
            time_surface = font.render(time_text, True, WHITE)
            screen.blit(time_surface, (progress_rect.x, progress_rect.y - 30))
        
        # Gambar button
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
