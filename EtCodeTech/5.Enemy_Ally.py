import pygame as pg
import random
import math
import time

# initialize pygame
pg.init()

# set up the display
width, height = 800, 600
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
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font setup
font = pg.font.Font(None, 36)

# Sound effects
shooting_sound = pg.mixer.Sound("OOP/picture/tank-shots.mp3")
explosion_sound = pg.mixer.Sound("OOP/picture/tank-hits.mp3")


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
        self.damage = 10  # Damage per bullet

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
    def __init__(self, is_main=True):
        self.picture = pg.image.load("OOP/picture/tanker64.png")
        self.x = 300
        self.y = 300
        self.x_point = 0
        self.y_point = 0
        self.bullets = []
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = 200
        self.health = 100
        self.is_main = is_main

    def move(self, leader=None):
        if self.is_main:
            self.x += self.x_point
            self.y += self.y_point
        else:
            # Follower tank behavior - follows the leader with slight delay
            target_x = leader.x - 80  # Position slightly behind leader
            target_y = leader.y

            # Smooth movement towards leader
            dx = target_x - self.x
            dy = target_y - self.y
            self.x += dx * 0.1
            self.y += dy * 0.1

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

        # Draw health bar
        bar_width = self.picture.get_width()
        bar_height = 5
        health_width = (self.health / 100) * bar_width

        # Background (red) health bar
        pg.draw.rect(screen, RED,
                     (self.x, self.y - 10, bar_width, bar_height))
        # Foreground (green) health bar
        pg.draw.rect(screen, GREEN,
                     (self.x, self.y - 10, health_width, bar_height))


def check_collision(bullet, target):
    bullet_rect = pg.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius,
                          bullet.radius * 2, bullet.radius * 2)
    target_rect = pg.Rect(target.x, target.y, target.picture.get_width(),
                          target.picture.get_height())
    return bullet_rect.colliderect(target_rect)


# Initialize game state
players = [Player(is_main=True)]  # Start with main tank
enemy_list = []
for i in range(random.randint(5, 10)):
    enemy_list.append(Enemy())

score = 0
game_start_time = None
game_time = 0

# Game loop
runs = True
while runs:
    screen.blit(background, (0, 0))

    # Start timer when player first moves
    if game_start_time is None and (players[0].x_point != 0 or players[0].y_point != 0):
        game_start_time = time.time()

    # Update game time
    if game_start_time is not None:
        game_time = int(time.time() - game_start_time)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            runs = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT or event.key == ord("a"):
                players[0].x_point = -0.3
            elif event.key == pg.K_RIGHT or event.key == ord("d"):
                players[0].x_point = 0.3
            elif event.key == pg.K_UP or event.key == ord("w"):
                players[0].y_point = -0.3
            elif event.key == pg.K_DOWN or event.key == ord("s"):
                players[0].y_point = 0.3

        if event.type == pg.KEYUP:
            if event.key in [pg.K_LEFT, ord("a"), pg.K_RIGHT, ord("d")]:
                players[0].x_point = 0
            elif event.key in [pg.K_UP, ord("w"), pg.K_DOWN, ord("s")]:
                players[0].y_point = 0

    # Check if new tank should be added (every 100 points)
    if score >= 100 * len(players) and len(players) < 3:  # Limit to 3 tanks
        players.append(Player(is_main=False))

    # Update and draw players
    for i, player in enumerate(players):
        player.move(players[0] if i > 0 else None)  # Pass leader for follower tanks
        player.shoot()
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
                    enemy_list.append(Enemy())
                    score += 10
                    break

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

            # Check for collision with players
            for player in players[:]:
                if check_collision(bullet, player):
                    explosion_sound.play()
                    enemy.bullets.remove(bullet)
                    player.health -= bullet.damage

                    if player.health <= 0 and len(players) > 1:
                        players.remove(player)
                    break

            if bullet.x < 0:
                enemy.bullets.remove(bullet)

    # Draw UI elements
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    time_text = font.render(f"Time: {game_time}s", True, WHITE)
    screen.blit(time_text, (10, 50))

    pg.display.update()

pg.quit()