import pygame
import math
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BULLET_RADIUS = 5
GRAVITY_CONSTANT = 2000
SPACESHIP_SPEED = 5
BULLET_SPEED = 10
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spacewar!")

# Load assets
try:
    background_image = pygame.image.load("tank/assets/space3.webp")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    spaceship1_image = pygame.image.load("tank/assets/space-ship1.png")
    spaceship1_image = pygame.transform.scale(spaceship1_image, (40, 40))
    spaceship2_image = pygame.image.load("tank/assets/space-ship2.png")
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
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.image = image
        self.controls = controls
        self.bullets = []
        self.is_ai = is_ai
        self.ai_timer = 0
        self.health = 100

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)

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

            if keys[self.controls['up']] and keys[self.controls['right']]:
                self.angle = 45
                self.velocity_x = SPACESHIP_SPEED / 1.4
                self.velocity_y = -SPACESHIP_SPEED / 1.4

            if keys[self.controls['up']] and keys[self.controls['left']]:
                self.angle = 135
                self.velocity_x = -SPACESHIP_SPEED / 1.4
                self.velocity_y = -SPACESHIP_SPEED / 1.4

        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS

        # Wrap around screen
        self.x %= SCREEN_WIDTH
        self.y %= SCREEN_HEIGHT

    def ai_move(self):
        if self.ai_timer <= 0:
            self.angle += random.choice([-5, 0, 5])
            if random.random() < 0.3:  # Randomly decide to shoot
                self.shoot()
            self.ai_timer = random.randint(10, 50)  # Random delay between actions
        else:
            self.ai_timer -= 1

        self.velocity_x += SPACESHIP_SPEED * math.cos(math.radians(self.angle)) / FPS
        self.velocity_y -= SPACESHIP_SPEED * math.sin(math.radians(self.angle)) / FPS

    def shoot(self):
        bullet_velocity_x = BULLET_SPEED * math.cos(math.radians(self.angle))
        bullet_velocity_y = -BULLET_SPEED * math.sin(math.radians(self.angle))
        self.bullets.append(Bullet(self.x, self.y, bullet_velocity_x, bullet_velocity_y))
        pygame.mixer.Sound.play(shoot_sound)

# Bullet class
class Bullet:
    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), BULLET_RADIUS)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Remove bullet if out of bounds
        return 0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT

# Planet class
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

# Scores
score2 = 0

# Main game loop
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

    # Draw everything
    planet.draw()
    spaceship1.draw()
    spaceship2.draw()
    spaceship3.draw()

    for spaceship in [spaceship1, spaceship2, spaceship3]:
        for bullet in spaceship.bullets:
            bullet.draw()

    # Display score and health
    font = pygame.font.SysFont(None, 36)
    health_text = font.render(f"Health: {spaceship2.health}", True, RED)
    score_text = font.render(f"Score: {score2}", True, WHITE)
    screen.blit(health_text, (20, 20))
    screen.blit(score_text, (20, 60))

    # Update display and control frame rate
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
