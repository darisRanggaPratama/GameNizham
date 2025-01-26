# game_logic.py
import sys

from game_objects import *


class GameManager:
    def __init__(self):
        pg.init()
        pg.mixer.init()

        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption("Tank Battle")

        try:
            icon = pg.image.load("assets/tanker.png")
            pg.display.set_icon(icon)
        except pg.error as e:
            print(f"Error loading icon: {e}")

        self.clock = pg.time.Clock()
        self.tank = Tank(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 100, "assets/tanker64.png")
        self.all_sprites = pg.sprite.Group(self.tank)
        self.bullets = pg.sprite.Group()

        self.sounds = {
            'move': pg.mixer.Sound("assets/tank-move.mp3"),
            'shoot': pg.mixer.Sound("assets/tank-shots.mp3")
        }

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.sounds['shoot'].play()
                    bullet = self.tank.shoot()
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

                self._handle_tank_movement(event, True)
                self.sounds['move'].play()

            if event.type == pg.KEYUP:
                self._handle_tank_movement(event, False)
                self.sounds['shoot'].stop()
                self.sounds['move'].stop()

        return True

    def _handle_tank_movement(self, event, is_keydown):
        speed = config.TANK_SPEED if is_keydown else 0
        if event.key == pg.K_LEFT or event.key == pg.K_a:
            self.tank.speed_x = -speed
        elif event.key == pg.K_RIGHT or event.key == pg.K_d:
            self.tank.speed_x = speed
        elif event.key == pg.K_UP or event.key == pg.K_w:
            self.tank.speed_y = -speed
        elif event.key == pg.K_DOWN or event.key == pg.K_s:
            self.tank.speed_y = speed

    def update(self):
        self.tank.move(self.tank.speed_x, self.tank.speed_y)
        self.bullets.update()

        # Remove bullets that go off-screen
        for bullet in self.bullets:
            if bullet.rect.bottom < 0:
                bullet.kill()

    def render(self):
        self.screen.fill(config.LIGHT_CORAL)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pg.quit()
        sys.exit()