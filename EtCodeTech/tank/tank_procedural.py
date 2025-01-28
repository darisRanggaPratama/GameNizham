import sys
import math
import random
import pygame as pg

# Configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TANK_SPEED = 5
BULLET_SPEED = 10

# Global game state
screen = None
clock = None
all_sprites = None
bullets = None
font = None
game_over = False

# Tank states
tank1_rect = None
tank2_rect = None
tank1_image = None
tank2_image = None
tank1_direction = 1
tank2_direction = -1
tank1_health = 100
tank2_health = 100
tank1_score = 0
tank2_score = 0

# Sound effects
move_sound = None
explosion_sound = None
shoot_sound = None


def init_game():
    global screen, clock, all_sprites, bullets, font
    global tank1_rect, tank2_rect, tank1_image, tank2_image
    global move_sound, explosion_sound, shoot_sound

    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Tank Battle")
    clock = pg.time.Clock()

    # Load tank images
    tank1_image = pg.image.load("assets/tanker64.png").convert_alpha()
    tank2_image = pg.image.load("assets/tankers64.png").convert_alpha()

    # Initialize tank positions
    tank1_rect = tank1_image.get_rect()
    tank2_rect = tank2_image.get_rect()
    reset_tank_positions()

    # Initialize sprite groups
    all_sprites = pg.sprite.Group()
    bullets = pg.sprite.Group()

    # Load sounds
    try:
        pg.mixer.music.load("assets/adventure.mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        move_sound = pg.mixer.Sound("assets/tank-engine.mp3")
        move_sound.set_volume(0.3)
        explosion_sound = pg.mixer.Sound("assets/tank-hits.mp3")
        shoot_sound = pg.mixer.Sound("assets/tank-shots.mp3")
    except FileNotFoundError as e:
        print(f"Sound error: {e}")

    font = pg.font.Font(None, 36)


def reset_tank_positions():
    global tank1_rect, tank2_rect
    while True:
        tank1_rect.x = random.randint(0, SCREEN_WIDTH - tank1_rect.width)
        tank1_rect.y = random.randint(0, SCREEN_HEIGHT - tank1_rect.height)
        tank2_rect.x = random.randint(0, SCREEN_WIDTH - tank2_rect.width)
        tank2_rect.y = random.randint(0, SCREEN_HEIGHT - tank2_rect.height)
        if not tank1_rect.colliderect(tank2_rect):
            break


def move_tank(rect, dx, dy):
    if move_sound and (dx != 0 or dy != 0):
        move_sound.play()

    rect.x += dx
    rect.y += dy
    rect.x = max(0, min(rect.x, SCREEN_WIDTH - rect.width))
    rect.y = max(0, min(rect.y, SCREEN_HEIGHT - rect.height))


def create_bullet(x, y, direction):
    bullet = pg.sprite.Sprite()
    bullet.direction = direction
    bullet.speed = BULLET_SPEED * direction
    bullet.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    bullet.radius = 5
    bullet.glow_radius = 15

    bullet.image = pg.Surface((bullet.glow_radius * 2, bullet.glow_radius * 2), pg.SRCALPHA)
    bullet.rect = bullet.image.get_rect(center=(x, y))

    return bullet


def update_bullet(bullet):
    bullet.rect.x += bullet.speed

    if bullet.rect.right < 0 or bullet.rect.left > SCREEN_WIDTH:
        bullet.kill()
        return

    frame = pg.time.get_ticks() // 50
    intensity = abs(math.sin(frame / 10)) * 200 + 55
    bullet.color = (int(intensity), random.randint(50, 255), random.randint(50, 255))

    bullet.image.fill((0, 0, 0, 0))
    pg.draw.circle(bullet.image, (*bullet.color, 100),
                   (bullet.glow_radius, bullet.glow_radius), bullet.glow_radius)
    pg.draw.circle(bullet.image, bullet.color,
                   (bullet.glow_radius, bullet.glow_radius), bullet.radius)


def handle_bullet_collision(bullet):
    global tank1_health, tank2_health, tank1_score, tank2_score, game_over

    target_rect = tank2_rect if bullet.direction > 0 else tank1_rect

    if bullet.rect.colliderect(target_rect):
        if explosion_sound:
            explosion_sound.play()

        if bullet.direction > 0:
            tank2_health = max(0, tank2_health - 20)
            tank1_score += 1
            if tank2_health == 0:
                game_over = True
        else:
            tank1_health = max(0, tank1_health - 20)
            tank2_score += 1
            if tank1_health == 0:
                game_over = True

        bullet.kill()
        if game_over:
            pg.mixer.music.stop()


def reset_game():
    global tank1_health, tank2_health, tank1_score, tank2_score, game_over

    tank1_health = 100
    tank2_health = 100
    tank1_score = 0
    tank2_score = 0
    reset_tank_positions()
    bullets.empty()
    game_over = False

    if not pg.mixer.music.get_busy():
        pg.mixer.music.play(-1)


def handle_events():
    global game_over

    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if not game_over and event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:  # Tank 1 shoot
                if shoot_sound:
                    shoot_sound.play()
                bullet = create_bullet(tank1_rect.right, tank1_rect.centery, tank1_direction)
                bullets.add(bullet)
                all_sprites.add(bullet)

            if event.key == pg.K_RETURN:  # Tank 2 shoot
                if shoot_sound:
                    shoot_sound.play()
                bullet = create_bullet(tank2_rect.left, tank2_rect.centery, tank2_direction)
                bullets.add(bullet)
                all_sprites.add(bullet)

    if not game_over:
        keys = pg.key.get_pressed()

        # Tank 1 movement
        dx = dy = 0
        if keys[pg.K_a]:
            dx = -TANK_SPEED
        elif keys[pg.K_d]:
            dx = TANK_SPEED
        if keys[pg.K_w]:
            dy = -TANK_SPEED
        elif keys[pg.K_s]:
            dy = TANK_SPEED
        move_tank(tank1_rect, dx, dy)

        # Tank 2 movement
        dx = dy = 0
        if keys[pg.K_LEFT]:
            dx = -TANK_SPEED
        elif keys[pg.K_RIGHT]:
            dx = TANK_SPEED
        if keys[pg.K_UP]:
            dy = -TANK_SPEED
        elif keys[pg.K_DOWN]:
            dy = TANK_SPEED
        move_tank(tank2_rect, dx, dy)

    return True


def update():
    if game_over:
        return

    for bullet in bullets:
        update_bullet(bullet)
        handle_bullet_collision(bullet)


def render():
    background = pg.image.load("assets/background.jpeg")
    background = pg.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))

    # Draw tanks
    screen.blit(tank1_image, tank1_rect)
    screen.blit(tank2_image, tank2_rect)

    # Draw bullets
    bullets.draw(screen)

    # Draw stats
    tank1_stats = font.render(f"Tank 1: {tank1_health}% | Score: {tank1_score}", True, (0, 0, 0))
    tank2_stats = font.render(f"Tank 2: {tank2_health}% | Score: {tank2_score}", True, (0, 0, 0))
    screen.blit(tank1_stats, (10, 10))
    screen.blit(tank2_stats, (SCREEN_WIDTH - 300, 10))

    if game_over:
        winner = "Tank 1 Wins!" if tank2_health <= 0 else "Tank 2 Wins!"
        game_over_text = font.render(winner, True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    pg.display.flip()


def main():
    init_game()
    running = True

    while running:
        running = handle_events()

        if game_over:
            pg.time.delay(3000)
            reset_game()
        else:
            update()

        render()
        clock.tick(60)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()