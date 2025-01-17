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
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Pengaturan window
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MP3 Player dengan Visualisasi Tornado")

# Font
font = pygame.font.Font(None, 36)

class TombolBersinar:
    def __init__(self, x, y, width, height, text, warna_dasar):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.warna_dasar = warna_dasar
        self.is_hover = False
        self.waktu_sinar = random.uniform(0, 2 * math.pi)
        self.kecepatan_sinar = random.uniform(0.05, 0.15)

    def gambar(self, surface):
        self.waktu_sinar += self.kecepatan_sinar
        sinar = (math.sin(self.waktu_sinar) + 1) / 2
        warna = self.warna_dasar

        if self.is_hover:
            jumlah_sinar = int(60 * sinar)
            warna = tuple(min(255, c + jumlah_sinar) for c in self.warna_dasar)
            
            # Efek sinar di pinggir tombol
            for i in range(5):
                rect_sinar = self.rect.inflate(i * 6, i * 6)
                warna_sinar = tuple(max(0, min(255, c - 40 + jumlah_sinar)) for c in self.warna_dasar)
                pygame.draw.rect(surface, warna_sinar, rect_sinar, border_radius=15)

        pygame.draw.rect(surface, warna, self.rect, border_radius=15)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hover = self.rect.collidepoint(event.pos)
        return event.type == pygame.MOUSEBUTTONDOWN and self.is_hover

class VisualisasiTornado:
    def __init__(self):
        self.tornados = []
        self.buat_tornado(1)
        self.waktu_terakhir_split = pygame.time.get_ticks()
        self.interval_split = 2000  # 2 detik

    def buat_tornado(self, jumlah):
        if len(self.tornados) >= 9:
            return

        # Atur posisi tornado berdasarkan jumlah
        posisi = []
        if jumlah <= 3:
            # Satu baris
            for i in range(jumlah):
                x = WINDOW_WIDTH * (i + 1) / (jumlah + 1)
                posisi.append((x, WINDOW_HEIGHT // 3))
        elif jumlah <= 6:
            # Dua baris
            for i in range(3):
                x = WINDOW_WIDTH * (i + 1) / 4
                posisi.append((x, WINDOW_HEIGHT // 4))
            for i in range(jumlah - 3):
                x = WINDOW_WIDTH * (i + 1) / (jumlah - 2)
                posisi.append((x, WINDOW_HEIGHT // 2))
        else:
            # Tiga baris
            for i in range(3):
                x = WINDOW_WIDTH * (i + 1) / 4
                posisi.append((x, WINDOW_HEIGHT // 4))
            for i in range(3):
                x = WINDOW_WIDTH * (i + 1) / 4
                posisi.append((x, WINDOW_HEIGHT // 2))
            for i in range(jumlah - 6):
                x = WINDOW_WIDTH * (i + 1) / 4
                posisi.append((x, 3 * WINDOW_HEIGHT // 4))

        self.tornados = []
        size_multiplier = 1.0 / (jumlah ** 0.5)  # Tornado mengecil seiring bertambahnya jumlah
        
        for x, y in posisi:
            tornado = {
                'x': x,
                'y': y,
                'partikel': [],
                'warna': random.choice(COLORS),
                'kecepatan_rotasi': random.uniform(0.02, 0.05),
                'ukuran': size_multiplier
            }
            self.tornados.append(tornado)

    def buat_partikel(self, x, y, warna, ukuran):
        return {
            'x': x,
            'y': y,
            'sudut': random.uniform(0, 2 * math.pi),
            'radius': random.uniform(10, 50) * ukuran,
            'kecepatan': random.uniform(2, 5),
            'warna': warna,
            'ukuran': random.randint(2, 6) * ukuran,
            'kecerahan': random.randint(100, 255)
        }

    def update(self):
        waktu_sekarang = pygame.time.get_ticks()
        
        # Split tornado setiap interval
        if waktu_sekarang - self.waktu_terakhir_split > self.interval_split and len(self.tornados) < 9:
            self.waktu_terakhir_split = waktu_sekarang
            self.buat_tornado(len(self.tornados) + 1)

        for tornado in self.tornados:
            # Tambah partikel baru
            for _ in range(20):
                tornado['partikel'].append(
                    self.buat_partikel(tornado['x'], tornado['y'], tornado['warna'], tornado['ukuran']))

            # Update posisi dan properti partikel
            for partikel in tornado['partikel']:
                partikel['sudut'] += tornado['kecepatan_rotasi']
                partikel['radius'] -= partikel['kecepatan'] * 0.1
                partikel['kecerahan'] = max(0, partikel['kecerahan'] - random.uniform(1, 3))
                partikel['x'] = tornado['x'] + partikel['radius'] * math.cos(partikel['sudut'])
                partikel['y'] = tornado['y'] + partikel['radius'] * math.sin(partikel['sudut'])

            # Hapus partikel yang sudah redup
            tornado['partikel'] = [p for p in tornado['partikel'] if p['kecerahan'] > 0 and p['radius'] > 5]

    def gambar(self, surface):
        for tornado in self.tornados:
            for partikel in tornado['partikel']:
                warna = tuple(int(c * partikel['kecerahan'] / 255) for c in partikel['warna'])
                pos = (int(partikel['x']), int(partikel['y']))
                pygame.draw.circle(surface, warna, pos, int(partikel['ukuran']))

def load_music_files():
    return [file for file in os.listdir('.') if file.endswith('.mp3')]

def main():
    # Buat tombol-tombol
    play_button = TombolBersinar(50, 650, 100, 40, "Play", (0, 180, 0))
    pause_button = TombolBersinar(170, 650, 100, 40, "Pause", (180, 180, 0))
    stop_button = TombolBersinar(290, 650, 100, 40, "Stop", (180, 0, 0))
    loop_button = TombolBersinar(410, 650, 100, 40, "Loop", (0, 0, 180))
    volume_up = TombolBersinar(530, 650, 100, 40, "Vol +", (0, 180, 180))
    volume_down = TombolBersinar(650, 650, 100, 40, "Vol -", (180, 0, 180))

    # Progress bar
    progress_rect = pygame.Rect(50, 600, 700, 15)
    
    # Status awal
    is_playing = False
    is_looping = False
    current_volume = 0.5
    mixer.music.set_volume(current_volume)

    # Load file musik
    music_files = load_music_files()
    if not music_files:
        print("Tidak ada file MP3 dalam direktori")
        return

    current_track = 0
    mixer.music.load(music_files[current_track])
    track_length = mixer.Sound(music_files[current_track]).get_length()

    visualizer = VisualisasiTornado()
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle tombol-tombol
            if play_button.handle_event(event):
                if not is_playing:
                    mixer.music.play(-1 if is_looping else 0)
                    is_playing = True
                    visualizer = VisualisasiTornado()

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
                visualizer = VisualisasiTornado()

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

        # Update dan gambar visualisasi
        if is_playing:
            visualizer.update()
        visualizer.gambar(screen)

        # Gambar progress bar
        pygame.draw.rect(screen, (40, 40, 40), progress_rect)
        if is_playing:
            progress = mixer.music.get_pos() / 1000
            progress_width = min(progress / track_length * progress_rect.width, progress_rect.width)
            pygame.draw.rect(screen, (100, 200, 255), 
                           (progress_rect.x, progress_rect.y, progress_width, progress_rect.height))

        # Gambar tombol-tombol
        play_button.gambar(screen)
        pause_button.gambar(screen)
        stop_button.gambar(screen)
        loop_button.gambar(screen)
        volume_up.gambar(screen)
        volume_down.gambar(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
