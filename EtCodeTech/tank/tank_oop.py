import pygame as pg
import random
import math
import sys

# constants.py
class GameConfig:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TANK_SPEED = 5
    BULLET_SPEED = 10
    FPS = 60


# assets.py
class AssetManager:
    def __init__(self):
        self.sounds = {}
        self.images = {}

    def load_sounds(self):
        sound_files = {
            'engine': "assets/tank-engine.mp3",
            'explosion': "assets/tank-hits.mp3",
            'shoot': "assets/tank-shots.mp3",
            'background': "assets/adventure.mp3"
        }

        for key, path in sound_files.items():
            try:
                if key == 'background':
                    pg.mixer.music.load(path)
                    pg.mixer.music.set_volume(0.5)
                else:
                    self.sounds[key] = pg.mixer.Sound(path)
                    if key == 'engine':
                        self.sounds[key].set_volume(0.3)
            except FileNotFoundError:
                print(f"Missing sound: {path}")
                self.sounds[key] = None

    def load_images(self):
        try:
            self.images['tank1'] = pg.image.load("assets/tanker64.png").convert_alpha()
            self.images['tank2'] = pg.image.load("assets/tankers64.png").convert_alpha()
            self.images['background'] = pg.image.load("assets/background.jpeg")
            self.images['background'] = pg.transform.scale(
                self.images['background'],
                (GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT)
            )
        except FileNotFoundError as e:
            print(f"Missing image: {e}")

    def get_sound(self, key):
        return self.sounds.get(key)

    def get_image(self, key):
        return self.images.get(key)


