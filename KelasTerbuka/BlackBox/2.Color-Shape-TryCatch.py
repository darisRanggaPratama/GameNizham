import pygame

# Initialize Pygame
try:
    pygame.init()
except Exception as e:
    print(f"Error initializing Pygame: {e}")
    exit()

# Set up the display
WIDTH, HEIGHT = 800, 600
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
except Exception as e:
    print(f"Error setting up display: {e}")
    exit()

# Window title
pygame.display.set_caption("Color & Shape")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw rectangles
    try:
        pygame.draw.rect(screen, RED, (50, 50, 100, 100))
        pygame.draw.rect(screen, ORANGE, (200, 50, 100, 100))
        pygame.draw.rect(screen, BROWN, (350, 50, 100, 100))

        # Draw circles
        pygame.draw.circle(screen, RED, (50, 250), 50)
        pygame.draw.circle(screen, ORANGE, (200, 250), 50)
        pygame.draw.circle(screen, BROWN, (350, 250), 50)

        # Draw lines
        pygame.draw.line(screen, RED, (50, 450), (150, 450), 5)
        pygame.draw.line(screen, ORANGE, (200, 450), (300, 450), 5)
        pygame.draw.line(screen, BROWN, (350, 450), (450, 450), 5)
    except Exception as e:
        print(f"Error drawing shapes: {e}")

    # Update the display
    try:
        pygame.display.flip()
    except Exception as e:
        print(f"Error updating display: {e}")

# Quit Pygame
pygame.quit()

# 🔍 Konsep Dasar:
# • Program ini seperti "kanvas digital" yang membuat gambar-gambar geometri
# • Menggunakan PyGame untuk membuat tampilan grafis

# 🖼️ Struktur Program:#
# 1. Persiapan Awal
# • Memuat library PyGame
# • Membuat window/layar grafis
# • Menentukan ukuran layar (800x600 pixel)
#
# 2. Warna yang Digunakan
# • Putih (background)
# • Merah • Oranye • Cokelat

# 📐 Objek yang Digambar: • 3 Persegi Warna • 3 Lingkaran Warna • 3 Garis Warna
#
# 🛡️ Fitur Keamanan: • Menggunakan error handling (try-except) • Mencegah program crash saat ada masalah • Menampilkan pesan error jika terjadi kesalahan

