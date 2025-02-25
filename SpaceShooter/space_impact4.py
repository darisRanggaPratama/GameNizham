import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH_SCREEN = 1600
HEIGHT_SCREEN = 1000
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("Space Impact")

# Set FPS
FPS = 60
clock = pygame.time.Clock()

# Load assets
# Backgrounds
backgrounds = []
for i in range(6):
    try:
        bg = pygame.image.load(f"background{i}.jpg")
        backgrounds.append(pygame.transform.scale(bg, (WIDTH_SCREEN, HEIGHT_SCREEN)))
    except:
        # Fallback to creating a background if images not found
        bg = pygame.Surface((WIDTH_SCREEN, HEIGHT_SCREEN))
        bg.fill((0, 0, 0))
        for _ in range(50):
            x = random.randint(0, WIDTH_SCREEN)
            y = random.randint(0, HEIGHT_SCREEN)
            radius = random.randint(1, 3)
            pygame.draw.circle(bg, (255, 255, 255), (x, y), radius)
        backgrounds.append(bg)

# Try to load font, use default if not found
try:
    font = pygame.font.Font("SHPinscher-Regular.otf", 35)
except:
    font = pygame.font.SysFont('Arial', 35)


# Try to load images, create placeholders if not found
def load_image(name, size=(50, 50), color=(255, 255, 255)):
    try:
        img = pygame.image.load(name)
        return pygame.transform.scale(img, size)
    except:
        # Create a placeholder
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, size[0], size[1]))
        return surf


# Load game images
player_ship = load_image("space_ship.png", (60, 40), (0, 255, 0))
enemy_spaceship = load_image("enemy-spaceship.png", (60, 40), (255, 0, 0))
enemy_missile_craft = load_image("enemy-ship.png", (55, 35), (255, 100, 0))
player_bullet = load_image("torpedo-left.png", (20, 10), (0, 255, 255))
enemy_bullet = load_image("missile-right.png", (20, 10), (255, 255, 0))
missile = load_image("missile-xright.png", (25, 15), (255, 0, 255))
player_explosion = load_image("boom1.png", (60, 60), (255, 255, 0))
enemy_explosion = load_image("boom2.png", (60, 60), (255, 100, 0))
asteroid_img = load_image("asteroid.png", (40, 40), (150, 150, 150))


# Try to load sounds, use empty sounds if not found
def load_sound(name):
    try:
        return pygame.mixer.Sound(name)
    except:
        return pygame.mixer.Sound(None)  # Empty sound


# Load sound effects
shoot_sound = load_sound("tank-shots.mp3")
enemy_shoot_sound = load_sound("tank-hits.mp3")
explosion_sound = load_sound("tank-explode.mp3")
background_music = load_sound("background1.mp3")
victory_sound = load_sound("victory.mp3")
defeat_sound = load_sound("defeat.mp3")


# Function to stop all sounds
def stop_all_sounds():
    shoot_sound.stop()
    enemy_shoot_sound.stop()
    explosion_sound.stop()
    background_music.stop()
    victory_sound.stop()
    defeat_sound.stop()


# Game classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_ship
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT_SCREEN // 2
        self.speed = 5
        self.last_shot = 0
        self.shot_delay = 500  # 0.5 seconds between shots
        self.lives = 10
        self.auto_shoot = True  # Enable auto-shooting by default

    def update(self):
        # Get mouse position and move player toward it
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate direction vector
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery

        # Normalize the vector (if not zero)
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            dx /= distance
            dy /= distance

        # Move player
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Keep player on screen
        self.rect.x = max(0, min(self.rect.x, WIDTH_SCREEN - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT_SCREEN - self.rect.height))

        # Auto-shooting mechanism
        if self.auto_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot > self.shot_delay:
                self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shot_delay:
            self.last_shot = current_time
            bullet = PlayerBullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            player_bullets.add(bullet)
            shoot_sound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type

        if enemy_type == "spaceship":
            self.image = enemy_spaceship
            self.speed = random.randint(2, 4)
            self.health = 2
            self.points = 10
            self.shoot_chance = 0.01
        elif enemy_type == "missile_craft":
            self.image = enemy_missile_craft
            self.speed = random.randint(3, 5)
            self.health = 1
            self.points = 15
            self.shoot_chance = 0.02
        elif enemy_type == "asteroid":
            self.image = asteroid_img
            self.speed = random.randint(1, 3)
            self.health = 3
            self.points = 5
            self.shoot_chance = 0

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH_SCREEN
        self.rect.y = random.randint(50, HEIGHT_SCREEN - 100)

        # For movement patterns
        self.pattern = random.choice(["straight", "zigzag", "sine"])
        self.angle = 0
        self.amplitude = random.randint(20, 80) if self.pattern != "straight" else 0
        self.frequency = random.uniform(0.05, 0.1)
        self.initial_y = self.rect.y

    def update(self):
        # Move based on pattern
        self.rect.x -= self.speed

        if self.pattern == "zigzag":
            if int(self.angle / 180) % 2 == 0:
                self.rect.y += 2
            else:
                self.rect.y -= 2
            self.angle = (self.angle + 5) % 360
        elif self.pattern == "sine":
            self.rect.y = self.initial_y + int(self.amplitude * math.sin(self.frequency * self.rect.x))

        # Remove if off-screen
        if self.rect.right < 0:
            self.kill()

        # Randomly shoot if not an asteroid
        if self.enemy_type != "asteroid" and random.random() < self.shoot_chance:
            self.shoot()

    def shoot(self):
        if self.enemy_type == "spaceship":
            bullet = EnemyBullet(self.rect.left, self.rect.centery)
        else:  # missile_craft uses missiles
            bullet = HomingMissile(self.rect.left, self.rect.centery)

        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
        enemy_shoot_sound.play()


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH_SCREEN:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


