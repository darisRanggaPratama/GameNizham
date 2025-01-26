# game.py
import sys
import math
import random
import pygame as pg

# Configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TANK_SPEED = 5
BULLET_SPEED = 10


class Tank(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, direction):
        super().__init__()
        self.image = pg.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.health = 100
        self.score = 0

        # Tambahkan inisialisasi kecepatan
        self.speed_x = 0
        self.speed_y = 0

        # Suara pergerakan tank
        self.move_sound = None
        try:
            self.move_sound = pg.mixer.Sound("assets/tank-engine.mp3")
            self.move_sound.set_volume(0.3)
        except FileNotFoundError:
            print("Missing move sound: assets/tank-engine.mp3")

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

        if (dx != 0 or dy != 0) and self.move_sound:
            self.move_sound.play()

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        return self.health == 0

    def shoot(self):
        bullet_x = self.rect.right if self.direction == 1 else self.rect.left
        bullet_y = self.rect.centery
        return Bullet(bullet_x, bullet_y, self.direction)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.speed = BULLET_SPEED * direction

        # Inisialisasi warna awal
        self.color = self._generate_random_color()
        self.radius = 5
        self.glow_radius = 15  # Radius untuk efek bersinar

        # Membuat permukaan peluru
        self.image = pg.Surface((self.glow_radius * 2, self.glow_radius * 2), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def _generate_random_color(self):
        # Pilih warna acak yang kontras dengan background (tidak putih sepenuhnya)
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def _update_color(self, frame):
        # Berkelap-kelip: Ubah nilai RGB secara dinamis
        intensity = abs(math.sin(frame / 10)) * 200 + 55  # Nilai antara 55-255
        self.color = (int(intensity), random.randint(50, 255), random.randint(50, 255))

    def update(self):
        # Perbarui posisi peluru
        self.rect.x += self.speed

        # Hapus peluru jika keluar layar
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # Perbarui warna peluru untuk efek berkelap-kelip
        frame = pg.time.get_ticks() // 50  # Dapatkan waktu dalam frame
        self._update_color(frame)

        # Gambar ulang peluru dengan efek glow
        self.image.fill((0, 0, 0, 0))  # Bersihkan permukaan
        pg.draw.circle(self.image, (self.color[0], self.color[1], self.color[2], 100),
                       (self.glow_radius, self.glow_radius), self.glow_radius)  # Glow
        pg.draw.circle(self.image, self.color,
                       (self.glow_radius, self.glow_radius), self.radius)  # Bullet


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

        # Musik dan efek suara
        try:
            pg.mixer.music.load("assets/adventure.mp3")
            pg.mixer.music.set_volume(0.5)
            pg.mixer.music.play(-1)  # Musik diputar secara loop
            self.explosion_sound = pg.mixer.Sound("assets/tank-hits.mp3")
            self.shoot_sound = pg.mixer.Sound("assets/tank-shots.mp3")
        except FileNotFoundError as e:
            print(f"Sound error: {e}")
            self.explosion_sound = None
            self.shoot_sound = None

        self.font = pg.font.Font(None, 36)
        self.game_over = False

    def randomize_positions(self):
        """Atur posisi awal kedua tank secara acak."""
        while True:
            self.tank1.rect.x = random.randint(0, SCREEN_WIDTH - self.tank1.rect.width)
            self.tank1.rect.y = random.randint(0, SCREEN_HEIGHT - self.tank1.rect.height)

            self.tank2.rect.x = random.randint(0, SCREEN_WIDTH - self.tank2.rect.width)
            self.tank2.rect.y = random.randint(0, SCREEN_HEIGHT - self.tank2.rect.height)

            # Pastikan posisi kedua tank tidak bertabrakan
            if not self.tank1.rect.colliderect(self.tank2.rect):
                break

    def reset_game(self):
        """Reset kondisi permainan."""
        self.tank1.health = 100
        self.tank2.health = 100
        self.tank1.score = 0
        self.tank2.score = 0
        self.tank1.rect.x = 50
        self.tank1.rect.y = SCREEN_HEIGHT - 100
        self.tank2.rect.x = SCREEN_WIDTH - 150
        self.tank2.rect.y = SCREEN_HEIGHT - 100
        self.randomize_positions()

        self.bullets.empty()  # Bersihkan peluru
        self.all_sprites = pg.sprite.Group(self.tank1, self.tank2)
        self.all_sprites.add(self.bullets)
        self.game_over = False

        # Restart musik
        if pg.mixer.music.get_busy() is False:
            pg.mixer.music.play(-1)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if not self.game_over and event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # Tank 1 menembak
                    self._play_sound(self.shoot_sound)
                    bullet = self.tank1.shoot()
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

                if event.key == pg.K_RETURN:  # Tank 2 menembak
                    self._play_sound(self.shoot_sound)
                    bullet = self.tank2.shoot()
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

        if not self.game_over:  # Tangkap input hanya jika game belum selesai
            keys = pg.key.get_pressed()
            self._handle_tank_movement(keys, self.tank1, {
                pg.K_a: (-TANK_SPEED, 0),
                pg.K_d: (TANK_SPEED, 0),
                pg.K_w: (0, -TANK_SPEED),
                pg.K_s: (0, TANK_SPEED),
            })
            self._handle_tank_movement(keys, self.tank2, {
                pg.K_LEFT: (-TANK_SPEED, 0),
                pg.K_RIGHT: (TANK_SPEED, 0),
                pg.K_UP: (0, -TANK_SPEED),
                pg.K_DOWN: (0, TANK_SPEED),
            })

        return True

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

        self.tank1.move(self.tank1.speed_x, self.tank1.speed_y)
        self.tank2.move(self.tank2.speed_x, self.tank2.speed_y)
        self.bullets.update()

        for bullet in self.bullets:
            self._check_bullet_collision(bullet)

    def _check_bullet_collision(self, bullet):
        target = self.tank2 if bullet.direction > 0 else self.tank1
        shooter = self.tank1 if bullet.direction > 0 else self.tank2

        if bullet.rect.colliderect(target.rect):
            self._play_sound(self.explosion_sound)
            is_destroyed = target.take_damage(20)
            shooter.score += 1
            bullet.kill()

            if is_destroyed:
                self.game_over = True
                pg.mixer.music.stop()  # Hentikan musik saat game over

    def render(self):
        background = pg.image.load("assets/background.jpeg")
        background = pg.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(background, (0, 0))

        # self.screen.fill(BACKGROUND)
        self.all_sprites.draw(self.screen)

        tank1_stats = self.font.render(f"Tank 1: {self.tank1.health}% | Score: {self.tank1.score}", True, (0, 0, 0))
        tank2_stats = self.font.render(f"Tank 2: {self.tank2.health}% | Score: {self.tank2.score}", True, (0, 0, 0))

        self.screen.blit(tank1_stats, (10, 10))
        self.screen.blit(tank2_stats, (SCREEN_WIDTH - 300, 10))

        if self.game_over:
            winner = "Tank 1 Wins!" if self.tank2.health <= 0 else "Tank 2 Wins!"
            game_over_text = self.font.render(winner, True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

        pg.display.flip()

    def _play_sound(self, sound):
        if sound:
            sound.play()

    def run(self):
        running = True
        while running:
            running = self.handle_events()

            if self.game_over:
                # Tunggu 3 detik sebelum restart
                pg.time.delay(3000)
                self.reset_game()
            else:
                self.update()

            self.render()
            self.clock.tick(60)

        pg.quit()
        sys.exit()


def main():
    GameManager().run()


if __name__ == "__main__":
    main()
