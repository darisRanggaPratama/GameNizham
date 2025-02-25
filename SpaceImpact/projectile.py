import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, is_player=True):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        color = (255, 255, 0) if is_player else (255, 0, 0)  # Yellow for player, red for enemy
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7 if is_player else -5

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > 800 or self.rect.right < 0:
            self.kill()