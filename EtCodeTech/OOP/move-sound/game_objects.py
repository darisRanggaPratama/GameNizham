# game_objects.py
import pygame as pg
import config


class Tank(pg.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        try:
            self.image = pg.image.load(image_path)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed_x = 0
            self.speed_y = 0
        except pg.error as e:
            print(f"Error loading tank image: {e}")
            raise

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, config.SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, config.SCREEN_HEIGHT - self.rect.height))

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.centery)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = config.BULLET_SPEED

    def update(self):
        self.rect.x += self.speed
