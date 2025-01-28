import pygame
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLANET_RADIUS = 30
BULLET_RADIUS = 5
GRAVITY_CONSTANT = 2000
SPACESHIP_SPEED = 5
BULLET_SPEED = 10
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spacewar!")

# Load assets
background_image = pygame.image.load("tank/assets/space2.webp")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

spaceship1_image = pygame.image.load("tank/assets/space-ship1.png")
spaceship1_image = pygame.transform.scale(spaceship1_image, (40, 40))

spaceship2_image = pygame.image.load("tank/assets/space-ship2.png")
spaceship2_image = pygame.transform.scale(spaceship2_image, (40, 40))

shoot_sound = pygame.mixer.Sound("tank/assets/tank-shots.mp3")
collision_sound = pygame.mixer.Sound("tank/assets/tank-explode.mp3")
movement_sound = pygame.mixer.Sound("tank/assets/tank-move.mp3")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Spaceship class
class Spaceship:
    def __init__(self, x, y, image, controls):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.image = image
        self.controls = controls
        self.bullets = []

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[self.controls['left']]:
            self.angle += 5
            pygame.mixer.Sound.play(movement_sound)
        if keys[self.controls['right']]:
            self.angle -= 5
            pygame.mixer.Sound.play(movement_sound)
        if keys[self.controls['up']]:
            self.velocity_x += SPACESHIP_SPEED * math.cos(math.radians(self.angle))
            self.velocity_y -= SPACESHIP_SPEED * math.sin(math.radians(self.angle))
            pygame.mixer.Sound.play(movement_sound)
        if keys[self.controls['down']]:
            self.velocity_x -= SPACESHIP_SPEED * math.cos(math.radians(self.angle))
            self.velocity_y += SPACESHIP_SPEED * math.sin(math.radians(self.angle))
            pygame.mixer.Sound.play(movement_sound)

        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS

        # Wrap around screen
        self.x %= SCREEN_WIDTH
        self.y %= SCREEN_HEIGHT

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
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), PLANET_RADIUS)

    def apply_gravity(self, spaceship):
        dx = self.x - spaceship.x
        dy = self.y - spaceship.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > PLANET_RADIUS:
            force = GRAVITY_CONSTANT / (distance ** 2)
            angle = math.atan2(dy, dx)
            spaceship.velocity_x += force * math.cos(angle) / FPS
            spaceship.velocity_y += force * math.sin(angle) / FPS

# Initialize game objects
planet = Planet(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
spaceship1 = Spaceship(100, 100, spaceship1_image, {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'shoot': pygame.K_RSHIFT
})
spaceship2 = Spaceship(700, 500, spaceship2_image, {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'up': pygame.K_w,
    'down': pygame.K_s,
    'shoot': pygame.K_SPACE
})

# Scores
score1 = 0
score2 = 0

# Main game loop
game_running = True
while game_running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == spaceship1.controls['shoot']:
                spaceship1.shoot()
            if event.key == spaceship2.controls['shoot']:
                spaceship2.shoot()

    # Apply gravity
    planet.apply_gravity(spaceship1)
    planet.apply_gravity(spaceship2)

    # Move spaceships
    spaceship1.move()
    spaceship2.move()

    # Move and draw bullets
    for spaceship in [spaceship1, spaceship2]:
        for bullet in spaceship.bullets[:]:
            if not bullet.move():
                spaceship.bullets.remove(bullet)

    # Detect collisions
    for bullet in spaceship1.bullets[:]:
        if math.hypot(bullet.x - spaceship2.x, bullet.y - spaceship2.y) < 40:
            score1 += 1
            spaceship1.bullets.remove(bullet)
            spaceship2.x, spaceship2.y = 700, 500  # Reset spaceship2
            pygame.mixer.Sound.play(collision_sound)

    for bullet in spaceship2.bullets[:]:
        if math.hypot(bullet.x - spaceship1.x, bullet.y - spaceship1.y) < 40:
            score2 += 1
            spaceship2.bullets.remove(bullet)
            spaceship1.x, spaceship1.y = 100, 100  # Reset spaceship1
            pygame.mixer.Sound.play(collision_sound)

    # Draw everything
    planet.draw()
    spaceship1.draw()
    spaceship2.draw()

    for bullet in spaceship1.bullets:
        bullet.draw()

    for bullet in spaceship2.bullets:
        bullet.draw()

    # Display scores
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Player 1: {score1}  Player 2: {score2}", True, WHITE)
    screen.blit(score_text, (20, 20))

    # Update display and control frame rate
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
