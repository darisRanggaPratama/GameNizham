import pygame
import sys

# Inisialisasi PyGame
pygame.init()

# Ukuran layar
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spacewar - 1962 Remake")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Background
background = pygame.image.load("tank/assets/background.jpeg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Kapal luar angkasa
ship1 = pygame.image.load("tank/assets/tanker64.png")
ship1 = pygame.transform.scale(ship1, (50, 50))
ship2 = pygame.image.load("tank/assets/tankers64.png")
ship2 = pygame.transform.scale(ship2, (50, 50))

# Posisi kapal
ship1_x, ship1_y = 100, SCREEN_HEIGHT // 2
ship2_x, ship2_y = SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2

# Kecepatan
ship_speed = 5
bullet_speed = 10

# Peluru
bullets1 = []  # Peluru dari ship1
bullets2 = []  # Peluru dari ship2

# Suara
shoot_sound = pygame.mixer.Sound("tank/assets/tank-shots.mp3")
hit_sound = pygame.mixer.Sound("tank/assets/tank-explode.mp3")

# Skor
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Kontrol kapal
    keys = pygame.key.get_pressed()
    # Kapal 1 (WASD)
    if keys[pygame.K_w] and ship1_y > 0:
        ship1_y -= ship_speed
    if keys[pygame.K_s] and ship1_y < SCREEN_HEIGHT - 50:
        ship1_y += ship_speed
    if keys[pygame.K_SPACE]:  # Tembak peluru
        bullets1.append([ship1_x + 50, ship1_y + 25])
        shoot_sound.play()

    # Kapal 2 (Arrow keys)
    if keys[pygame.K_UP] and ship2_y > 0:
        ship2_y -= ship_speed
    if keys[pygame.K_DOWN] and ship2_y < SCREEN_HEIGHT - 50:
        ship2_y += ship_speed
    if keys[pygame.K_RETURN]:  # Tembak peluru
        bullets2.append([ship2_x - 10, ship2_y + 25])
        shoot_sound.play()

    # Update peluru
    for bullet in bullets1:
        bullet[0] += bullet_speed
        if bullet[0] > SCREEN_WIDTH:
            bullets1.remove(bullet)
        elif ship2_x < bullet[0] < ship2_x + 50 and ship2_y < bullet[1] < ship2_y + 50:
            bullets1.remove(bullet)
            score1 += 1
            hit_sound.play()

    for bullet in bullets2:
        bullet[0] -= bullet_speed
        if bullet[0] < 0:
            bullets2.remove(bullet)
        elif ship1_x < bullet[0] < ship1_x + 50 and ship1_y < bullet[1] < ship1_y + 50:
            bullets2.remove(bullet)
            score2 += 1
            hit_sound.play()

    # Gambar kapal dan peluru
    screen.blit(ship1, (ship1_x, ship1_y))
    screen.blit(ship2, (ship2_x, ship2_y))

    for bullet in bullets1:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], 10, 5))

    for bullet in bullets2:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], 10, 5))

    # Tampilkan skor
    score_text = font.render(f"Player 1: {score1}  Player 2: {score2}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 150, 20))

    # Update layar
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
