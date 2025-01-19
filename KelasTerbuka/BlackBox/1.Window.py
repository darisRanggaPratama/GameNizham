import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Window title
pygame.display.set_caption("Set Window")

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Update the display
    pygame.display.flip()

# Penjelasan Kode
# 1. Inisialisasi PyGame: pygame.init() digunakan untuk menginisialisasi semua modul PyGame.
# 2. Membuat Jendela: pygame.display.set_mode() digunakan untuk membuat jendela dengan ukuran yang ditentukan.
# 3. Loop Utama: Ini adalah loop yang akan terus berjalan selama aplikasi berjalan. Di dalam loop ini, kita memeriksa event (seperti menutup jendela).
# 4. Mengisi Latar Belakang: screen.fill((255, 255, 255)) mengisi layar dengan warna putih.
# 5. Memperbarui Tampilan: pygame.display.flip() digunakan untuk memperbarui tampilan jendela.




