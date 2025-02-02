import pygame
import random
import os
import time


class GameObject:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path) if image_path else None
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Dino(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, "OOP/picture/kitty.png")
        self.velocity = 0
        self.gravity = 0.5
        self.is_ducking = False
        self.duck_image = pygame.image.load("OOP/picture/kitty2.png")
        self.duck_image = pygame.transform.scale(self.duck_image, (50, 50))
        self.run_image = self.image

    def jump(self):
        if self.rect.y >= 300:  # Hanya bisa lompat jika di tanah
            self.velocity = -12
            pygame.mixer.Sound("OOP/picture/jump.mp3").play()

    def duck(self):
        self.is_ducking = True
        self.image = self.duck_image

    def stand(self):
        self.is_ducking = False
        self.image = self.run_image

    def update(self):
        # Update posisi vertikal
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Batasi posisi di ground
        if self.rect.y >= 300:
            self.rect.y = 300
            self.velocity = 0


class Obstacle(GameObject):
    def __init__(self, x):
        size = random.choice([(20, 40), (30, 60), (40, 80)])
        super().__init__(x, 360 - size[1], size[0], size[1], "OOP/picture/cactus.png")
        self.speed = 5

    def update(self, game_speed):
        self.rect.x -= self.speed + game_speed

    @property
    def is_off_screen(self):
        return self.rect.x < -50


class Ground(GameObject):
    def __init__(self):
        super().__init__(0, 360, 800, 40, "OOP/picture/grass.png")
        self.scroll = 0
        self.scroll_speed = 5

    def update(self, game_speed):
        self.scroll -= (self.scroll_speed + game_speed)
        if abs(self.scroll) > self.rect.width:
            self.scroll = 0

    def draw(self, screen):
        screen.blit(self.image, (self.scroll, self.rect.y))
        screen.blit(self.image, (self.rect.width + self.scroll, self.rect.y))


class Cloud(GameObject):
    def __init__(self):
        super().__init__(800, random.randint(50, 200), 60, 30, "OOP/picture/cloud.png")
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed

    @property
    def is_off_screen(self):
        return self.rect.x < -60


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("T-Rex Runner")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)

        self.game_speed = 0
        self.score = 0
        self.high_score = 0

        self.dino = Dino(50, 300)
        self.ground = Ground()
        self.obstacles = []
        self.clouds = []

        # Load sounds
        self.game_over_sound = pygame.mixer.Sound("OOP/picture/game-over.mp3")
        self.background_music = pygame.mixer.Sound("OOP/picture/adventure.mp3")  # Tambahkan file musik background
        self.background_music.play(-1)  # -1 artinya loop forever

        self.game_active = True
        self.game_over_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.dino.jump()
                if event.key == pygame.K_DOWN:
                    self.dino.duck()
                if event.key == pygame.K_RETURN and not self.game_active:
                    if time.time() - self.game_over_time >= 3:  # Cek apakah sudah 3 detik
                        self.reset_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.dino.stand()

        return True

    def spawn_obstacles(self):
        if len(self.obstacles) == 0 or \
                self.obstacles[-1].rect.x < 600 and random.random() < 0.02:
            self.obstacles.append(Obstacle(800))

    def spawn_clouds(self):
        if len(self.clouds) == 0 or \
                self.clouds[-1].rect.x < 600 and random.random() < 0.01:
            self.clouds.append(Cloud())

    def update(self):
        if not self.game_active:
            current_time = time.time()
            if current_time - self.game_over_time >= 3:  # Setelah 3 detik
                pygame.mixer.stop()  # Hentikan semua suara
            return

        self.dino.update()
        self.ground.update(self.game_speed)

        # Update dan hapus obstacle yang sudah lewat
        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen]
        for obstacle in self.obstacles:
            obstacle.update(self.game_speed)
            if self.dino.rect.colliderect(obstacle.rect):
                self.game_over()

        # Update dan hapus awan yang sudah lewat
        self.clouds = [cloud for cloud in self.clouds if not cloud.is_off_screen]
        for cloud in self.clouds:
            cloud.update()

        # Spawn obstacles dan clouds baru
        self.spawn_obstacles()
        self.spawn_clouds()

        # Update score dan game speed
        self.score += 1
        self.game_speed = self.score // 100

    def draw(self):
        self.screen.fill((255, 255, 255))

        # Gambar semua objek
        for cloud in self.clouds:
            cloud.draw(self.screen)
        self.ground.draw(self.screen)
        self.dino.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Gambar score
        score_text = self.font.render(f"Score: {self.score}", True, (83, 83, 83))
        self.screen.blit(score_text, (650, 20))

        high_score_text = self.font.render(f"HI: {self.high_score}", True, (83, 83, 83))
        self.screen.blit(high_score_text, (650, 50))

        if not self.game_active:
            if time.time() - self.game_over_time >= 3:
                game_over_text = self.font.render("Press Enter to Restart", True, (83, 83, 83))
            else:
                game_over_text = self.font.render("GAME OVER", True, (83, 83, 83))
            self.screen.blit(game_over_text, (300, 200))

        pygame.display.flip()

    def game_over(self):
        self.game_active = False
        self.game_over_time = time.time()  # Catat waktu game over
        self.game_over_sound.play()
        if self.score > self.high_score:
            self.high_score = self.score

    def reset_game(self):
        self.game_active = True
        self.score = 0
        self.game_speed = 0
        self.dino = Dino(50, 300)
        self.obstacles.clear()
        self.clouds.clear()
        self.background_music.play(-1)  # Mulai musik background lagi

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()