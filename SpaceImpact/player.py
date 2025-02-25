import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((0, 255, 0))  # Temporary green rectangle
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 300
        self.speed = 5
        self.health = 3
        self.shoot_delay = 250  # Milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y = max(0, self.rect.y - self.speed)
        if keys[pygame.K_DOWN]:
            self.rect.y = min(570, self.rect.y + self.speed)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            return True
        return False