import pygame as pg
import sys


class GameControl:
    def __init__(self, width=800, height=600):
        # Inisialisasi pygame dengan error handling
        try:
            pg.init()
        except pg.error as e:
            print(f"Pygame initialization error: {e}")
            sys.exit(1)

        # Konfigurasi layar
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Keyboard Control Game")

        # Warna
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # Objek game
        self.circle = {
            'x': 400,
            'y': 300,
            'radius': 50,
            'speed': 5
        }

        self.rectangle = {
            'x': 100,
            'y': 100,
            'width': 100,
            'height': 100,
            'speed': 5
        }

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()

    def move_objects(self, keys):
        # Gerak lingkaran
        if keys[pg.K_LEFT]: self.circle['x'] -= self.circle['speed']
        if keys[pg.K_RIGHT]: self.circle['x'] += self.circle['speed']
        if keys[pg.K_UP]: self.circle['y'] -= self.circle['speed']
        if keys[pg.K_DOWN]: self.circle['y'] += self.circle['speed']

        # Gerak persegi panjang
        if keys[pg.K_a]: self.rectangle['x'] -= self.rectangle['speed']
        if keys[pg.K_d]: self.rectangle['x'] += self.rectangle['speed']
        if keys[pg.K_w]: self.rectangle['y'] -= self.rectangle['speed']
        if keys[pg.K_s]: self.rectangle['y'] += self.rectangle['speed']

    def draw_objects(self):
        self.screen.fill(self.WHITE)

        # Gambar objek
        pg.draw.rect(
            self.screen,
            self.RED,
            (self.rectangle['x'], self.rectangle['y'],
             self.rectangle['width'], self.rectangle['height'])
        )
        pg.draw.circle(
            self.screen,
            self.GREEN,
            (self.circle['x'], self.circle['y']),
            self.circle['radius']
        )

        pg.display.flip()

    def run(self):
        try:
            clock = pg.time.Clock()
            while True:
                self.handle_events()
                keys = pg.key.get_pressed()
                self.move_objects(keys)
                self.draw_objects()
                clock.tick(60)  # Batasi frame rate
        except Exception as e:
            print(f"Game error: {e}")
        finally:
            self.quit_game()

    def quit_game(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = GameControl()
    game.run()
    


# ✨ Keunggulan Kode Baru

# Menggunakan OOP (Object-Oriented Programming)
# Error handling yang lebih komprehensif
# Konfigurasi objek yang lebih fleksibel
# Kontrol frame rate dengan clock.tick()
# Pemisahan logika yang lebih baik

# 🔒 Error Handling Tambahan

# Inisialisasi PyGame dengan try-except
# Penanganan event quit
# Kontrol eksepsi saat menjalankan game
# Metode quit_game() untuk keluar dengan aman