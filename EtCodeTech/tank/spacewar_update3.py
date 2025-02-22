# spacewar_game.py
import pygame
import math
import random
from spacewar_ui import GameUI

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1000
BULLET_RADIUS = 5
GRAVITY_CONSTANT = 2000
SPACESHIP_SPEED = 200  # Increased from 50 for faster movement
AI_SPEED = 50
BULLET_SPEED = 300  # Increased for faster bullets
FPS = 60
AUTO_SHOOT_DELAY = 150  # Milliseconds between auto shots

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BRIGHT_YELLOW = (255, 255, 128)
RAINBOW_COLORS = [RED, GREEN, BLUE, (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spacewar!")

# Load assets
try:
    background_image = pygame.image.load("assets/space3.webp")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    spaceship1_image = pygame.image.load("assets/space-ship5.png")
    spaceship1_image = pygame.transform.scale(spaceship1_image, (40, 40))
    spaceship2_image = pygame.image.load("assets/space-ship1.png")
    spaceship2_image = pygame.transform.scale(spaceship2_image, (40, 40))
    spaceship3_image = pygame.image.load("assets/space-ship3.png")
    spaceship3_image = pygame.transform.scale(spaceship3_image, (40, 40))
    planet_image = pygame.image.load("assets/planet2.png")
    planet_image = pygame.transform.scale(planet_image, (60, 60))

    # Load sounds
    shoot_sound = pygame.mixer.Sound("assets/tank-shots.mp3")
    collision_sound = pygame.mixer.Sound("assets/tank-hits.mp3")
    movement_sound = pygame.mixer.Sound("assets/tank-engine.mp3")

    # Load background music
    pygame.mixer.music.load("assets/sky.mp3")
    pygame.mixer.music.set_volume(0.5)
except Exception as e:
    print(f"Error loading assets: {e}")
    exit()

clock = pygame.time.Clock()


class Spaceship:
    def __init__(self, x, y, image, controls, is_ai=False, target=None):
        self.x = x
        self.y = y
        self.angle = random.randint(0, 360) if is_ai else 0
        self.velocity_x = random.choice([-AI_SPEED, AI_SPEED]) if is_ai else 0
        self.velocity_y = random.choice([-AI_SPEED, AI_SPEED]) if is_ai else 0
        self.image = image
        self.controls = controls
        self.bullets = []
        self.is_ai = is_ai
        self.target = target
        self.health = 100
        self.score = 0
        self.shots_fired = 0
        self.has_moved = False
        self.respawn_timer = 0
        self.last_shot_time = 0
        self.active = True

    def aim_at_target(self):
        if self.target and self.active:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            self.angle = math.degrees(math.atan2(-dy, dx))

    def shoot(self):
        if not self.active:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= AUTO_SHOOT_DELAY:
            bullet_velocity_x = BULLET_SPEED * math.cos(math.radians(self.angle))
            bullet_velocity_y = -BULLET_SPEED * math.sin(math.radians(self.angle))
            self.bullets.append(Bullet(self.x, self.y, bullet_velocity_x, bullet_velocity_y, self))
            self.shots_fired += 1
            self.last_shot_time = current_time
            pygame.mixer.Sound.play(shoot_sound)

    def move(self):
        if not self.active:
            return

        if self.is_ai:
            self.ai_move()
        else:
            keys = pygame.key.get_pressed()
            self.velocity_x = 0
            self.velocity_y = 0

            if keys[self.controls['left']]:
                self.velocity_x = -SPACESHIP_SPEED
                self.has_moved = True
            if keys[self.controls['right']]:
                self.velocity_x = SPACESHIP_SPEED
                self.has_moved = True
            if keys[self.controls['up']]:
                self.velocity_y = -SPACESHIP_SPEED
                self.has_moved = True
            if keys[self.controls['down']]:
                self.velocity_y = SPACESHIP_SPEED
                self.has_moved = True

            # Auto-shoot for player
            self.shoot()

        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS

        # Update angle based on movement direction for player
        if not self.is_ai and (self.velocity_x != 0 or self.velocity_y != 0):
            self.angle = math.degrees(math.atan2(-self.velocity_y, self.velocity_x))

        # Keep within screen bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH))
        self.y = max(0, min(self.y, SCREEN_HEIGHT))

    def ai_move(self):
        self.aim_at_target()
        self.shoot()

        # Move towards target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 200:  # Keep some distance from target
            self.velocity_x = (dx / distance) * AI_SPEED
            self.velocity_y = (dy / distance) * AI_SPEED

    def draw(self):
        if not self.active:
            return

        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)

        # Health bar
        pygame.draw.rect(screen, RED, (self.x - 20, self.y - 30, 40, 5))
        pygame.draw.rect(screen, GREEN, (self.x - 20, self.y - 30, 40 * (self.health / 100), 5))


class Bullet:
    def __init__(self, x, y, velocity_x, velocity_y, owner):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.owner = owner
        self.color_index = 0
        self.glow_size = 0
        self.growing = True

    def draw(self):
        if self.owner.is_ai:
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), BULLET_RADIUS)
        else:
            self.color_index = (self.color_index + 1) % len(RAINBOW_COLORS)
            pygame.draw.circle(screen, RAINBOW_COLORS[self.color_index],
                               (int(self.x), int(self.y)), BULLET_RADIUS)

    def move(self):
        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS
        return 0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT


def main():
    game_ui = GameUI(screen, clock)

    # Initialize spaceships
    player = Spaceship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, spaceship2_image, {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'up': pygame.K_UP,
        'down': pygame.K_DOWN
    })

    enemy1 = Spaceship(100, 100, spaceship1_image, {}, is_ai=True, target=player)
    enemy2 = Spaceship(SCREEN_WIDTH - 100, 100, spaceship3_image, {}, is_ai=True, target=player)

    game_running = True
    game_active = True
    start_time = None
    music_playing = False

    while game_running:
        if game_active:
            screen.blit(background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

            # Start music when player moves
            if player.has_moved and not music_playing:
                pygame.mixer.music.play(-1)  # -1 for infinite loop
                music_playing = True
                start_time = pygame.time.get_ticks()

            # Move and update all ships
            player.move()
            enemy1.move()
            enemy2.move()

            # Process bullets and collisions
            for ship in [player, enemy1, enemy2]:
                for bullet in ship.bullets[:]:
                    if not bullet.move():
                        ship.bullets.remove(bullet)
                        continue

                    for target in [player, enemy1, enemy2]:
                        if target != ship and target.active:
                            if math.hypot(bullet.x - target.x, bullet.y - target.y) < 20:
                                if target.is_ai:
                                    target.active = False
                                    ship.score += 10
                                else:
                                    target.health -= 1
                                ship.bullets.remove(bullet)
                                pygame.mixer.Sound.play(collision_sound)
                                break

            # Check win/lose conditions
            if player.health <= 0:
                game_active = False
                stop_all_sounds()
                end_time = pygame.time.get_ticks()
                game_ui.show_game_over(player, start_time, end_time)
                pygame.time.wait(3000)
                break

            if not enemy1.active and not enemy2.active:
                player.score = 100  # Victory score
                game_active = False
                stop_all_sounds()
                end_time = pygame.time.get_ticks()
                game_ui.show_game_over(player, start_time, end_time)
                pygame.time.wait(3000)
                break

            # Draw everything
            for ship in [player, enemy1, enemy2]:
                ship.draw()
                for bullet in ship.bullets:
                    bullet.draw()

            if start_time is not None:
                current_time = pygame.time.get_ticks()
                game_ui.draw_game_stats(player, start_time, current_time)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def stop_all_sounds():
    pygame.mixer.music.stop()
    shoot_sound.stop()
    collision_sound.stop()
    movement_sound.stop()


if __name__ == "__main__":
    main()