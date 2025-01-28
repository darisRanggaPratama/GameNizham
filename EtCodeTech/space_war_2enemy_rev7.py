import pygame
import math
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1000
BULLET_RADIUS = 5
GRAVITY_CONSTANT = 2000
SPACESHIP_SPEED = 50  # Normal speed
AI_SPEED = 50  # Reduced speed for AI ships
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
    background_image = pygame.image.load("tank/assets/space3.webp")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    spaceship1_image = pygame.image.load("tank/assets/space-ship5.png")
    spaceship1_image = pygame.transform.scale(spaceship1_image, (40, 40))
    spaceship2_image = pygame.image.load("tank/assets/space-ship1.png")
    spaceship2_image = pygame.transform.scale(spaceship2_image, (40, 40))
    spaceship3_image = pygame.image.load("tank/assets/space-ship3.png")
    spaceship3_image = pygame.transform.scale(spaceship3_image, (40, 40))
    planet_image = pygame.image.load("tank/assets/planet2.png")
    planet_image = pygame.transform.scale(planet_image, (60, 60))
    shoot_sound = pygame.mixer.Sound("tank/assets/tank-shots.mp3")
    collision_sound = pygame.mixer.Sound("tank/assets/tank-hits.mp3")
    movement_sound = pygame.mixer.Sound("tank/assets/tank-engine.mp3")
except Exception as e:
    print(f"Error loading assets: {e}")
    exit()

# Clock for controlling frame rate
clock = pygame.time.Clock()


# Spaceship class
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

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)
        # Draw health bar
        pygame.draw.rect(screen, RED, (self.x - 20, self.y - 30, 40, 5))
        pygame.draw.rect(screen, GREEN, (self.x - 20, self.y - 30, 40 * (self.health / 100), 5))

    def move(self):
        if self.is_ai:
            self.ai_move()
        else:
            keys = pygame.key.get_pressed()
            self.velocity_x = 0
            self.velocity_y = 0

            if keys[self.controls['left']]:
                self.angle = 180
                self.velocity_x = -SPACESHIP_SPEED
            if keys[self.controls['right']]:
                self.angle = 0
                self.velocity_x = SPACESHIP_SPEED
            if keys[self.controls['up']]:
                self.angle = 90
                self.velocity_y = -SPACESHIP_SPEED
            if keys[self.controls['down']]:
                self.angle = 270
                self.velocity_y = SPACESHIP_SPEED

        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS

        # Bounce off screen edges and return to center
        if self.x <= 0:
            self.velocity_x *= -1
            self.x = SCREEN_WIDTH // 2
        elif self.x >= SCREEN_WIDTH:
            self.velocity_x *= -1
            self.x = SCREEN_WIDTH // 2

        if self.y <= 0:
            self.velocity_y *= -1
            self.y = SCREEN_HEIGHT // 2
        elif self.y >= SCREEN_HEIGHT:
            self.velocity_y *= -1
            self.y = SCREEN_HEIGHT // 2

    def ai_move(self):
        if self.ai_timer <= 0:
            # Random movement with slower speed
            self.angle += random.choice([-5, 5])  # Smaller angle changes
            self.velocity_x = AI_SPEED * math.cos(math.radians(self.angle))
            self.velocity_y = AI_SPEED * math.sin(math.radians(self.angle))
            self.shoot()
            self.ai_timer = random.randint(30, 70)  # Longer delays between actions
        else:
            self.ai_timer -= 1

        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS

        # Bounce off screen edges and return to center
        if self.x <= 0:
            self.velocity_x *= -1
            self.x = SCREEN_WIDTH // 2
        elif self.x >= SCREEN_WIDTH:
            self.velocity_x *= -1
            self.x = SCREEN_WIDTH // 2

        if self.y <= 0:
            self.velocity_y *= -1
            self.y = SCREEN_HEIGHT // 2
        elif self.y >= SCREEN_HEIGHT:
            self.velocity_y *= -1
            self.y = SCREEN_HEIGHT // 2

    def shoot(self):
        bullet_velocity_x = BULLET_SPEED * math.cos(math.radians(self.angle))
        bullet_velocity_y = -BULLET_SPEED * math.sin(math.radians(self.angle))
        self.bullets.append(Bullet(self.x, self.y, bullet_velocity_x, bullet_velocity_y, self))
        self.shots_fired += 1
        pygame.mixer.Sound.play(shoot_sound)


