import random
import pygame


class Display:
    pygame.init()
    pygame.mixer.init()
    windows = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()

    background = pygame.image.load("background.png")
    font = pygame.font.Font("SHPinscher-Regular.otf", 35)

    spaceship = pygame.image.load("space_ship.png")
    enemy_spaceship = pygame.image.load("enemy-spaceship.png")
    enemy_missile_craft = pygame.image.load("enemy-ship.png")
    laser = pygame.image.load("bullet-right.png")
    enemy_laser = pygame.image.load("bullet-left.png")
    missile = pygame.image.load("missile-left.png")

    # Sound effects
    shoot_sound = pygame.mixer.Sound("tank-shots.mp3")
    enemy_shoot_sound = pygame.mixer.Sound("tank-hits.mp3")
    explosion_sound = pygame.mixer.Sound("tank-explode.mp3")


class Text:
    def __init__(self, text: str, size: int):
        self.text = text
        self.size = size
        self.selected = False

    def display(self):
        color = (255, 0, 0) if self.selected else (255, 255, 255)
        font = pygame.font.Font("SHPinscher-Regular.otf", self.size)
        return font.render(self.text, True, color)


class Menu:
    def __init__(self):
        self.text_list = []
        self.selected = 1

    def text(self):
        text_list = ["Main Menu", "Start", "Exit"]
        size_list = [70, 40, 40]
        self.text_list = [
            Text(text_list[i], size_list[i]) for i in range(len(text_list))
        ]
        self.text_list[1].selected = True

    def controls(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.select(1)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.select(2)

    def select(self, code: int):
        for text in self.text_list:
            text.selected = False

        if code == 1:
            self.selected = 1 if self.selected == 2 else 2
        if code == 2:
            self.selected = 2 if self.selected == 1 else 1

        self.text_list[self.selected].selected = True

    def buttons_function(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.selected == 1:
                    Start().execute()
                if self.selected == 2:
                    exit()

    def objects(self):
        spacing = 50
        Display.windows.blit(Display.background, (0, 0))
        for text in self.text_list:
            Display.windows.blit(
                text.display(),
                (
                    (Display.windows.get_width() - text.display().get_width()) / 2,
                    spacing,
                ),
            )
            spacing += 100

    def execute(self):
        self.text()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                self.controls(event)
                self.buttons_function(event)

            self.objects()
            pygame.display.flip()


class GameOver:
    def __init__(self, score, health, play_time):
        self.text_list = []
        self.selected = 0
        self.score = score
        self.health = health
        self.play_time = play_time
        pygame.mixer.stop()

    def text(self, code: int):
        options = ["Yes", "No"]
        if code == 1:
            return Text("Game Over", 90).display()
        if code == 2:
            return Text(f"Score: {self.score}  Health: {self.health}  Time: {self.play_time:.1f}s", 30).display()
        if code == 3:
            self.text_list = [Text(text, 25) for text in options]
            self.text_list[0].selected = True

    def objects(self):
        Display.windows.blit(Display.background, (0, 0))
        Display.windows.blit(
            self.text(1),
            ((Display.windows.get_width() - self.text(1).get_width()) / 2, 70),
        )
        Display.windows.blit(
            self.text(2),
            ((Display.windows.get_width() - self.text(2).get_width()) / 2, 200),
        )
        for text in self.text_list:
            if text == self.text_list[0]:
                ops = (Display.windows.get_width() - text.display().get_width()) / 2 - 50
            else:
                ops = (Display.windows.get_width() - text.display().get_width()) / 2 + 50

            Display.windows.blit(text.display(), (ops, 250))

    def controls(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.select(1)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.select(2)

    def select(self, code: int):
        for text in self.text_list:
            text.selected = False

        if code == 1:
            self.selected = 0 if self.selected == 1 else 1
        if code == 2:
            self.selected = 1 if self.selected == 0 else 0

        self.text_list[self.selected].selected = True

    def buttons_func(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.selected == 0:
                    Start().execute()
                if self.selected == 1:
                    exit()

    def execute(self):
        self.text(3)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                self.controls(event)
                self.buttons_func(event)

            self.objects()
            pygame.display.flip()


class Enemies:
    def __init__(self):
        self.x = random.randint(700, 1000)
        self.y = random.randint(
            0,
            Display.windows.get_height() - Display.enemy_spaceship.get_height() + 1,
        )
        self.type = random.choice([1, 2])
        self.bullets_list = []
        self.alive = True

    def collision_box(self):
        return pygame.Rect(
            (self.x, self.y),
            (
                Display.enemy_spaceship.get_width(),
                Display.enemy_spaceship.get_height(),
            ),
        )

    def firing(self):
        self.bullets_list.append([self.x, self.y])
        if self.type == 1:
            Display.enemy_shoot_sound.play()
        else:
            Display.shoot_sound.play()


class Objects:
    def __init__(self):
        self.x = 40
        self.y = (Display.windows.get_height() - Display.spaceship.get_width()) / 2
        self.laser_list = []
        self.enemies_list = []
        self.enemy_count = 3
        self.background_list = [[0, 0], [1800, 0]]
        self.score = 0
        self.condition = 10
        self.health = 100
        self.start_time = None
        self.game_started = False

    def objects(self):
        Display.windows.fill((0, 0, 0))
        self.background()
        self.collision_box()
        Display.windows.blit(Display.spaceship, (self.x, self.y))
        self.fire_laser()
        self.enemies_movement()
        self.score_board()
        self.health_display()

    def collision_box(self):
        return pygame.Rect(
            (self.x, self.y),
            (Display.spaceship.get_width(), Display.spaceship.get_height()),
        )

    def background(self):
        for location in self.background_list:
            Display.windows.blit(Display.background, (location[0], location[1]))
            location[0] -= 2

            if location[0] + Display.background.get_width() <= 0:
                index = self.background_list.index(location)
                self.background_list[index][0] = self.background_list[index - 1][0] + 1800

    def add_enemies(self):
        if self.score >= self.condition:
            self.enemy_count += 1
            self.condition += 10

    def health_display(self):
        health_text = Display.font.render(f"Health: {self.health}", True, (255, 255, 255))
        Display.windows.blit(health_text, (10, 40))

    def score_board(self):
        score_board = Display.font.render(f"Score: {self.score}", True, (255, 255, 255))
        Display.windows.blit(score_board, (10, 0))

    def insert_laser(self):
        self.laser_list.append([self.x + Display.spaceship.get_width(), self.y])
        Display.shoot_sound.play()

    def fire_laser(self):
        # Modifikasi untuk mencegah ValueError
        for location in self.laser_list[:]:  # Salin list untuk iterasi
            rect = pygame.Rect(
                (location[0], location[1] + 15),
                (Display.laser.get_width(), Display.laser.get_height() - 30),
            )
            Display.windows.blit(Display.laser, (location[0], location[1]))

            self.laser_hit(rect, location)
            if location[0] + Display.laser.get_width() >= Display.windows.get_width():
                if location in self.laser_list:
                    self.laser_list.remove(location)
            location[0] += 5

    def laser_hit(self, rect: pygame.Rect, laser: list):
        for enemy in self.enemies_list[:]:  # Salin list untuk iterasi
            if enemy.alive:
                collision = rect.colliderect(enemy.collision_box())
                if collision:
                    Display.explosion_sound.play()
                    if laser in self.laser_list:
                        self.laser_list.remove(laser)
                    self.reset_enemies(enemy, False)
                    self.score += 1

    def reset_enemies(self, enemies: 'Enemies', condition: bool):
        enemies.alive = False
        if condition:
            if enemies in self.enemies_list:
                self.enemies_list.remove(enemies)
                self.enemy_count -= 1
        if not condition:
            new_enemy = Enemies()
            new_enemy.x = random.randint(700, 1000)
            new_enemy.y = random.randint(0, Display.windows.get_height() - Display.enemy_spaceship.get_height())
            self.enemies_list.append(new_enemy)
            self.enemy_count += 1

    def place_enemies(self):
        for i in range(self.enemy_count):
            if len(self.enemies_list) < self.enemy_count:
                self.enemies_list.append(Enemies())

    def enemies_movement(self):
        for enemies in self.enemies_list[:]:  # Salin list untuk iterasi
            if enemies.type == 1 and enemies.alive:
                Display.windows.blit(Display.enemy_spaceship, (enemies.x, enemies.y))
            if enemies.type == 2 and enemies.alive:
                Display.windows.blit(Display.enemy_missile_craft, (enemies.x, enemies.y))

            if enemies.x >= 550:
                enemies.x -= 2
            else:
                self.enemy_laser(enemies)

            if enemies.alive and enemies.collision_box().colliderect(self.collision_box()):
                Display.explosion_sound.play()
                self.health -= 1
                self.score -= 1
                self.reset_enemies(enemies, False)
                if self.health <= 0:
                    play_time = (pygame.time.get_ticks() - self.start_time) / 1000 if self.start_time else 0
                    GameOver(self.score, self.health, play_time).execute()

    def enemy_laser(self, enemy: Enemies):
        if len(enemy.bullets_list) < 1 and enemy.alive:
            enemy.firing()
        self.enemy_firing(enemy)

    def enemy_firing(self, enemy: Enemies):
        if enemy.type == 1:
            self.enemy_type1_firing(enemy)
        elif enemy.type == 2:
            self.enemy_type2_firing(enemy)

    def enemy_type1_firing(self, enemy: Enemies):
        for laser in enemy.bullets_list[:]:  # Salin list untuk iterasi
            Display.windows.blit(
                Display.enemy_laser,
                (laser[0] - Display.enemy_spaceship.get_width(), laser[1] + 28),
            )
            collision = pygame.Rect(
                (laser[0] - Display.enemy_spaceship.get_width(), laser[1] + 28),
                (Display.enemy_laser.get_width(), Display.enemy_laser.get_height()),
            )

            if laser[0] + Display.enemy_laser.get_width() <= 0:
                if laser in enemy.bullets_list:
                    enemy.bullets_list.remove(laser)

            self.player_hit(collision)
            laser[0] -= 5

    def enemy_type2_firing(self, enemy: Enemies):
        for missile in enemy.bullets_list[:]:  # Salin list untuk iterasi
            Display.windows.blit(
                Display.missile,
                (missile[0] - 80, missile[1]),
            )
            collision = pygame.Rect(
                (missile[0] - 80, missile[1]),
                (Display.missile.get_width(), Display.missile.get_height()),
            )

            if missile[0] + Display.missile.get_width() <= 0:
                if missile in enemy.bullets_list:
                    enemy.bullets_list.remove(missile)

            self.player_hit(collision)
            missile[0] -= 2

            if missile[0] > Display.windows.get_width() / 2:
                if self.y < missile[1]:
                    missile[1] -= 2
                if self.y > missile[1]:
                    missile[1] += 2

    def player_hit(self, collision: pygame.Rect):
        hit = collision.colliderect(self.collision_box())
        if hit:
            self.health -= 1
            self.score -= 1
            if self.health <= 0:
                play_time = (pygame.time.get_ticks() - self.start_time) / 1000 if self.start_time else 0
                GameOver(self.score, self.health, play_time).execute()


class Start:
    def __init__(self):
        self.object = Objects()
        self.up = False
        self.down = False

    def controls(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.up = True
                if not self.object.game_started:
                    self.object.start_time = pygame.time.get_ticks()
                    self.object.game_started = True
            if event.key == pygame.K_s:
                self.down = True
                if not self.object.game_started:
                    self.object.start_time = pygame.time.get_ticks()
                    self.object.game_started = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.up = False
            if event.key == pygame.K_s:
                self.down = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.object.insert_laser()

    def movements(self):
        if self.up and self.object.y >= 0:
            self.object.y -= 5
        if self.down and self.object.y + Display.spaceship.get_height() <= Display.windows.get_height():
            self.object.y += 5

    def execute(self):
        while True:
            self.object.place_enemies()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                self.controls(event)

            self.movements()
            self.object.objects()
            self.object.add_enemies()

            if self.object.health <= 0 or self.object.score >= 100:
                play_time = (
                                    pygame.time.get_ticks() - self.object.start_time) / 1000 if self.object.start_time else 0
                GameOver(self.object.score, self.object.health, play_time).execute()

            pygame.display.flip()
            Display.clock.tick(60)


# Start the game
Menu().execute()
