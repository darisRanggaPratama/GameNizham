# spacewar_game.py
import pygame
import math
import random
from spacewar_ui import GameUI

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1000
BULLET_RADIUS = 5
GRAVITY_CONSTANT = 2000
SPACESHIP_SPEED = 50
AI_SPEED = 50
BULLET_SPEED = 200
FPS = 60

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
    shoot_sound = pygame.mixer.Sound("assets/tank-shots.mp3")
    collision_sound = pygame.mixer.Sound("assets/tank-hits.mp3")
    movement_sound = pygame.mixer.Sound("assets/tank-engine.mp3")
except Exception as e:
    print(f"Error loading assets: {e}")
    exit()

# Clock for controlling frame rate
clock = pygame.time.Clock()


class Spaceship:
    def __init__(self, x, y, image, controls, is_ai=False):
        self.x = x
        self.y = y
        self.angle = random.randint(0, 360) if is_ai else 0
        self.velocity_x = random.choice([-AI_SPEED, AI_SPEED]) if is_ai else 0
        self.velocity_y = random.choice([-AI_SPEED, AI_SPEED]) if is_ai else 0
        self.image = image
        self.controls = controls
        self.bullets = []
        self.is_ai = is_ai
        self.ai_timer = 0
        self.health = 100
        self.score = 0
        self.shots_fired = 0
        self.has_moved = False
        self.respawn_timer = 0

    def respawn(self):
        """Respawn the spaceship at a random position near the center"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        random_offset = 200  # Random offset from center

        self.x = random.randint(center_x - random_offset, center_x + random_offset)
        self.y = random.randint(center_y - random_offset, center_y + random_offset)
        self.velocity_x = random.choice([-AI_SPEED, AI_SPEED])
        self.velocity_y = random.choice([-AI_SPEED, AI_SPEED])
        self.angle = random.randint(0, 360)
        self.respawn_timer = 60  # 1 second at 60 FPS

    def reset(self):
        self.health = 100
        self.score = 0
        self.shots_fired = 0
        self.has_moved = False
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        self.bullets.clear()

    def draw(self):
        if self.respawn_timer > 0:
            return  # Don't draw during respawn

        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)
        pygame.draw.rect(screen, RED, (self.x - 20, self.y - 30, 40, 5))
        pygame.draw.rect(screen, GREEN, (self.x - 20, self.y - 30, 40 * (self.health / 100), 5))

    def move(self):
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            return

        if self.is_ai:
            self.ai_move()
        else:
            keys = pygame.key.get_pressed()
            self.velocity_x = 0
            self.velocity_y = 0

            if keys[self.controls['left']]:
                self.angle = 180
                self.velocity_x = -SPACESHIP_SPEED
                self.has_moved = True
            if keys[self.controls['right']]:
                self.angle = 0
                self.velocity_x = SPACESHIP_SPEED
                self.has_moved = True
            if keys[self.controls['up']]:
                self.angle = 90
                self.velocity_y = -SPACESHIP_SPEED
                self.has_moved = True
            if keys[self.controls['down']]:
                self.angle = 270
                self.velocity_y = SPACESHIP_SPEED
                self.has_moved = True

        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS

        # Check for window boundaries
        if (self.x <= 0 or self.x >= SCREEN_WIDTH or
                self.y <= 0 or self.y >= SCREEN_HEIGHT):
            if self.is_ai:
                self.respawn()

    def ai_move(self):
        if self.ai_timer <= 0:
            self.angle += random.choice([-5, 5])
            self.velocity_x = AI_SPEED * math.cos(math.radians(self.angle))
            self.velocity_y = AI_SPEED * math.sin(math.radians(self.angle))
            self.shoot()
            self.ai_timer = random.randint(30, 70)
        else:
            self.ai_timer -= 1

        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS

        if (self.x <= 0 or self.x >= SCREEN_WIDTH or
                self.y <= 0 or self.y >= SCREEN_HEIGHT):
            self.respawn()

    def shoot(self):
        bullet_velocity_x = BULLET_SPEED * math.cos(math.radians(self.angle))
        bullet_velocity_y = -BULLET_SPEED * math.sin(math.radians(self.angle))
        self.bullets.append(Bullet(self.x, self.y, bullet_velocity_x, bullet_velocity_y, self))
        self.shots_fired += 1
        pygame.mixer.Sound.play(shoot_sound)


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
        if self.owner == spaceship2:
            if self.growing:
                self.glow_size += 0.2
                if self.glow_size >= 3:
                    self.growing = False
            else:
                self.glow_size -= 0.2
                if self.glow_size <= 0:
                    self.growing = True

            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)),
                               BULLET_RADIUS + self.glow_size + 4, 2)
            pygame.draw.circle(screen, BRIGHT_YELLOW, (int(self.x), int(self.y)),
                               BULLET_RADIUS + self.glow_size + 2)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), BULLET_RADIUS)
        else:
            self.color_index = (self.color_index + 1) % len(RAINBOW_COLORS)
            pygame.draw.circle(screen, RAINBOW_COLORS[self.color_index],
                               (int(self.x), int(self.y)), BULLET_RADIUS)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)),
                               BULLET_RADIUS + 2, 1)

    def move(self):
        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS

        if (self.x < -SCREEN_WIDTH or self.x > SCREEN_WIDTH * 2 or
                self.y < -SCREEN_HEIGHT or self.y > SCREEN_HEIGHT * 2):
            return False
        return True


class Planet:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.angle = 0

    def draw(self):
        self.angle = (self.angle + 1) % 360
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)

    def apply_gravity(self, spaceship):
        dx = self.x - spaceship.x
        dy = self.y - spaceship.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 30:
            force = GRAVITY_CONSTANT / (distance ** 2)
            angle = math.atan2(dy, dx)
            spaceship.velocity_x += force * math.cos(angle) / FPS
            spaceship.velocity_y += force * math.sin(angle) / FPS


def stop_all_sounds():
    shoot_sound.stop()
    collision_sound.stop()
    movement_sound.stop()


# Initialize game objects
planet = Planet(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, planet_image)
spaceship1 = Spaceship(100, 100, spaceship1_image, {}, is_ai=True)
spaceship3 = Spaceship(600, 100, spaceship3_image, {}, is_ai=True)
spaceship2 = Spaceship(700, 500, spaceship2_image, {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'shoot': pygame.K_SPACE
})


def reset_game():
    spaceship1.reset()
    spaceship2.reset()
    spaceship3.reset()


def main():
    game_ui = GameUI(screen, clock)
    game_running = True
    game_active = True
    start_time = None

    while game_running:
        if game_active:
            screen.blit(background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == spaceship2.controls['shoot']:
                        spaceship2.shoot()

            if spaceship2.has_moved and start_time is None:
                start_time = pygame.time.get_ticks()

            planet.apply_gravity(spaceship1)
            planet.apply_gravity(spaceship2)
            planet.apply_gravity(spaceship3)

            spaceship1.move()
            spaceship2.move()
            spaceship3.move()

            for spaceship in [spaceship1, spaceship3, spaceship2]:
                for bullet in spaceship.bullets[:]:
                    if not bullet.move():
                        spaceship.bullets.remove(bullet)
                    else:
                        for target in [spaceship1, spaceship2, spaceship3]:
                            if (math.hypot(bullet.x - target.x, bullet.y - target.y) < 20
                                    and target != spaceship):
                                if target.is_ai:
                                    target.respawn()
                                else:
                                    target.health -= 1
                                spaceship.score += 1
                                spaceship.bullets.remove(bullet)
                                pygame.mixer.Sound.play(collision_sound)
                                break

            if spaceship2.health <= 0 or spaceship2.score >= 100:
                game_active = False
                stop_all_sounds()
                end_time = pygame.time.get_ticks()
                game_ui.show_game_over(spaceship2, start_time, end_time)
                pygame.time.wait(3000)
                reset_game()
                start_time = None
                game_active = True

            planet.draw()
            spaceship1.draw()
            spaceship2.draw()
            spaceship3.draw()

            for spaceship in [spaceship1, spaceship2, spaceship3]:
                for bullet in spaceship.bullets:
                    bullet.draw()

            if start_time is not None:
                current_time = pygame.time.get_ticks()
                game_ui.draw_game_stats(spaceship2, start_time, current_time)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
