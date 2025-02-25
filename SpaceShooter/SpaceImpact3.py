import pygame
import random
import math
import sys

# Inisialisasi Pygame
pygame.init()

# Set ukuran layar
widthScreen = 1600
heightScreen = 1000
screen = pygame.display.set_mode((widthScreen, heightScreen))
pygame.display.set_caption("Space Impact")

# Set FPS
fps = 60
clock = pygame.time.Clock()

# Memuat aset
backgrounds = [
    pygame.transform.scale(pygame.image.load("background0.jpeg"), (widthScreen, heightScreen)),
    pygame.transform.scale(pygame.image.load("background1.png"), (widthScreen, heightScreen)),
    pygame.transform.scale(pygame.image.load("background2.jpg"), (widthScreen, heightScreen)),
    pygame.transform.scale(pygame.image.load("background3.jpeg"), (widthScreen, heightScreen)),
    pygame.transform.scale(pygame.image.load("background4.jpg"), (widthScreen, heightScreen)),
    pygame.transform.scale(pygame.image.load("background5.jpg"), (widthScreen, heightScreen))
]
current_background_index = 0
background_change_timer = 0
background_change_interval = 5000  # 5 detik

font = pygame.font.Font("SHPinscher-Regular.otf", 35)
spaceship = pygame.image.load("space_ship.png")
enemy_spaceship_img = pygame.image.load("enemy-spaceship.png")
enemy_missile_craft_img = pygame.image.load("enemy-ship.png")
asteroid_img = pygame.image.load("asteroid.png")
bullet_img = pygame.image.load("torpedo-left.png")
enemy_bullet_img = pygame.image.load("missile-right.png")
missile_img = pygame.image.load("missile-xright.png")
explode_img = pygame.image.load("boom1.png")
enemy_explode_img = pygame.image.load("boom2.png")

# Suara
shoot_sound = pygame.mixer.Sound("tank-shots.mp3")
enemy_shoot_sound = pygame.mixer.Sound("tank-hits.mp3")
explosion_sound = pygame.mixer.Sound("tank-explode.mp3")
background_music = pygame.mixer.Sound("background1.mp3")
victory_sound = pygame.mixer.Sound("victory.mp3")
defeat_sound = pygame.mixer.Sound("defeat.mp3")

# Putar musik latar
background_music.play(-1)

# Kelas
class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship
        self.rect = self.image.get_rect()
        self.last_shoot_time = 0
        self.cooldown = 500  # milidetik

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.centerx = max(50, min(widthScreen - 50, mouse_x))
        self.rect.centery = max(50, min(heightScreen - 50, mouse_y))

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.cooldown:
            bullet = Bullet(self.rect.right, self.rect.centery, "right", bullet_img)
            player_bullets.add(bullet)
            all_sprites.add(bullet)
            self.last_shoot_time = current_time
            shoot_sound.play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, speed, shoot_interval, bullet_img=None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.shoot_interval = shoot_interval
        self.bullet_img = bullet_img
        self.last_shoot_time = 0
        self.timer = 0

    def update(self):
        self.rect.x -= self.speed
        self.timer += 1
        self.move_pattern()
        current_time = pygame.time.get_ticks()
        if self.shoot_interval and current_time - self.last_shoot_time >= self.shoot_interval:
            self.shoot()
            self.last_shoot_time = current_time
        if self.rect.right < 0:
            self.kill()

    def move_pattern(self):
        pass

    def shoot(self):
        if self.bullet_img:
            player_pos = (player_ship.rect.centerx, player_ship.rect.centery)
            enemy_pos = (self.rect.centerx, self.rect.centery)
            direction = pygame.math.Vector2(player_pos) - pygame.math.Vector2(enemy_pos)
            if direction.length() > 0:
                direction.normalize_ip()
            bullet = Bullet(self.rect.left, self.rect.centery, direction, self.bullet_img)
            enemy_bullets.add(bullet)
            all_sprites.add(bullet)
            enemy_shoot_sound.play()

class StraightEnemy(Enemy):
    pass  # Bergerak lurus

class ZigzagEnemy(Enemy):
    def __init__(self, image, speed, shoot_interval, bullet_img=None):
        super().__init__(image, speed, shoot_interval, bullet_img)
        self.direction = 1
        self.zigzag_timer = 0
        self.zigzag_speed = 2

    def move_pattern(self):
        self.zigzag_timer += 1
        if self.zigzag_timer >= 30:
            self.direction *= -1
            self.zigzag_timer = 0
        self.rect.y += self.direction * self.zigzag_speed

class SinusoidalEnemy(Enemy):
    def __init__(self, image, speed, shoot_interval, bullet_img=None):
        super().__init__(image, speed, shoot_interval, bullet_img)
        self.initial_y = self.rect.y
        self.amplitude = 50
        self.frequency = 0.05

    def move_pattern(self):
        self.rect.y = self.initial_y + self.amplitude * math.sin(self.frequency * self.timer)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        if isinstance(direction, str):
            self.velocity = pygame.math.Vector2(10, 0) if direction == "right" else pygame.math.Vector2(-10, 0)
        else:
            self.velocity = direction * 10

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if self.rect.right < 0 or self.rect.left > widthScreen or self.rect.bottom < 0 or self.rect.top > heightScreen:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= 30:
            self.kill()

# Grup sprite
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Buat kapal pemain
player_ship = PlayerShip()
all_sprites.add(player_ship)

