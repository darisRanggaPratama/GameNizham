import pygame
import random
import math

import sys

# Inisialisasi Pygame
pygame.init()

# Set ukuran layar
widthScreen = 640
heightScreen = 480
screen = pygame.display.set_mode((widthScreen, heightScreen))

# Set judul layar
pygame.display.set_caption("Space Impact")


# Set FPS (frame per second)
fps = 60
jam = pygame.time.Clock()

backgrounds = [
        pygame.transform.scale(pygame.image.load("background0.jpg"), (widthScreen, heightScreen)),
        pygame.transform.scale(pygame.image.load("background1.png"), (widthScreen, heightScreen)),
        pygame.transform.scale(pygame.image.load("background2.jpg"), (widthScreen, heightScreen)),
        pygame.transform.scale(pygame.image.load("background3.jpeg"), (widthScreen, heightScreen)),
        pygame.transform.scale(pygame.image.load("background4.jpg"), (widthScreen, heightScreen)),
        pygame.transform.scale(pygame.image.load("background5.jpg"), (widthScreen, heightScreen))
    ]

index = 0

font = pygame.font.Font("SHPinscher-Regular.otf", 35)

spaceship = pygame.image.load("space_ship.png")
enemy_spaceship = pygame.image.load("enemy-spaceship.png")
enemy_missile_craft = pygame.image.load("enemy-ship.png")
bullet = pygame.image.load("torpedo-left.png")
enemy_bullet = pygame.image.load("missile-right.png")
missile = pygame.image.load("missile-xright.png")
explode = pygame.image.load("boom1.png")
enemy_explode = pygame.image.load("boom2.png")
asteroid = pygame.image.load("asteroid.png")

shoot_sound = pygame.mixer.Sound("tank-shots.mp3")
enemy_shoot_sound = pygame.mixer.Sound("tank-hits.mp3")
explosion_sound = pygame.mixer.Sound("tank-explode.mp3")
background_music = pygame.mixer.Sound("background.mp3")
victory_sound = pygame.mixer.Sound("victory.mp3")  # Add victory sound
defeat_sound = pygame.mixer.Sound("defeat.mp3")  # Add defeat sound

# Fungsi utama game
def main():
    global index
    while True:
        # Cek event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display background
        index = (index + 1) % len(backgrounds)
        screen.blit(backgrounds[index], (0, 0))

        # Update layar
        pygame.display.flip()
        jam.tick(fps)

# Jalankan game
if __name__ == "__main__":
    main()