class HomingMissile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = missile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        # Basic homing behavior towards player
        if player.sprite:
            target_x = player.sprite.rect.centerx
            target_y = player.sprite.rect.centery

            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery

            # Normalize
            distance = max(1, math.sqrt(dx ** 2 + dy ** 2))
            dx = dx / distance
            dy = dy / distance

            # Move towards player, but primarily leftward
            self.rect.x -= self.speed * 0.8
            self.rect.x += dx * self.speed * 0.2
            self.rect.y += dy * self.speed * 0.5
        else:
            # If player doesn't exist, just move left
            self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, is_player=False):
        super().__init__()
        self.image = player_explosion if is_player else enemy_explosion
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # how fast the animation plays

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.frame += 1
            if self.frame > 8:  # Assume 8 frames of animation
                self.kill()
            else:
                self.last_update = now


# Create sprite groups
all_sprites = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Create player
player_ship_sprite = Player()
player.add(player_ship_sprite)
all_sprites.add(player_ship_sprite)

# Game variables
score = 0
level = 1
enemy_spawn_timer = 0
enemy_spawn_delay = 2000  # 2 seconds
bg_scroll = 0
bg_speed = 2
game_state = "playing"  # "playing", "game_over", "victory"
victory_enemies = 50  # Enemies to defeat to win


# Draw text function
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