# Level
levels = [
    {"enemies": [{"type": "spaceship", "count": 5}, {"type": "missile_craft", "count": 3},
                 {"type": "asteroid", "count": 2}]},
    {"enemies": [{"type": "spaceship", "count": 3}, {"type": "missile_craft", "count": 5},
                 {"type": "asteroid", "count": 3}]},
    {"enemies": [{"type": "spaceship", "count": 2}, {"type": "missile_craft", "count": 3},
                 {"type": "asteroid", "count": 5}]},
]

# Variabel permainan
current_level = 0
score = 0
lives = 3
game_state = "playing"
background_x = 0

# Fungsi untuk memulai level baru
def start_level(level_index):
    global enemies_to_spawn
    level_data = levels[level_index]
    enemies_to_spawn = []
    for enemy_type in level_data["enemies"]:
        for _ in range(enemy_type["count"]):
            if enemy_type["type"] == "spaceship":
                enemies_to_spawn.append(StraightEnemy(enemy_spaceship_img, 3, 2000, enemy_bullet_img))
            elif enemy_type["type"] == "missile_craft":
                enemies_to_spawn.append(ZigzagEnemy(enemy_missile_craft_img, 3, 1500, missile_img))
            elif enemy_type["type"] == "asteroid":
                enemies_to_spawn.append(SinusoidalEnemy(asteroid_img, 2, None))  # Tidak menembak

# Mulai level pertama
start_level(0)
spawn_timer = 0
spawn_interval = 2000  # milidetik

# Loop utama
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "playing":
                if event.key == pygame.K_SPACE:
                    player_ship.shoot()
            elif game_state == "game_over" or game_state == "victory":
                if event.key == pygame.K_r:
                    # Mulai ulang permainan
                    score = 0
                    lives = 3
                    current_level = 0
                    start_level(0)
                    game_state = "playing"
                    background_music.play(-1)  # Putar ulang musik latar
                elif event.key == pygame.K_q:
                    running = False

    if game_state == "playing":
        # Perbarui posisi kapal pemain
        player_ship.update()

        # Munculkan musuh
        current_time = pygame.time.get_ticks()
        if enemies_to_spawn and current_time - spawn_timer >= spawn_interval:
            enemy = enemies_to_spawn.pop(0)
            enemy.rect.x = widthScreen
            enemy.rect.y = random.randint(50, heightScreen - 50)
            enemies.add(enemy)
            all_sprites.add(enemy)
            spawn_timer = current_time

        # Perbarui semua sprite
        all_sprites.update()

        # Periksa tabrakan
        for bullet, enemies_hit in pygame.sprite.groupcollide(player_bullets, enemies, True, True).items():
            for enemy in enemies_hit:
                score += 10
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery, enemy_explode_img)
                all_sprites.add(explosion)
                explosion_sound.play()

        if pygame.sprite.spritecollide(player_ship, enemy_bullets, True):
            lives -= 1
            if lives <= 0:
                explosion = Explosion(player_ship.rect.centerx, player_ship.rect.centery, explode_img)
                all_sprites.add(explosion)
                explosion_sound.play()
                game_state = "game_over"
                background_music.stop()  # Hentikan musik latar
                shoot_sound.stop()
                enemy_shoot_sound.stop()
                explosion_sound.stop()
                defeat_sound.play()

        if pygame.sprite.spritecollide(player_ship, enemies, True):
            lives -= 1
            if lives <= 0:
                explosion = Explosion(player_ship.rect.centerx, player_ship.rect.centery, explode_img)
                all_sprites.add(explosion)
                explosion_sound.play()
                game_state = "game_over"
                background_music.stop()  # Hentikan musik latar
                shoot_sound.stop()
                enemy_shoot_sound.stop()
                explosion_sound.stop()
                defeat_sound.play()

        # Periksa apakah level selesai
        if not enemies_to_spawn and not enemies:
            if current_level < len(levels) - 1:
                current_level += 1
                start_level(current_level)
            else:
                game_state = "victory"
                background_music.stop()  # Hentikan musik latar
                shoot_sound.stop()
                enemy_shoot_sound.stop()
                explosion_sound.stop()
                victory_sound.play()

        # Ganti latar belakang secara perlahan
        background_change_timer += clock.get_time()
        if background_change_timer >= background_change_interval:
            current_background_index = (current_background_index + 1) % len(backgrounds)
            background_change_timer = 0

        # Gambar latar belakang
        background = backgrounds[current_background_index]
        screen.blit(background, (0, 0))

        # Gambar semua sprite
        all_sprites.draw(screen)

        # Gambar skor dan nyawa
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (widthScreen - 100, 10))

    elif game_state == "game_over":
        screen.fill((0, 0, 0))
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (widthScreen // 2 - 100, heightScreen // 2 - 50))
        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (widthScreen // 2 - 100, heightScreen // 2))
        restart_text = font.render("Press R to Restart, Q to Quit", True, (255, 255, 255))
        screen.blit(restart_text, (widthScreen // 2 - 150, heightScreen // 2 + 50))

    elif game_state == "victory":
        screen.fill((0, 0, 0))
        victory_text = font.render("Victory!", True, (0, 255, 0))
        screen.blit(victory_text, (widthScreen // 2 - 100, heightScreen // 2 - 50))
        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (widthScreen // 2 - 100, heightScreen // 2))
        restart_text = font.render("Press R to Restart, Q to Quit", True, (255, 255, 255))
        screen.blit(restart_text, (widthScreen // 2 - 150, heightScreen // 2 + 50))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()