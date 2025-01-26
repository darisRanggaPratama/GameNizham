# game_logic.py
import sys
import pygame as pg

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
        self.tank1 = Tank(50, config.SCREEN_HEIGHT - 100, "assets/tanker64.png", 1)
        self.tank2 = Tank(config.SCREEN_WIDTH - 150, config.SCREEN_HEIGHT - 100, "assets/tankers64.png", -1)

        self.all_sprites = pg.sprite.Group(self.tank1, self.tank2)
        self.bullets = pg.sprite.Group()

        self.sounds = {
            'move': pg.mixer.Sound("assets/tank-move.mp3"),
            'shoot': pg.mixer.Sound("assets/tank-shots.mp3"),
            'explosion': pg.mixer.Sound("assets/tank-hits.mp3")  # Add explosion sound
        }

        self.font = pg.font.Font(None, 36)
        self.game_over = False

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if not self.game_over and event.type == pg.KEYDOWN:
                # Tank 1 controls (WASD)
                if event.key == pg.K_SPACE:
                    self.sounds['shoot'].play()
                    bullet = self.tank1.shoot()
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

                self._handle_tank_movement(event, self.tank1, True)
                self.sounds['move'].play()

                # Tank 2 controls (Arrow keys)
                if event.key == pg.K_RETURN:
                    self.sounds['shoot'].play()
                    bullet = self.tank2.shoot()
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

                self._handle_tank_movement(event, self.tank2, True)

            if event.type == pg.KEYUP:
                self._handle_tank_movement(event, self.tank1, False)
                self._handle_tank_movement(event, self.tank2, False)
                self.sounds['shoot'].stop()
                self.sounds['move'].stop()

        return True

    def _handle_tank_movement(self, event, tank, is_keydown):
        speed = config.TANK_SPEED if is_keydown else 0
        tank_controls = {
            self.tank1: {pg.K_a: (-speed, 0), pg.K_d: (speed, 0), pg.K_w: (0, -speed), pg.K_s: (0, speed)},
            self.tank2: {pg.K_LEFT: (-speed, 0), pg.K_RIGHT: (speed, 0), pg.K_UP: (0, -speed), pg.K_DOWN: (0, speed)}
        }

        for key, movement in tank_controls[tank].items():
            if event.key == key:
                if tank == self.tank1:
                    tank.speed_x, tank.speed_y = movement
                else:
                    tank.speed_x, tank.speed_y = movement

    def update(self):
        if self.game_over:
            return

        self.tank1.move(self.tank1.speed_x, self.tank1.speed_y)
        self.tank2.move(self.tank2.speed_x, self.tank2.speed_y)
        self.bullets.update()

        # Remove bullets that go off-screen and check for collisions
        for bullet in list(self.bullets):
            if bullet.rect.left < 0 or bullet.rect.right > config.SCREEN_WIDTH:
                bullet.kill()

            # Check collision with opposite tank
            if bullet.direction > 0 and bullet.rect.colliderect(self.tank1.rect):
                self.sounds['explosion'].play()
                is_tank_destroyed = self.tank1.take_damage(bullet.damage)
                self.tank2.score += 1
                bullet.kill()

                if is_tank_destroyed:
                    self.game_over = True

            elif bullet.direction < 0 and bullet.rect.colliderect(self.tank2.rect):
                self.sounds['explosion'].play()
                is_tank_destroyed = self.tank2.take_damage(bullet.damage)
                self.tank1.score += 1
                bullet.kill()

                if is_tank_destroyed:
                    self.game_over = True

    def render(self):
        self.screen.fill(config.LIGHT_CORAL)
        self.all_sprites.draw(self.screen)

        # Render scores and health
        tank1_score = self.font.render(f"Tank 1 Score: {self.tank1.score}", True, (0, 0, 0))
        tank2_score = self.font.render(f"Tank 2 Score: {self.tank2.score}", True, (0, 0, 0))
        
        tank1_health = self.font.render(f"Tank 1 Health: {self.tank1.health}%", True, (0, 0, 0))
        tank2_health = self.font.render(f"Tank 2 Health: {self.tank2.health}%", True, (0, 0, 0))

        self.screen.blit(tank1_score, (10, 10))
        self.screen.blit(tank2_score, (config.SCREEN_WIDTH - 200, 10))
        self.screen.blit(tank1_health, (10, 50))
        self.screen.blit(tank2_health, (config.SCREEN_WIDTH - 200, 50))

        if self.game_over:
            winner_text = "Tank 2 Wins!" if self.tank1.health <= 0 else "Tank 1 Wins!"
            game_over_text = self.font.render(winner_text, True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)

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
