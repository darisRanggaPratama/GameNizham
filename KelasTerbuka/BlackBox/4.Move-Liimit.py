import pygame as pg
import sys


class GameControl:
    def __init__(self, width=800, height=600, scale_factor=1.0):
        # Inisialisasi pygame dengan error handling
        try:
            pg.init()
        except pg.error as e:
            print(f"Pygame initialization error: {e}")
            sys.exit(1)

        # Konfigurasi resolusi dengan scaling
        self.ORIGINAL_WIDTH = width
        self.ORIGINAL_HEIGHT = height

        # Hitung resolusi yang di-scale
        self.WIDTH = int(width * scale_factor)
        self.HEIGHT = int(height * scale_factor)

        # Konfigurasi layar
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT), pg.RESIZABLE)
        pg.display.set_caption("Advanced Pygame Game")

        # Warna
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.PURPLE = (255, 0, 255)

        # Objek game dengan scaling
        self.circle = {
            'x': int(400 * scale_factor),
            'y': int(300 * scale_factor),
            'radius': int(50 * scale_factor),
            'speed': int(5 * scale_factor)
        }

        self.rectangle = {
            'x': int(100 * scale_factor),
            'y': int(100 * scale_factor),
            'width': int(100 * scale_factor),
            'height': int(100 * scale_factor),
            'speed': int(5 * scale_factor)
        }

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            # Tambahan event handling untuk resize
            elif event.type == pg.VIDEORESIZE:
                self.WIDTH, self.HEIGHT = event.size
                self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT), pg.RESIZABLE)

    def move_objects(self, keys):
        # Gerak lingkaran dengan batasan
        if keys[pg.K_LEFT]:
            self.circle['x'] = max(self.circle['radius'],
                                   min(self.circle['x'] - self.circle['speed'],
                                       self.WIDTH - self.circle['radius']))
        if keys[pg.K_RIGHT]:
            self.circle['x'] = max(self.circle['radius'],
                                   min(self.circle['x'] + self.circle['speed'],
                                       self.WIDTH - self.circle['radius']))
        if keys[pg.K_UP]:
            self.circle['y'] = max(self.circle['radius'],
                                   min(self.circle['y'] - self.circle['speed'],
                                       self.HEIGHT - self.circle['radius']))
        if keys[pg.K_DOWN]:
            self.circle['y'] = max(self.circle['radius'],
                                   min(self.circle['y'] + self.circle['speed'],
                                       self.HEIGHT - self.circle['radius']))

        # Gerak persegi panjang dengan batasan
        if keys[pg.K_a]:
            self.rectangle['x'] = max(0,
                                      min(self.rectangle['x'] - self.rectangle['speed'],
                                          self.WIDTH - self.rectangle['width']))
        if keys[pg.K_d]:
            self.rectangle['x'] = max(0,
                                      min(self.rectangle['x'] + self.rectangle['speed'],
                                          self.WIDTH - self.rectangle['width']))
        if keys[pg.K_w]:
            self.rectangle['y'] = max(0,
                                      min(self.rectangle['y'] - self.rectangle['speed'],
                                          self.HEIGHT - self.rectangle['height']))
        if keys[pg.K_s]:
            self.rectangle['y'] = max(0,
                                      min(self.rectangle['y'] + self.rectangle['speed'],
                                          self.HEIGHT - self.rectangle['height']))

    def check_collision(self):
        # Deteksi tabrakan antara lingkaran dan persegi
        circle_rect = pg.Rect(
            self.circle['x'] - self.circle['radius'],
            self.circle['y'] - self.circle['radius'],
            self.circle['radius'] * 2,
            self.circle['radius'] * 2
        )

        rectangle_rect = pg.Rect(
            self.rectangle['x'],
            self.rectangle['y'],
            self.rectangle['width'],
            self.rectangle['height']
        )

        return circle_rect.colliderect(rectangle_rect)

    def draw_objects(self, collision_color=None):
        # Bersihkan layar
        self.screen.fill(self.WHITE)

        # Warna default atau warna collision
        rect_color = collision_color if collision_color else self.RED
        circle_color = self.GREEN

        # Gambar objek
        pg.draw.rect(
            self.screen,
            rect_color,
            (self.rectangle['x'], self.rectangle['y'],
             self.rectangle['width'], self.rectangle['height'])
        )
        pg.draw.circle(
            self.screen,
            circle_color,
            (self.circle['x'], self.circle['y']),
            self.circle['radius']
        )

        # Update tampilan
        pg.display.flip()

    def run(self):
        try:
            clock = pg.time.Clock()

            while True:
                self.handle_events()
                keys = pg.key.get_pressed()

                self.move_objects(keys)

                # Cek dan tampilkan collision
                if self.check_collision():
                    self.draw_objects(collision_color=(255, 0, 255))
                else:
                    self.draw_objects()

                clock.tick(60)  # Batasi frame rate
        except Exception as e:
            print(f"Game error: {e}")
        finally:
            self.quit_game()

    def quit_game(self):
        pg.quit()
        sys.exit()


# Menjalankan game dengan berbagai pilihan scaling
def main():
    # Pilih salah satu opsi scaling
    game_normal = GameControl(width=800, height=600)  # Resolusi normal
    # game_scaled = GameControl(width=800, height=600, scale_factor=1.5)  # Resolusi diperbesar
    # game_small = GameControl(width=800, height=600, scale_factor=0.75)  # Resolusi diperkecil

    game_normal.run()


if __name__ == "__main__":
    main()


# 🚀 Fitur Utama yang Ditambahkan:

# Scaling Resolusi
#
# Parameter scale_factor untuk mengubah ukuran layar
# Penyesuaian otomatis ukuran objek
# Dukungan resize window

# Batasan Pergerakan
#
# Pembatasan gerakan objek di dalam layar
# Mencegah objek keluar dari area permainan

# Collision Detection
#
# Deteksi tabrakan antara lingkaran dan persegi
# Perubahan warna saat terjadi tabrakan

# 🔧 Cara Penggunaan
#
# Jalankan script untuk memulai game
# Gunakan arrow keys untuk menggerakkan lingkaran
# Gunakan WASD untuk menggerakkan persegi