import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Massa dan kecepatan
m_A = 800  # kg
v_A_i = 20  # m/s
m_B = 1200  # kg
v_B_i = -10  # m/s

# Menghitung kecepatan akhir setelah tumbukan tidak lenting
v_f = (m_A * v_A_i + m_B * v_B_i) / (m_A + m_B)

# Posisi awal kotak
pos_A = 100
pos_B = 600

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulasi Tumbukan Tidak Lenting Sama Sekali")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mengisi latar belakang
    screen.fill(WHITE)

    # Menggambar kotak A dan B
    pygame.draw.rect(screen, BLUE, (pos_A, HEIGHT // 2 - 25, 50, 50))  # Kotak A
    pygame.draw.rect(screen, RED, (pos_B, HEIGHT // 2 - 25, 50, 50))   # Kotak B

    # Update posisi kotak
    pos_A += v_A_i * 0.05  # Update posisi A
    pos_B += v_B_i * 0.05  # Update posisi B

    # Cek tumbukan
    if pos_A + 50 >= pos_B:  # Jika kotak A dan B bertumbukan
        pos_A = pos_B - 50  # Mengatur posisi agar tidak saling menembus
        v_A_i = v_f  # Kecepatan baru untuk kotak A
        v_B_i = v_f  # Kecepatan baru untuk kotak B

    # Menggambar kecepatan akhir
    font = pygame.font.Font(None, 36)
    text = font.render(f'Kecepatan Akhir: {v_f:.2f} m/s', True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # Memperbarui tampilan
    pygame.display.flip()
    pygame.time.delay(50)

# Keluar dari Pygame
pygame.quit()
sys.exit()