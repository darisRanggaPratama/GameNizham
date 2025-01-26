import pygame as pg
import config
import random


class Tank(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, direction):
        super().__init__()
        try:
            self.image = pg.image.load(image_path)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed_x = 0
            self.speed_y = 0
            self.direction = direction  # 1 for right, -1 for left
            self.max_health = 100
            self.health = self.max_health
            self.score = 0
        except pg.error as e:
            print(f"Error loading tank image: {e}")
            raise

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, config.SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, config.SCREEN_HEIGHT - self.rect.height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        return self.health <= 0

    def shoot(self):
        # Adjust bullet position based on tank direction
        if self.direction == 1:  # Tank facing right
            bullet_x = self.rect.right  # Start from right side of tank
        else:  # Tank facing left
            bullet_x = self.rect.left  # Start from left side of tank

        return Bullet(bullet_x, self.rect.centery, self.direction)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.damage = 20  # Standard bullet damage

        # High-contrast colors for better visibility
        self.colors = [
            (255, 0, 0),    # Bright Red
            (0, 255, 0),    # Bright Green
            (0, 0, 255),    # Bright Blue
            (255, 255, 0),  # Bright Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255)   # Cyan
        ]

        # Create a slightly larger surface with alpha channel for better transparency
        self.image = pg.Surface((30, 30), pg.SRCALPHA)

        # Select random color with more vibrant options
        self.base_color = random.choice(self.colors)

        # Create a more complex, multi-layered bullet shape
        pg.draw.circle(self.image, self.base_color, (15, 15), 15)
        pg.draw.circle(self.image, (255, 255, 255, 200), (15, 15), 12, 3)  # bright White

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = config.BULLET_SPEED * 2 * direction
        self.direction = direction

    def update(self):
        # Move bullet
        self.rect.x += self.speed

        # Remove bullet if out of screen
        if self.rect.right < 0 or self.rect.left > config.SCREEN_WIDTH:
            self.kill()
