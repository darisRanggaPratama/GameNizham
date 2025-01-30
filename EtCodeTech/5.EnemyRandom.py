import pygame as pg
import random
import math

# initialize pygame
pg.init()

# set up the display
width, height = 1200, 700
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Tank Battle")

# Background Window
background = pg.image.load("OOP/picture/background.jpeg")
background = pg.transform.scale(background, (width, height))

# Logo/icon
logo = pg.image.load("OOP/picture/tanker.png")
pg.display.set_icon(logo)

# Colors
lightCoral = (240, 128, 128)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Sound effects
shooting_sound = pg.mixer.Sound("OOP/picture/tank-shots.mp3")  # Replace with your sound file
explosion_sound = pg.mixer.Sound("OOP/picture/tank-hits.mp3")  # Replace with your sound file


class Bullet:
    def __init__(self, x, y, is_player=True):
        self.x = x
        self.y = y
        self.speed = 7
        self.is_player = is_player
        self.radius = 5
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)] if not is_player else [YELLOW]
        self.current_color = 0
        self.size = 5

    def move(self):
        if self.is_player:
            self.x += self.speed
        else:
            self.x -= self.speed

    def draw(self):
        if self.is_player:
            # Sun-like bullet effect for player
            pg.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
            pg.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 2)

            # Add glowing effect
            for r in range(self.radius + 2, self.radius + 5):
                alpha = max(0, 255 - (r - self.radius) * 50)
                s = pg.Surface((r * 2, r * 2), pg.SRCALPHA)
                pg.draw.circle(s, (255, 255, 0, alpha), (r, r), r)
                screen.blit(s, (int(self.x) - r, int(self.y) - r))
        else:
            # Black hole effect for enemy bullets
            self.current_color = (self.current_color + 1) % len(self.colors)
            color = self.colors[self.current_color]
            self.size = max(3, min(7, self.size + random.uniform(-0.5, 0.5)))

            # Spiral effect
            t = pg.time.get_ticks() / 200
            for i in range(4):
                angle = t + i * math.pi / 2
                offset_x = math.cos(angle) * 3
                offset_y = math.sin(angle) * 3
                pg.draw.circle(screen, color,
                               (int(self.x + offset_x), int(self.y + offset_y)),
                               int(self.size))


class Enemy:
    def __init__(self):
        self.picture = pg.image.load("OOP/picture/tankers64.png")
        self.width = self.picture.get_width()
        self.height = self.picture.get_height()
        self.respawn()
        self.shoot_delay = random.randint(1000, 3000)
        self.last_shot = pg.time.get_ticks()
        self.bullets = []

    def respawn(self):
        self.x = random.randint(width - 200, width - self.width)
        self.y = random.randint(0, height - self.height)
        self.pointx = random.uniform(-0.2, -0.1)
        self.pointy = random.uniform(-0.1, 0.1)

    def move(self):
        self.x += self.pointx
        self.y += self.pointy

        # Bounce off screen edges
        if self.y <= 0 or self.y >= height - self.height:
            self.pointy *= -1
        if self.x <= width / 2 or self.x >= width - self.width:
            self.pointx *= -1

    def shoot(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.bullets.append(Bullet(self.x, self.y + self.height / 2, False))
            shooting_sound.play()
            self.last_shot = current_time

    def draw(self):
        screen.blit(self.picture, (self.x, self.y))


class Player:
    def __init__(self):
        self.picture = pg.image.load("OOP/picture/tanker64.png")
        self.x = 300
        self.y = 300
        self.x_point = 0
        self.y_point = 0
        self.bullets = []
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = 200  # Delay between shots in milliseconds

    def move(self):
        self.x += self.x_point
        self.y += self.y_point

        # Keep player in bounds
        self.x = max(0, min(self.x, width - self.picture.get_width()))
        self.y = max(0, min(self.y, height - self.picture.get_height()))

    def shoot(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.bullets.append(Bullet(self.x + self.picture.get_width(),
                                       self.y + self.picture.get_height() / 2))
            shooting_sound.play()
            self.last_shot = current_time

    def draw(self):
        screen.blit(self.picture, (self.x, self.y))


def check_collision(bullet, target):
    bullet_rect = pg.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius,
                          bullet.radius * 2, bullet.radius * 2)
    target_rect = pg.Rect(target.x, target.y, target.picture.get_width(),
                          target.picture.get_height())
    return bullet_rect.colliderect(target_rect)


# Create player and enemies
player = Player()
enemy_list = []
for i in range(random.randint(5, 10)):
    enemy_list.append(Enemy())

# Game loop
runs = True
while runs:
    screen.blit(background, (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            runs = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT or event.key == ord("a"):
                player.x_point = -0.3
            elif event.key == pg.K_RIGHT or event.key == ord("d"):
                player.x_point = 0.3
            elif event.key == pg.K_UP or event.key == ord("w"):
                player.y_point = -0.3
            elif event.key == pg.K_DOWN or event.key == ord("s"):
                player.y_point = 0.3

        if event.type == pg.KEYUP:
            if event.key in [pg.K_LEFT, ord("a"), pg.K_RIGHT, ord("d")]:
                player.x_point = 0
            elif event.key in [pg.K_UP, ord("w"), pg.K_DOWN, ord("s")]:
                player.y_point = 0

    # Player shooting
    player.shoot()  # Automatic shooting
    player.move()
    player.draw()

    # Update and draw player bullets
    for bullet in player.bullets[:]:
        bullet.move()
        bullet.draw()

        # Check for collision with enemies
        for enemy in enemy_list[:]:
            if check_collision(bullet, enemy):
                explosion_sound.play()
                enemy_list.remove(enemy)
                player.bullets.remove(bullet)
                enemy_list.append(Enemy())  # Spawn new enemy
                break

        # Remove bullets that are off screen
        if bullet.x > width:
            player.bullets.remove(bullet)

    # Update and draw enemies
    for enemy in enemy_list:
        enemy.move()
        enemy.draw()
        enemy.shoot()

        # Update and draw enemy bullets
        for bullet in enemy.bullets[:]:
            bullet.move()
            bullet.draw()

            # Check for collision with player
            if check_collision(bullet, player):
                explosion_sound.play()
                enemy.bullets.remove(bullet)

            # Remove bullets that are off screen
            if bullet.x < 0:
                enemy.bullets.remove(bullet)

    pg.display.update()

pg.quit()