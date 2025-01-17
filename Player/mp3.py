import pygame
import random
import numpy as np
from pygame import gfxdraw
from mutagen.mp3 import MP3
import os
from numpy.fft import fft

# Inisialisasi PyGame
pygame.init()
pygame.mixer.init()

# Konstanta
WIDTH = 800
HEIGHT = 600
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0),    # Merah
    (0, 255, 0),    # Hijau
    (0, 0, 255),    # Biru
    (255, 255, 0),  # Kuning
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
]

class MusicVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MP3 Player dengan Visualisasi")
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.current_song = None
        self.particles = []
        
    def load_music(self, music_file):
        """Memuat file musik MP3"""
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            self.current_song = music_file
            self.audio = MP3(music_file)
            return True
        return False
    
    def create_particle(self):
        """Membuat partikel baru dengan properti random"""
        return {
            'x': random.randint(0, WIDTH),
            'y': random.randint(0, HEIGHT),
            'radius': random.randint(2, 20),
            'color': random.choice(COLORS),
            'speed': random.uniform(1, 5),
            'direction': random.uniform(0, 2 * np.pi)
        }
    
    def update_particles(self):
        """Mengupdate posisi dan properti partikel"""
        # Update partikel yang ada
        for particle in self.particles:
            particle['x'] += np.cos(particle['direction']) * particle['speed']
            particle['y'] += np.sin(particle['direction']) * particle['speed']
            
            # Jika partikel keluar layar, reset posisinya
            if particle['x'] < 0 or particle['x'] > WIDTH:
                particle['x'] = random.randint(0, WIDTH)
            if particle['y'] < 0 or particle['y'] > HEIGHT:
                particle['y'] = random.randint(0, HEIGHT)
                
        # Tambah partikel baru jika musik sedang dimainkan
        if self.playing and len(self.particles) < 50:
            self.particles.append(self.create_particle())
    
    def draw(self):
        """Menggambar visualisasi"""
        self.screen.fill(BLACK)
        
        # Gambar semua partikel
        for particle in self.particles:
            gfxdraw.filled_circle(
                self.screen,
                int(particle['x']),
                int(particle['y']),
                particle['radius'],
                particle['color']
            )
            
        # Gambar informasi lagu yang sedang diputar
        if self.current_song:
            font = pygame.font.Font(None, 36)
            song_name = os.path.basename(self.current_song)
            text = font.render(f"Now Playing: {song_name}", True, WHITE)
            self.screen.blit(text, (10, HEIGHT - 40))
            
        pygame.display.flip()
    
    def handle_events(self):
        """Menangani input pengguna"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.playing:
                        pygame.mixer.music.pause()
                        self.playing = False
                    else:
                        pygame.mixer.music.unpause()
                        self.playing = True
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def run(self):
        """Loop utama aplikasi"""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            if self.playing:
                self.update_particles()
            self.draw()

        pygame.quit()

# Contoh penggunaan
if __name__ == "__main__":
    visualizer = MusicVisualizer()
    
    # Ganti dengan path ke file MP3 Anda
    music_file = "music.mp3"
    
    if visualizer.load_music(music_file):
        pygame.mixer.music.play()
        visualizer.playing = True
        visualizer.run()
    else:
        print("Error: File musik tidak ditemukan!")
