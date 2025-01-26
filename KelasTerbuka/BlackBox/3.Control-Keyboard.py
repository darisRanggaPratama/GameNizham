import pygame as pg

# Initialize Pygame
pg.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))

# Window title
pg.display.set_caption("Keyboard Control")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Circle position
circle_x, circle_y = 400, 300
circle_speed = 1
circle_radius = 50

# Rectangle position
rectangle_x, rectangle_y = 100, 100
rectangle_width, rectangle_height = 100, 100
rectangle_speed = 1


# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Get keyboard input
    keys = pg.key.get_pressed()

    # Move circle
    if keys[pg.K_LEFT]:
        circle_x -= circle_speed
    if keys[pg.K_RIGHT]:
        circle_x += circle_speed
    if keys[pg.K_UP]:
        circle_y -= circle_speed
    if keys[pg.K_DOWN]:
        circle_y += circle_speed

    # Move rectangle
    if keys[pg.K_a]:
        rectangle_x -= rectangle_speed
    if keys[pg.K_d]:
        rectangle_x += rectangle_speed
    if keys[pg.K_w]:
        rectangle_y -= rectangle_speed
    if keys[pg.K_s]:
        rectangle_y += rectangle_speed

    # Clear the screen
    screen.fill(WHITE)

    # Draw the shape
    # Persegi panjang merah
    pg.draw.rect(screen, RED, (rectangle_x, rectangle_y, rectangle_width, rectangle_height))
    # Lingkaran hijau
    pg.draw.circle(screen, GREEN, (circle_x, circle_y), circle_radius)


    # Update the display
    pg.display.flip()


# 🔍 Konsep Utama:
# • Program membuat window grafis interaktif
# • Memungkinkan pergerakan objek menggunakan keyboard
# • Menggunakan library PyGame untuk grafis dan input

# 🖥️ Konfigurasi Awal:
# • Ukuran window: 800x600 pixel
# • Warna background: Putih
# • Objek utama: Lingkaran hijau dan Persegi merah

# 🎮 Kontrol Keyboard:
# • Panah (↑↓←→): Menggerakkan Lingkaran hijau
# • Tombol (WASD): Menggerakkan Persegi merah

# 🔑 Detail Pergerakan:
# • Kecepatan gerak: Sangat lambat (1 pixel per frame)
# • Kontrol real-time menggunakan tombol keyboard
# • Objek dapat bergerak di seluruh area window