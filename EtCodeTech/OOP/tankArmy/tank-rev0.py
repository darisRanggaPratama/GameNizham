import pygame as pg
import sys
import random

# config.py
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
LIGHT_CORAL = WHITE
TANK_SPEED = 5
BULLET_SPEED = 10

class Tank(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, direction):
        super().__init__()
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.direction = direction
        self.max_health = 100
        self.health = self.max_health
        self.score = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        return self.health == 0

    def shoot(self):
        bullet_x = self.rect.right if self.direction == 1 else self.rect.left
        return Bullet(bullet_x, self.rect.centery, self.direction)

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.damage = 20
        self.image = pg.Surface((10, 5), pg.SRCALPHA)
        self.image.fill((255, 0, 0))  # Red bullet
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = BULLET_SPEED * 2 * direction
        self.direction = direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class GameManager:
    def __init__(self):
        pg.init()
        pg.mixer.init()

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Tank Battle")

        self.clock = pg.time.Clock()
        self.tank1 = Tank(50, SCREEN_HEIGHT - 100, "assets/tanker64.png", 1)
        self.tank2 = Tank(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, "assets/tankers64.png", -1)

        self.all_sprites = pg.sprite.Group(self.tank1, self.tank2)
        self.bullets = pg.sprite.Group()

        # Sound effects
        try:
            self.explosion_sound = pg.mixer.Sound("assets/tank-hits.mp3")
            self.shoot_sound = pg.mixer.Sound("assets/tank-shots.mp3")
        except Exception as e:
            print(f"Sound error: {e}")
            self.explosion_sound = None
            self.shoot_sound = None

        self.font = pg.font.Font(None, 36)
        self.game_over = False

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if not self.game_over and event.type == pg.KEYDOWN:
                # Tank 1 controls (WASD)
                if event.key == pg.K_SPACE:
                    if self.shoot_sound:
                        self.shoot_sound.play()
                    bullet = self.tank1.shoot()
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

                # Tank 2 controls (Arrow keys)
                if event.key == pg.K_RETURN:
                    if self.shoot_sound:
                        self.shoot_sound.play()
                    bullet = self.tank2.shoot()
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

        keys = pg.key.get_pressed()
        self._handle_tank_movement(keys, self.tank1, {
            pg.K_a: (-TANK_SPEED, 0), 
            pg.K_d: (TANK_SPEED, 0), 
            pg.K_w: (0, -TANK_SPEED), 
            pg.K_s: (0, TANK_SPEED)
        })
        self._handle_tank_movement(keys, self.tank2, {
            pg.K_LEFT: (-TANK_SPEED, 0), 
            pg.K_RIGHT: (TANK_SPEED, 0), 
            pg.K_UP: (0, -TANK_SPEED), 
            pg.K_DOWN: (0, TANK_SPEED)
        })

        return True

    def _handle_tank_movement(self, keys, tank, controls):
        tank.speed_x, tank.speed_y = 0, 0
        for key, (dx, dy) in controls.items():
            if keys[key]:
                tank.speed_x, tank.speed_y = dx, dy
                break

    def update(self):
        if self.game_over:
            return

        self.tank1.move(self.tank1.speed_x, self.tank1.speed_y)
        self.tank2.move(self.tank2.speed_x, self.tank2.speed_y)
        self.bullets.update()

        for bullet in list(self.bullets):
            # Check collision with opposite tank
            if bullet.direction > 0 and bullet.rect.colliderect(self.tank1.rect):
                if self.explosion_sound:
                    self.explosion_sound.play()
                is_destroyed = self.tank1.take_damage(bullet.damage)
                self.tank2.score += 1
                bullet.kill()

                if is_destroyed:
                    self.game_over = True

            elif bullet.direction < 0 and bullet.rect.colliderect(self.tank2.rect):
                if self.explosion_sound:
                    self.explosion_sound.play()
                is_destroyed = self.tank2.take_damage(bullet.damage)
                self.tank1.score += 1
                bullet.kill()

                if is_destroyed:
                    self.game_over = True

    def render(self):
        self.screen.fill(LIGHT_CORAL)
        self.all_sprites.draw(self.screen)

        # Render scores and health
        tank1_score = self.font.render(f"Tank 1 Score: {self.tank1.score}", True, (0, 0, 0))
        tank2_score = self.font.render(f"Tank 2 Score: {self.tank2.score}", True, (0, 0, 0))
        
        tank1_health = self.font.render(f"Tank 1 Health: {self.tank1.health}%", True, (0, 0, 0))
        tank2_health = self.font.render(f"Tank 2 Health: {self.tank2.health}%", True, (0, 0, 0))

        self.screen.blit(tank1_score, (10, 10))
        self.screen.blit(tank2_score, (SCREEN_WIDTH - 200, 10))
        self.screen.blit(tank1_health, (10, 50))
        self.screen.blit(tank2_health, (SCREEN_WIDTH - 200, 50))

        if self.game_over:
            winner_text = "Tank 2 Wins!" if self.tank1.health <= 0 else "Tank 1 Wins!"
            game_over_text = self.font.render(winner_text, True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
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

def main():
    game = GameManager()
    game.run()

if __name__ == "__main__":
    main()
