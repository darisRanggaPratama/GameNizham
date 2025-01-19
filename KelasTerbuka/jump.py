import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Pengaturan layar
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Kotak Melompat")

# Warna-warna (RGB)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
WHITE = (255, 255, 255)

# Daftar warna untuk rotasi
colors = [RED, YELLOW, GREEN, BLUE, PURPLE, BROWN]
current_color_index = 0

# Pengaturan kotak
box_size = 50
box_x = WINDOW_WIDTH // 2 - box_size // 2
box_y = WINDOW_HEIGHT - box_size
box_rect = pygame.Rect(box_x, box_y, box_size, box_size)

# Pengaturan lompatan
jump_height = 200
jump_speed = 7
is_jumping = False
jump_count = 10
gravity = 0.5
y_velocity = 0
initial_y = box_y

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Deteksi spasi untuk melompat
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                y_velocity = -15  # Kecepatan awal lompatan
                # Ganti warna
                current_color_index = (current_color_index + 1) % len(colors)

    # Update posisi kotak saat melompat
    if is_jumping:
        box_rect.y += y_velocity
        y_velocity += gravity

        # Cek jika kotak sudah kembali ke tanah
        if box_rect.y >= initial_y:
            box_rect.y = initial_y
            is_jumping = False
            y_velocity = 0

    # Bersihkan layar
    screen.fill(WHITE)

    # Gambar kotak
    pygame.draw.rect(screen, colors[current_color_index], box_rect)

    # Update tampilan
    pygame.display.flip()

    # Kontrol frame rate
    clock.tick(60)

pygame.quit()
sys.exit()