# Modified Bullet class to remove screen boundary constraints
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
        if self.owner == spaceship2:  # Enhanced bullets for player
            # Pulsating glow effect
            if self.growing:
                self.glow_size += 0.2
                if self.glow_size >= 3:
                    self.growing = False
            else:
                self.glow_size -= 0.2
                if self.glow_size <= 0:
                    self.growing = True

            # Draw multiple layers for glow effect
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)),
                               BULLET_RADIUS + self.glow_size + 4, 2)
            pygame.draw.circle(screen, BRIGHT_YELLOW, (int(self.x), int(self.y)),
                               BULLET_RADIUS + self.glow_size + 2)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), BULLET_RADIUS)
        else:
            # Regular bullets for AI ships
            self.color_index = (self.color_index + 1) % len(RAINBOW_COLORS)
            pygame.draw.circle(screen, RAINBOW_COLORS[self.color_index],
                               (int(self.x), int(self.y)), BULLET_RADIUS)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)),
                               BULLET_RADIUS + 2, 1)

    def move(self):
        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS

        # Remove bullets that are far outside the screen to prevent memory issues
        if (self.x < -SCREEN_WIDTH or self.x > SCREEN_WIDTH * 2 or
            self.y < -SCREEN_HEIGHT or self.y > SCREEN_HEIGHT * 2):
            return False
        return True


# Planet class remains the same
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

        if distance > 30:  # Minimum distance to apply gravity
            force = GRAVITY_CONSTANT / (distance ** 2)
            angle = math.atan2(dy, dx)
            spaceship.velocity_x += force * math.cos(angle) / FPS
            spaceship.velocity_y += force * math.sin(angle) / FPS


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


def main():
    game_running = True
    while game_running:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == spaceship2.controls['shoot']:
                    spaceship2.shoot()

        # Apply gravity
        planet.apply_gravity(spaceship1)
        planet.apply_gravity(spaceship2)
        planet.apply_gravity(spaceship3)

        # Move spaceships
        spaceship1.move()
        spaceship2.move()
        spaceship3.move()

        # Move bullets and check collisions
        for spaceship in [spaceship1, spaceship3, spaceship2]:
            for bullet in spaceship.bullets[:]:
                if not bullet.move():
                    spaceship.bullets.remove(bullet)
                else:
                    # Check collision
                    for target in [spaceship1, spaceship2, spaceship3]:
                        if math.hypot(bullet.x - target.x, bullet.y - target.y) < 20 and target != spaceship:
                            target.health -= 1
                            spaceship.score += 1
                            spaceship.bullets.remove(bullet)
                            pygame.mixer.Sound.play(collision_sound)
                            break

        # End game conditions
        if spaceship2.health <= 0 or spaceship2.score >= 100:
            game_running = False

        # Draw everything
        planet.draw()
        spaceship1.draw()
        spaceship2.draw()
        spaceship3.draw()

        for spaceship in [spaceship1, spaceship2, spaceship3]:
            for bullet in spaceship.bullets:
                bullet.draw()

        # Display scores and health
        font = pygame.font.SysFont(None, 36)
        health_text = font.render(f"Health: {spaceship2.health}", True, RED)
        score_text = font.render(f"Score: {spaceship2.score}", True, WHITE)
        shots_text = font.render(f"Shots Fired: {spaceship2.shots_fired}", True, BLUE)
        screen.blit(health_text, (20, 20))
        screen.blit(score_text, (20, 60))
        screen.blit(shots_text, (20, 100))

        # Update display and control frame rate
        pygame.display.flip()
        clock.tick(FPS)

    # Game Over screen
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 72)
    if spaceship2.health <= 0:
        game_over_text = font.render("Game Over! You Lost!", True, RED)
    elif spaceship2.score >= 100:
        game_over_text = font.render("Congratulations! You Won!", True, GREEN)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()


if __name__ == "__main__":
    main()