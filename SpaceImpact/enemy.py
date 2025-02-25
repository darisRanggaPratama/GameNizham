import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface((40, 25))
        self.image.fill((255, 0, 0))  # Temporary red rectangle
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = random.randint(0, height - 25)
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()