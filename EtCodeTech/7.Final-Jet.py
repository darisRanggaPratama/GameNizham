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

    @abstractmethod
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Player(GameObject):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.speed = 5
        self.direction = 0
        self.health = 100
        self.move_sound = mixer.Sound("OOP/picture/tank-engine.mp3")
        self.collision_sound = mixer.Sound("OOP/picture/tank-explode.mp3")
        self.last_shot_time = 0
        self.shoot_delay = 500  # milliseconds

    def update(self):
        self.x += self.direction * self.speed
        self.rect.x = self.x
        if self.direction != 0:
            self.move_sound.play()

        # Auto shooting
        current_time = pg.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            self.last_shot_time = current_time
            return Bullet(self.x + self.image.get_width() // 2, self.y)
        return None


class Enemy(GameObject):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.speed = 3
        self.hit_sound = mixer.Sound("OOP/picture/tank-hits.mp3")

    def update(self):
        self.y += self.speed
        self.rect.y = self.y


class Bullet(GameObject):
    def __init__(self, x, y):
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        self.current_color = random.choice(self.colors)
        self.radius = 5
        self.speed = 7
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, self.radius * 2, self.radius * 2)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
        self.current_color = random.choice(self.colors)  # Color flicker effect

    def draw(self, screen):
        # Main bullet
        pg.draw.circle(screen, self.current_color, (int(self.x), int(self.y)), self.radius)
        # Glowing effect
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

        self.reset_game()

        # Background music
        mixer.music.load("OOP/picture/adventure.mp3")
        mixer.music.play(-1)

    def reset_game(self):
        self.player = Player(random.randint(0, self.width - 64),
                             self.height - 64, "OOP/picture/jet.png")
        self.enemy = Enemy(random.randint(0, self.width - 64),
                           0, "OOP/picture/bomb3.png")
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
        # Player-Enemy collision
        if self.player.rect.colliderect(self.enemy.rect):
            self.player.collision_sound.play()
            self.player.health -= 1
            self.enemy.y = 0
            self.enemy.x = random.randint(0, self.width - self.enemy.image.get_width())

        # Bullets-Enemy collision
        for bullet in self.bullets[:]:
            if bullet.rect.colliderect(self.enemy.rect):
                self.enemy.hit_sound.play()
                self.bullets.remove(bullet)
                self.score += 1
                self.enemy.y = 0
                self.enemy.x = random.randint(0, self.width - self.enemy.image.get_width())

    def update(self):
        # Start timer when player moves
        if self.start_time is None and self.player.direction != 0:
            self.start_time = pg.time.get_ticks()

        if self.start_time is not None:
            self.game_time = (pg.time.get_ticks() - self.start_time) // 1000

        # Update player and possibly create new bullet
        new_bullet = self.player.update()
        if new_bullet:
            self.bullets.append(new_bullet)

        # Update enemy
        self.enemy.update()
        if self.enemy.y >= self.height:
            self.enemy.y = 0
            self.enemy.x = random.randint(0, self.width - self.enemy.image.get_width())

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        # Check win/lose conditions
        if self.score >= 200 or self.player.health <= 0:
            self.show_game_over()
            mixer.music.stop()
            pg.time.delay(3000)
            self.reset_game()
            mixer.music.play(-1)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Draw game objects
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Draw HUD
        self.draw_hud()

        pg.display.flip()

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        time_text = self.font.render(f"Time: {self.game_time}s", True, (255, 255, 255))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(health_text, (10, 50))
        self.screen.blit(time_text, (10, 90))

    def show_game_over(self):
        text = "Victory!" if self.score >= 200 else "Game Over!"
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