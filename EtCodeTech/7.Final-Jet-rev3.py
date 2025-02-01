import math
import random
import pygame as pg
from pygame import mixer
from abc import ABC, abstractmethod


class GameObject(ABC):
    def __init__(self, x, y, image_path):
        self.image = pg.image.load(image_path)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.width *= 0.8
        self.rect.height *= 0.8

    @abstractmethod
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)


class Player(GameObject):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.speed = 5
        self.direction = 0
        self.health = 10
        self.move_sound = mixer.Sound("OOP/picture/tank-engine.mp3")
        self.move_sound.set_volume(0.3)
        self.collision_sound = mixer.Sound("OOP/picture/tank-explode.mp3")
        self.collision_sound.set_volume(0.5)
        self.last_shot_time = 0
        self.shoot_delay = 500
        self.is_moving = False

    def update(self):
        previous_x = self.x
        self.x += self.direction * self.speed
        self.rect.x = self.x

        if self.direction != 0 and not self.is_moving:
            self.move_sound.play(-1)
            self.is_moving = True
        elif self.direction == 0 and self.is_moving:
            self.move_sound.stop()
            self.is_moving = False

        current_time = pg.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            self.last_shot_time = current_time
            return self.create_bullets()
        return None

    def create_bullets(self):
        bullets = []
        num_bullets = random.randint(1, 5)
        spread = 20

        total_width = (num_bullets - 1) * spread
        start_x = self.x + (self.image.get_width() // 2) - (total_width // 2)

        for i in range(num_bullets):
            bullet_x = start_x + (i * spread)
            bullets.append(Bullet(bullet_x, self.y))

        return bullets

    def take_damage(self):
        self.collision_sound.play()
        self.health -= 1


class Enemy(GameObject):
    def __init__(self, x, y, image_path, speed=None):
        super().__init__(x, y, image_path)
        self.speed = speed if speed else random.uniform(2, 4)
        self.hit_sound = mixer.Sound("OOP/picture/tank-hits.mp3")
        self.hit_sound.set_volume(0.5)
        self.was_hit = False

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def hit(self):
        if not self.was_hit:
            self.hit_sound.play()
            self.was_hit = True
        return True


class Bullet(GameObject):
    def __init__(self, x, y):
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        self.current_color = random.choice(self.colors)
        self.radius = 5
        self.speed = 7
        self.x = x
        self.y = y
        self.rect = pg.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
        self.current_color = random.choice(self.colors)

    def draw(self, screen):
        pg.draw.circle(screen, self.current_color, (int(self.x), int(self.y)), self.radius)
        for r in range(3):
            alpha = 100 - (r * 30)
            surface = pg.Surface((self.radius * 4, self.radius * 4), pg.SRCALPHA)
            pg.draw.circle(surface, (*self.current_color, alpha),
                           (self.radius * 2, self.radius * 2), self.radius + r * 2)
            screen.blit(surface, (self.x - self.radius * 2, self.y - self.radius * 2))


class Game:
    def __init__(self):
        pg.init()
        mixer.init()

        self.width = 800
        self.height = 600
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Space Shooter")

        self.background = pg.image.load("OOP/picture/space3.jpg")
        self.background = pg.transform.scale(self.background, (self.width, self.height))

        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 36)

        mixer.music.load("OOP/picture/adventure.mp3")
        mixer.music.set_volume(0.3)
        mixer.music.play(-1)

        self.reset_game()

    def create_enemies(self):
        num_enemies = random.randint(1, 5)
        enemies = []

        available_width = self.width - 64  # Mengurangi lebar gambar enemy
        segment_width = available_width // num_enemies

        for i in range(num_enemies):
            x = random.randint(i * segment_width, (i + 1) * segment_width - 64)
            y = random.randint(-100, 0)  # Mulai di atas layar dengan posisi random
            speed = random.uniform(2, 4)  # Kecepatan random untuk setiap enemy
            enemy = Enemy(x, y, "OOP/picture/bomb3.png", speed)
            enemies.append(enemy)

        return enemies

    def reset_game(self):
        self.player = Player(random.randint(0, self.width - 64),
                             self.height - 64, "OOP/picture/jet.png")
        self.enemies = self.create_enemies()
        self.bullets = []
        self.score = 0
        self.start_time = None
        self.game_time = 0
        self.running = True

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_LEFT, pg.K_a]:
                    self.player.direction = -1
                if event.key in [pg.K_RIGHT, pg.K_d]:
                    self.player.direction = 1

            if event.type == pg.KEYUP:
                if event.key in [pg.K_LEFT, pg.K_a, pg.K_RIGHT, pg.K_d]:
                    self.player.direction = 0

        return True

    def check_collisions(self):
        # Player-Enemy collisions
        for enemy in self.enemies[:]:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage()
                self.enemies.remove(enemy)

        # Respawn enemies if all are destroyed
        if not self.enemies:
            self.enemies = self.create_enemies()

        # Bullets-Enemy collisions
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    if enemy.hit():
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        self.score += 1

    def update(self):
        if self.start_time is None and self.player.direction != 0:
            self.start_time = pg.time.get_ticks()

        if self.start_time is not None:
            self.game_time = (pg.time.get_ticks() - self.start_time) // 1000

        new_bullets = self.player.update()
        if new_bullets:
            self.bullets.extend(new_bullets)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.y >= self.height:
                self.enemies.remove(enemy)

        # Create new enemies if all are gone
        if not self.enemies:
            self.enemies = self.create_enemies()

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        # Boundary check for player
        if self.player.x < 0:
            self.player.x = 0
        elif self.player.x > self.width - self.player.image.get_width():
            self.player.x = self.width - self.player.image.get_width()

        # Win/lose conditions
        if self.score >= 100 or self.player.health <= 0:
            self.show_game_over()
            mixer.music.stop()
            self.player.move_sound.stop()
            pg.time.delay(3000)
            self.reset_game()
            mixer.music.play(-1)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        self.draw_hud()
        pg.display.flip()

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        time_text = self.font.render(f"Time: {self.game_time}s", True, (255, 255, 255))
        enemies_text = self.font.render(f"Enemies: {len(self.enemies)}", True, (255, 255, 255))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(health_text, (10, 50))
        self.screen.blit(time_text, (10, 90))
        self.screen.blit(enemies_text, (10, 130))

    def show_game_over(self):
        text = "Victory!" if self.score >= 100 else "Game Over!"
        game_over_text = self.font.render(text, True, (255, 255, 255))
        stats_text = self.font.render(
            f"Score: {self.score} | Time: {self.game_time}s | Health: {self.player.health}",
            True, (255, 255, 255)
        )

        self.screen.blit(game_over_text,
                         (self.width // 2 - game_over_text.get_width() // 2,
                          self.height // 2 - game_over_text.get_height() // 2))
        self.screen.blit(stats_text,
                         (self.width // 2 - stats_text.get_width() // 2,
                          self.height // 2 + game_over_text.get_height()))
        pg.display.flip()

    def run(self):
        while self.running:
            self.running = self.handle_events()
            self.check_collisions()
            self.update()
            self.draw()
            self.clock.tick(60)

        pg.quit()


if __name__ == "__main__":
    game = Game()
    game.run()