# Game over screen
def show_game_over_screen():
    # Stop all sounds first
    stop_all_sounds()

    # Then play defeat sound
    defeat_sound.play()

    screen.fill((0, 0, 0))
    draw_text("GAME OVER", font, (255, 0, 0), WIDTH_SCREEN // 2 - 120, HEIGHT_SCREEN // 2 - 50)
    draw_text(f"Your score: {score}", font, (255, 255, 255), WIDTH_SCREEN // 2 - 120, HEIGHT_SCREEN // 2 + 10)
    draw_text("Press SPACE to restart", font, (255, 255, 255), WIDTH_SCREEN // 2 - 160, HEIGHT_SCREEN // 2 + 70)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


# Victory screen
def show_victory_screen():
    # Stop all sounds first
    stop_all_sounds()

    # Then play victory sound
    victory_sound.play()

    screen.fill((0, 0, 50))
    draw_text("VICTORY!", font, (0, 255, 0), WIDTH_SCREEN // 2 - 100, HEIGHT_SCREEN // 2 - 50)
    draw_text(f"Your score: {score}", font, (255, 255, 255), WIDTH_SCREEN // 2 - 120, HEIGHT_SCREEN // 2 + 10)
    draw_text("Press SPACE to play again", font, (255, 255, 255), WIDTH_SCREEN // 2 - 160, HEIGHT_SCREEN // 2 + 70)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


# Reset game function
def reset_game():
    global score, level, enemy_spawn_timer, game_state, enemies_defeated
    # Clear all sprites
    all_sprites.empty()
    player.empty()
    enemies.empty()
    player_bullets.empty()
    enemy_bullets.empty()
    explosions.empty()

    # Reset variables
    score = 0
    level = 1
    enemy_spawn_timer = 0
    game_state = "playing"
    enemies_defeated = 0

    # Create new player
    player_ship_sprite = Player()
    player.add(player_ship_sprite)
    all_sprites.add(player_ship_sprite)

    # Restart background music
    try:
        background_music.play(-1)  # Loop indefinitely
    except:
        pass


# Main game loop
enemies_defeated = 0

# Try to play background music
try:
    background_music.play(-1)  # Loop indefinitely
except:
    pass

running = True
while running:
    # Keep game running at the right speed
    clock.tick(FPS)

    # Process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "playing" and event.button == 1:  # Left mouse button
                if player.sprite:
                    # Manual shooting is still possible but not necessary
                    player.sprite.shoot()
        elif event.type == pygame.KEYDOWN:
            if game_state == "playing" and event.key == pygame.K_t:
                # Toggle auto-shooting on/off with 'T' key
                if player.sprite:
                    player.sprite.auto_shoot = not player.sprite.auto_shoot

    # Check if game is active
    if game_state == "playing":
        # Update
        all_sprites.update()

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time - enemy_spawn_timer > enemy_spawn_delay:
            enemy_spawn_timer = current_time

            # Adjust spawn rate based on level
            enemy_spawn_delay = max(500, 2000 - (level * 100))

            # Always choose randomly between the three enemy types regardless of level
            enemy_type = random.choice(["spaceship", "missile_craft", "asteroid"])

            new_enemy = Enemy(enemy_type)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Check for bullet collisions with enemies
        hits = pygame.sprite.groupcollide(enemies, player_bullets, False, True)
        for enemy, bullets in hits.items():
            enemy.health -= len(bullets)
            if enemy.health <= 0:
                score += enemy.points
                enemies_defeated += 1
                explosion_sound.play()
                explosion = Explosion(enemy.rect.center[0], enemy.rect.center[1])
                explosions.add(explosion)
                all_sprites.add(explosion)
                enemy.kill()

                # Level up every 10 enemies defeated
                if enemies_defeated % 10 == 0:
                    level = min(5, level + 1)

        # Check for collisions with player
        if player.sprite:
            # Player hit by enemy bullets
            hits = pygame.sprite.spritecollide(player.sprite, enemy_bullets, True)
            if hits:
                player.sprite.lives -= 1
                explosion_sound.play()
                explosion = Explosion(player.sprite.rect.center[0], player.sprite.rect.center[1], True)
                explosions.add(explosion)
                all_sprites.add(explosion)

                if player.sprite.lives <= 0:
                    player.sprite.kill()
                    game_state = "game_over"

            # Player collides with enemies
            hits = pygame.sprite.spritecollide(player.sprite, enemies, True)
            if hits:
                player.sprite.lives -= 1
                explosion_sound.play()
                explosion = Explosion(player.sprite.rect.center[0], player.sprite.rect.center[1], True)
                explosions.add(explosion)
                all_sprites.add(explosion)

                if player.sprite.lives <= 0:
                    player.sprite.kill()
                    game_state = "game_over"

        # Check for victory
        if enemies_defeated >= victory_enemies:
            game_state = "victory"

    # Render
    # Scroll background
    bg_index = (level - 1) % len(backgrounds)

    # Create a scrolling effect
    rel_x = bg_scroll % WIDTH_SCREEN
    screen.blit(backgrounds[bg_index], (rel_x - WIDTH_SCREEN, 0))
    if rel_x < WIDTH_SCREEN:
        screen.blit(backgrounds[bg_index], (rel_x, 0))
    bg_scroll += bg_speed

    # Draw all sprites
    all_sprites.draw(screen)

    # Draw score and lives
    if game_state == "playing":
        draw_text(f"Score: {score}", font, (255, 255, 255), 10, 10)
        draw_text(f"Level: {level}", font, (255, 255, 255), WIDTH_SCREEN // 2 - 50, 10)
        if player.sprite:
            draw_text(f"Lives: {player.sprite.lives}", font, (255, 255, 255), WIDTH_SCREEN - 150, 10)
            # Display auto-shoot status
            auto_status = "ON" if player.sprite.auto_shoot else "OFF"
            draw_text(f"Auto-shoot: {auto_status} (T)", font, (255, 255, 255), WIDTH_SCREEN - 280, 50)

    # Game over or victory
    if game_state == "game_over":
        show_game_over_screen()
        reset_game()
    elif game_state == "victory":
        show_victory_screen()
        reset_game()

    # Flip display
    pygame.display.flip()

# Quit game
stop_all_sounds()  # Stop all sounds before quitting the game
pygame.quit()
sys.exit()
