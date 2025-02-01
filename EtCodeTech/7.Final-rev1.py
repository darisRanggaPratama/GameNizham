import math
import random
import pygame as pg
from pygame import mixer

# Inisialisasi Pygame dan mixer
pg.init()
mixer.init()

# Konfigurasi layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Spaceship OOP Edition")

# Warna dan efek visual
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]


# Kelas GameObject
class GameObject:
    def __init__(self, image_path, x, y):
        self.image = pg.image.load(image_path)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


# Kelas Player
class Player(GameObject):
    def __init__(self):
        super().__init__("OOP/picture/jet.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 5
        self.health = 100
        self.last_shot = pg.time.get_ticks()
        self.moving = False
        self.move_sound = mixer.Sound("OOP/picture/tank-engine.mp3")

    def move(self, dx):
        self.x += dx * self.speed
        self.x = max(0, min(SCREEN_WIDTH - self.image.get_width(), self.x))
        if not self.moving:
            self.move_sound.play(-1)
            self.moving = True

    def stop(self):
        if self.moving:
            self.move_sound.stop()
            self.moving = False

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > 500:  # Tembak setiap 0.5 detik
            self.last_shot = now
            return Bullet(self.x + self.image.get_width() // 2, self.y)
        return None


# Kelasan Bullet
class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__("OOP/picture/bomb2.png", x, y)
        self.radius = 5
        self.color_index = 0
        self.speed = 10
        self.hit_sound = mixer.Sound("OOP/picture/tank-shots.mp3")
        self.rect.center = (x, y)

    def update(self):
        self.y -= self.speed
        self.color_index = (self.color_index + 1) % len(COLORS)
        # Update rect position sesuai dengan posisi aktual peluru
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        # Efek peluru bercahaya
        pg.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius + 2)
        pg.draw.circle(screen, COLORS[self.color_index], (self.x, self.y), self.radius)


# Kelas Enemy
class Enemy(GameObject):
    def __init__(self):
        super().__init__("OOP/picture/bomb.png", random.randint(0, SCREEN_WIDTH - 50), -50)
        self.speed = 3
        self.hit_sound = mixer.Sound("OOP/picture/tank-explode.mp3")

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.y = -self.image.get_height()


# Kelas Game
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = [Enemy() for _ in range(5)]
        self.bullets = []
        self.score = 0
        self.start_time = 0
        self.running = True
        self.font = pg.font.Font(None, 36)
        self.background = pg.transform.scale(
            pg.image.load("OOP/picture/space3.jpg"),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        mixer.music.load("OOP/picture/adventure.mp3")

    def check_collision(self, obj1, obj2):
        return obj1.rect.colliderect(obj2.rect)

    def show_stats(self):
        time_text = self.font.render(
            f"Time: {(pg.time.get_ticks() - self.start_time) // 1000}s",
            True, (255, 255, 255))
        health_text = self.font.render(
            f"Health: {self.player.health}",
            True, (255, 255, 255))
        screen.blit(time_text, (10, 50))
        screen.blit(health_text, (10, 90))

    def game_over(self):
        mixer.music.stop()
        screen.fill((0, 0, 0))
        texts = [
            f"Final Score: {self.score}",
            f"Time Survived: {(pg.time.get_ticks() - self.start_time) // 1000}s",
            f"Remaining Health: {self.player.health}%"
        ]
        for i, text in enumerate(texts):
            text_surf = self.font.render(text, True, (255, 255, 255))
            screen.blit(text_surf, (SCREEN_WIDTH // 2 - 150, 200 + i * 40))
        pg.display.update()
        pg.time.delay(3000)
        self.__init__()

    def run(self):
        self.start_time = pg.time.get_ticks()
        mixer.music.play(-1)

        while self.running:
            screen.blit(self.background, (0, 0))

            # Event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # Player movement
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.player.move(-1)
            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.player.move(1)
            else:
                self.player.stop()

            # Shooting
            if bullet := self.player.shoot():
                self.bullets.append(bullet)
                bullet.hit_sound.play()

            # Update game objects
            for bullet in self.bullets[:]:
                bullet.update()
                if bullet.y < 0:
                    self.bullets.remove(bullet)

            for enemy in self.enemies:
                enemy.y += enemy.speed
                if enemy.y > SCREEN_HEIGHT:
                    enemy.reset()

                # Collision bullet-enemy
                for bullet in self.bullets[:]:
                    if self.check_collision(enemy, bullet):
                        enemy.hit_sound.play()
                        self.score += 1
                        enemy.reset()
                        self.bullets.remove(bullet)

                # Collision player-enemy
                if self.check_collision(self.player, enemy):
                    self.player.health -= 1
                    enemy.reset()
                    if self.player.health <= 0:
                        self.game_over()

            # Victory condition
            if self.score >= 200:
                self.game_over()

            # Drawing
            self.player.draw(screen)
            for enemy in self.enemies:
                enemy.draw(screen)
            for bullet in self.bullets:
                bullet.draw(screen)

            # UI Elements
            self.show_stats()
            showScore = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            screen.blit(showScore, (10, 10))

            pg.display.update()
            pg.time.Clock().tick(60)


# Jalankan game
if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()
