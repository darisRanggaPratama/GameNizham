import pygame as pg
import random
import math
import time

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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
    def __init__(self, x, y, is_main=True, control_scheme='arrows'):
        self.picture = pg.image.load("OOP/picture/tanker64.png")
        self.x = x
        self.y = y
        self.x_point = 0
        self.y_point = 0
        self.bullets = []
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = 200
        self.health = 100
        self.is_main = is_main
        self.control_scheme = control_scheme

        # Different colors for different tanks
        if control_scheme == 'arrows':
            self.color = RED
        else:
            self.color = BLUE

    def handle_input(self, keys):
        if self.control_scheme == 'arrows':
            # Arrow keys control
            if keys[pg.K_LEFT]:
                self.x_point = -0.3
            elif keys[pg.K_RIGHT]:
                self.x_point = 0.3
            else:
                self.x_point = 0

            if keys[pg.K_UP]:
                self.y_point = -0.3
            elif keys[pg.K_DOWN]:
                self.y_point = 0.3
            else:
                self.y_point = 0
        else:
            # WASD control
            if keys[pg.K_a]:
                self.x_point = -0.3
            elif keys[pg.K_d]:
                self.x_point = 0.3
            else:
                self.x_point = 0

            if keys[pg.K_w]:
                self.y_point = -0.3
            elif keys[pg.K_s]:
                self.y_point = 0.3
            else:
                self.y_point = 0

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

        # Draw health bar
        bar_width = self.picture.get_width()
        bar_height = 5
        health_width = (self.health / 100) * bar_width

        # Background (red) health bar
        pg.draw.rect(screen, RED,
                     (self.x, self.y - 10, bar_width, bar_height))
        # Foreground (green) health bar
        pg.draw.rect(screen, self.color,
                     (self.x, self.y - 10, health_width, bar_height))


def check_collision(bullet, target):
    bullet_rect = pg.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius,
                          bullet.radius * 2, bullet.radius * 2)
    target_rect = pg.Rect(target.x, target.y, target.picture.get_width(),
                          target.picture.get_height())
    return bullet_rect.colliderect(target_rect)


def reset_game():
    global players, enemy_list, score, game_start_time, game_time, game_active, game_over_time, winner
    players = [Player(x=200, y=300, is_main=True, control_scheme='arrows')]
    enemy_list = []
    for i in range(random.randint(5, 10)):
        enemy_list.append(Enemy())
    score = 0
    game_start_time = None
    game_time = 0
    game_active = True
    game_over_time = None
    winner = None


# Initialize game state
players = [
    Player(x=200, y=300, is_main=True, control_scheme='arrows'),  # First tank (Arrow keys)
]
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

    # Start timer when any player first moves
    if game_start_time is None and any(p.x_point != 0 or p.y_point != 0 for p in players):
        game_start_time = time.time()

    # Update game time
    if game_start_time is not None:
        game_time = int(time.time() - game_start_time)

    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            runs = False

    # Get keyboard state
    keys = pg.key.get_pressed()

    # Check if new tank should be added (at 100 points)
    if score >= 100 and len(players) == 1:
        players.append(Player(x=100, y=300, is_main=True, control_scheme='wasd'))  # Second tank (WASD)

    # Update and draw players
    for player in players:
        player.handle_input(keys)
        player.move()
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

    # Draw control scheme reminder
    if len(players) == 2:
        controls_text = font.render("Tank 1: Arrows | Tank 2: WASD", True, WHITE)
        screen.blit(controls_text, (width - 400, 10))

    pg.display.update()

pg.quit()
