import random
import time

import pygame


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
        self.gravity = 0.6  # Gravitasi ditingkatkan
        self.jump_power = -15  # Kekuatan lompat ditingkatkan
        self.can_double_jump = False  # Untuk double jump
        self.acceleration = 2  # Akselerasi gerakan
        self.max_velocity = 20  # Kecepatan maksimal
        self.horizontal_velocity = 0  # Kecepatan horizontal

        self.is_ducking = False
        self.duck_image = pygame.image.load("OOP/picture/kitty2.png")
        self.duck_image = pygame.transform.scale(self.duck_image, (50, 50))
        self.run_image = self.image

        self.jump_sound = pygame.mixer.Sound("OOP/picture/jump.mp3")

    def jump(self):
        # Implementasi multi-jump
        if self.rect.y >= 300 or self.can_double_jump:
            self.velocity = self.jump_power
            self.jump_sound.play()
            if self.rect.y >= 300:
                self.can_double_jump = True
            else:
                self.can_double_jump = False

    def move_left(self):
        self.horizontal_velocity = max(self.horizontal_velocity - self.acceleration, -self.max_velocity)

    def move_right(self):
        self.horizontal_velocity = min(self.horizontal_velocity + self.acceleration, self.max_velocity)

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

        # Update posisi horizontal dengan momentum
        self.rect.x += self.horizontal_velocity

        # Perlambatan horizontal (friction)
        if self.horizontal_velocity > 0:
            self.horizontal_velocity = max(0, self.horizontal_velocity - 1)
        elif self.horizontal_velocity < 0:
            self.horizontal_velocity = min(0, self.horizontal_velocity + 1)

        # Batasi pergerakan dalam layar
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 750:  # 800 - lebar dino
            self.rect.x = 750

        # Batasi posisi di ground
        if self.rect.y >= 300:
            self.rect.y = 300
            self.velocity = 0
            self.can_double_jump = False


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
        super().__init__(0, 360, 800, 40, "OOP/picture/ground.png")
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

        # Tambahkan timer untuk siklus siang/malam
        self.day_night_timer = time.time()
        self.is_day = True
        self.day_color = (255, 255, 255)  # Putih untuk siang
        self.night_color = (50, 50, 100)  # Biru gelap untuk malam
        self.current_bg_color = self.day_color

        self.dino = Dino(50, 300)
        self.ground = Ground()
        self.obstacles = []
        self.clouds = []

        self.game_over_sound = pygame.mixer.Sound("OOP/picture/game-over.mp3")
        self.background_music = pygame.mixer.Sound("OOP/picture/adventure.mp3")
        self.background_music.play(-1)

        self.game_active = True
        self.game_over_time = 0

    def handle_events(self):
        keys = pygame.key.get_pressed()

        # Continuous movement controls
        if self.game_active:
            if keys[pygame.K_LEFT]:
                self.dino.move_left()
            if keys[pygame.K_RIGHT]:
                self.dino.move_right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.dino.jump()
                if event.key == pygame.K_DOWN:
                    self.dino.duck()
                if event.key == pygame.K_RETURN and not self.game_active:
                    if time.time() - self.game_over_time >= 3:
                        self.reset_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.dino.stand()

        return True

    def update_day_night_cycle(self):
        current_time = time.time()
        if current_time - self.day_night_timer >= 10:  # Setiap 10 detik
            self.day_night_timer = current_time
            self.is_day = not self.is_day

            # Transisi warna yang lebih halus
            if self.is_day:
                self.current_bg_color = self.day_color
            else:
                self.current_bg_color = self.night_color

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
            if current_time - self.game_over_time >= 3:
                pygame.mixer.stop()
            return

        self.update_day_night_cycle()
        self.dino.update()
        self.ground.update(self.game_speed)

        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen]
        for obstacle in self.obstacles:
            obstacle.update(self.game_speed)
            if self.dino.rect.colliderect(obstacle.rect):
                self.game_over()

        self.clouds = [cloud for cloud in self.clouds if not cloud.is_off_screen]
        for cloud in self.clouds:
            cloud.update()

        self.spawn_obstacles()
        self.spawn_clouds()

        self.score += 1
        self.game_speed = self.score // 100

    def draw(self):
        self.screen.fill(self.current_bg_color)

        for cloud in self.clouds:
            cloud.draw(self.screen)
        self.ground.draw(self.screen)
        self.dino.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        ORANGE = (255, 165, 0)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        PURPLE = (128, 0, 128)
        score_text = self.font.render(f"Score: {self.score}", True, ORANGE)
        self.screen.blit(score_text, (650, 20))

        high_score_text = self.font.render(f"HI: {self.high_score}", True, BLACK)
        self.screen.blit(high_score_text, (650, 50))

        if not self.game_active:
            if time.time() - self.game_over_time >= 3:
                game_over_text = self.font.render("Press Enter to Restart", True, PURPLE)
            else:
                game_over_text = self.font.render("GAME OVER", True, RED)
            self.screen.blit(game_over_text, (300, 200))

        pygame.display.flip()

    def game_over(self):
        self.game_active = False
        self.game_over_time = time.time()
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
        self.background_music.play(-1)

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