class Tank(pg.sprite.Sprite):
    def __init__(self, x, y, image, direction, asset_manager):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.health = 100
        self.score = 0
        self.speed_x = 0
        self.speed_y = 0
        self.move_sound = asset_manager.get_sound('engine')

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self._keep_in_bounds()
        self._play_move_sound(dx, dy)

    def _keep_in_bounds(self):
        self.rect.x = max(0, min(self.rect.x, GameConfig.SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, GameConfig.SCREEN_HEIGHT - self.rect.height))

    def _play_move_sound(self, dx, dy):
        if (dx != 0 or dy != 0) and self.move_sound:
            self.move_sound.play()

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        return self.health == 0

    def shoot(self):
        bullet_x = self.rect.right if self.direction == 1 else self.rect.left
        return Bullet(bullet_x, self.rect.centery, self.direction)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.speed = GameConfig.BULLET_SPEED * direction
        self.color = self._generate_random_color()
        self.radius = 5
        self.glow_radius = 15
        self._init_image(x, y)

    def _init_image(self, x, y):
        self.image = pg.Surface((self.glow_radius * 2, self.glow_radius * 2), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def _generate_random_color(self):
        return (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

    def _update_color(self, frame):
        intensity = abs(math.sin(frame / 10)) * 200 + 55
        self.color = (
            int(intensity),
            random.randint(50, 255),
            random.randint(50, 255)
        )

    def update(self):
        self._update_position()
        self._update_appearance()

    def _update_position(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > GameConfig.SCREEN_WIDTH:
            self.kill()

    def _update_appearance(self):
        frame = pg.time.get_ticks() // 50
        self._update_color(frame)
        self._redraw_bullet()

    def _redraw_bullet(self):
        self.image.fill((0, 0, 0, 0))
        pg.draw.circle(
            self.image,
            (*self.color, 100),
            (self.glow_radius, self.glow_radius),
            self.glow_radius
        )
        pg.draw.circle(
            self.image,
            self.color,
            (self.glow_radius, self.glow_radius),
            self.radius
        )


class UIManager:
    def __init__(self):
        self.font = pg.font.Font(None, 36)

    def draw_stats(self, screen, tank1, tank2):
        tank1_stats = self.font.render(
            f"Tank 1: {tank1.health}% | Score: {tank1.score}",
            True,
            (0, 0, 0)
        )
        tank2_stats = self.font.render(
            f"Tank 2: {tank2.health}% | Score: {tank2.score}",
            True,
            (0, 0, 0)
        )

        screen.blit(tank1_stats, (10, 10))
        screen.blit(tank2_stats, (GameConfig.SCREEN_WIDTH - 300, 10))

    def draw_game_over(self, screen, winner):
        text = self.font.render(f"{winner} Wins!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)


class GameManager:
    def __init__(self):
        pg.init()
        pg.mixer.init()

        self.screen = pg.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pg.display.set_caption("Tank Battle")

        self.clock = pg.time.Clock()
        self.asset_manager = AssetManager()
        self.ui_manager = UIManager()

        self._init_game()

    def _init_game(self):
        self.asset_manager.load_sounds()
        self.asset_manager.load_images()

        self.tank1 = Tank(
            50,
            GameConfig.SCREEN_HEIGHT - 100,
            self.asset_manager.get_image('tank1'),
            1,
            self.asset_manager
        )
        self.tank2 = Tank(
            GameConfig.SCREEN_WIDTH - 150,
            GameConfig.SCREEN_HEIGHT - 100,
            self.asset_manager.get_image('tank2'),
            -1,
            self.asset_manager
        )

        self.all_sprites = pg.sprite.Group(self.tank1, self.tank2)
        self.bullets = pg.sprite.Group()
        self.game_over = False

        pg.mixer.music.play(-1)

    def reset_game(self):
        self._init_game()
        self._randomize_positions()

    def _randomize_positions(self):
        while True:
            self.tank1.rect.x = random.randint(0, GameConfig.SCREEN_WIDTH - self.tank1.rect.width)
            self.tank1.rect.y = random.randint(0, GameConfig.SCREEN_HEIGHT - self.tank1.rect.height)

            self.tank2.rect.x = random.randint(0, GameConfig.SCREEN_WIDTH - self.tank2.rect.width)
            self.tank2.rect.y = random.randint(0, GameConfig.SCREEN_HEIGHT - self.tank2.rect.height)

            if not self.tank1.rect.colliderect(self.tank2.rect):
                break

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if not self.game_over and event.type == pg.KEYDOWN:
                self._handle_shooting(event)

        if not self.game_over:
            self._handle_movement()

        return True

    def _handle_shooting(self, event):
        if event.key == pg.K_SPACE:
            self._shoot(self.tank1)
        elif event.key == pg.K_RETURN:
            self._shoot(self.tank2)

    def _shoot(self, tank):
        shoot_sound = self.asset_manager.get_sound('shoot')
        if shoot_sound:
            shoot_sound.play()
        bullet = tank.shoot()
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def _handle_movement(self):
        keys = pg.key.get_pressed()

        # Tank 1 controls
        self._handle_tank_movement(keys, self.tank1, {
            pg.K_a: (-GameConfig.TANK_SPEED, 0),
            pg.K_d: (GameConfig.TANK_SPEED, 0),
            pg.K_w: (0, -GameConfig.TANK_SPEED),
            pg.K_s: (0, GameConfig.TANK_SPEED),
        })

        # Tank 2 controls
        self._handle_tank_movement(keys, self.tank2, {
            pg.K_LEFT: (-GameConfig.TANK_SPEED, 0),
            pg.K_RIGHT: (GameConfig.TANK_SPEED, 0),
            pg.K_UP: (0, -GameConfig.TANK_SPEED),
            pg.K_DOWN: (0, GameConfig.TANK_SPEED),
        })

    def _handle_tank_movement(self, keys, tank, controls):
        dx, dy = 0, 0
        for key, (move_x, move_y) in controls.items():
            if keys[key]:
                dx, dy = move_x, move_y
                break
        tank.move(dx, dy)

    def update(self):
        if self.game_over:
            return

        self.bullets.update()

        for bullet in self.bullets:
            self._check_bullet_collision(bullet)

    def _check_bullet_collision(self, bullet):
        target = self.tank2 if bullet.direction > 0 else self.tank1
        shooter = self.tank1 if bullet.direction > 0 else self.tank2

        if bullet.rect.colliderect(target.rect):
            explosion_sound = self.asset_manager.get_sound('explosion')
            if explosion_sound:
                explosion_sound.play()

            is_destroyed = target.take_damage(20)
            shooter.score += 1
            bullet.kill()

            if is_destroyed:
                self.game_over = True
                pg.mixer.music.stop()

    def render(self):
        self.screen.blit(self.asset_manager.get_image('background'), (0, 0))
        self.all_sprites.draw(self.screen)

        self.ui_manager.draw_stats(self.screen, self.tank1, self.tank2)

        if self.game_over:
            winner = "Tank 1" if self.tank2.health <= 0 else "Tank 2"
            self.ui_manager.draw_game_over(self.screen, winner)

        pg.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()

            if self.game_over:
                pg.time.delay(3000)
                self.reset_game()
            else:
                self.update()

            self.render()
            self.clock.tick(GameConfig.FPS)

        pg.quit()
        sys.exit()


def main():
    GameManager().run()


if __name__ == "__main__":
    main()