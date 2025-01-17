import pygame
import random
import math
from enum import Enum

# Inisialisasi Pygame
pygame.init()

# Konstanta
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class ShapeType(Enum):
    SQUARE = 1
    CIRCLE = 2
    PENTAGON = 3
    OCTAGON = 4

class GameObject:
    def __init__(self, x, y, shape_type=None, is_player=False):
        self.x = x
        self.y = y
        self.speed = 3
        self.size = 20
        self.shape_type = shape_type
        self.is_player = is_player
        self.health = 100
        self.bullets = []
        self.shoot_delay = 0
        
    def draw(self, screen):
        if self.is_player:
            # Gambar segitiga pemain
            points = [
                (self.x, self.y - self.size),
                (self.x - self.size, self.y + self.size),
                (self.x + self.size, self.y + self.size)
            ]
            pygame.draw.polygon(screen, RED, points)
        else:
            if self.shape_type == ShapeType.SQUARE:
                pygame.draw.rect(screen, BLUE, 
                               (self.x - self.size, self.y - self.size, 
                                self.size * 2, self.size * 2))
            elif self.shape_type == ShapeType.CIRCLE:
                pygame.draw.circle(screen, GREEN, (self.x, self.y), self.size)
            elif self.shape_type == ShapeType.PENTAGON:
                points = []
                for i in range(5):
                    angle = math.radians(i * 72 - 18)
                    points.append((
                        self.x + self.size * math.cos(angle),
                        self.y + self.size * math.sin(angle)
                    ))
                pygame.draw.polygon(screen, YELLOW, points)
            elif self.shape_type == ShapeType.OCTAGON:
                points = []
                for i in range(8):
                    angle = math.radians(i * 45)
                    points.append((
                        self.x + self.size * math.cos(angle),
                        self.y + self.size * math.sin(angle)
                    ))
                pygame.draw.polygon(screen, WHITE, points)

    def shoot(self, target_x, target_y):
        if self.shoot_delay <= 0:
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 0:
                dx = dx / distance * 7
                dy = dy / distance * 7
                self.bullets.append([self.x, self.y, dx, dy])
            self.shoot_delay = 20
        
    def update(self):
        self.shoot_delay -= 1
        # Update posisi peluru
        for bullet in self.bullets[:]:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            if (bullet[0] < 0 or bullet[0] > SCREEN_WIDTH or
                bullet[1] < 0 or bullet[1] > SCREEN_HEIGHT):
                self.bullets.remove(bullet)

    def draw_bullets(self, screen):
        for bullet in self.bullets:
            pygame.draw.circle(screen, RED if self.is_player else BLUE, 
                             (int(bullet[0]), int(bullet[1])), 3)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Triangle Shooter")
        self.clock = pygame.time.Clock()
        self.player = GameObject(SCREEN_WIDTH//2, SCREEN_HEIGHT-50, is_player=True)
        self.enemies = []
        self.score = 0
        self.spawn_timer = 0
        self.game_over = False
        
    def spawn_enemy(self):
        if len(self.enemies) < 5 and self.spawn_timer <= 0:
            x = random.randint(50, SCREEN_WIDTH-50)
            y = random.randint(50, SCREEN_HEIGHT//2)
            shape_type = random.choice(list(ShapeType))
            self.enemies.append(GameObject(x, y, shape_type))
            self.spawn_timer = 60

    def check_collisions(self):
        # Cek collision peluru player dengan musuh
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                distance = math.sqrt(
                    (bullet[0] - enemy.x)**2 + 
                    (bullet[1] - enemy.y)**2
                )
                if distance < enemy.size:
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 1
                    break

        # Cek collision peluru musuh dengan player
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                distance = math.sqrt(
                    (bullet[0] - self.player.x)**2 + 
                    (bullet[1] - self.player.y)**2
                )
                if distance < self.player.size:
                    if bullet in enemy.bullets:
                        enemy.bullets.remove(bullet)
                    self.player.health -= 10
                    if self.player.health <= 0:
                        self.game_over = True

    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    mx, my = pygame.mouse.get_pos()
                    self.player.shoot(mx, my)

            if not self.game_over:
                # Update
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and self.player.x > self.player.size:
                    self.player.x -= self.player.speed
                if keys[pygame.K_RIGHT] and self.player.x < SCREEN_WIDTH - self.player.size:
                    self.player.x += self.player.speed

                self.spawn_timer -= 1
                self.spawn_enemy()
                
                self.player.update()
                for enemy in self.enemies:
                    enemy.update()
                    if random.random() < 0.02:  # 2% chance to shoot each frame
                        enemy.shoot(self.player.x, self.player.y)
                
                self.check_collisions()

                # Check win condition
                if self.score >= 50:
                    self.game_over = True

            # Draw
            self.screen.fill(BLACK)
            
            # Draw game objects
            self.player.draw(self.screen)
            self.player.draw_bullets(self.screen)
            
            for enemy in self.enemies:
                enemy.draw(self.screen)
                enemy.draw_bullets(self.screen)

            # Draw UI
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}/50", True, WHITE)
            health_text = font.render(f"Health: {self.player.health}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(health_text, (10, 50))

            if self.game_over:
                game_over_text = font.render(
                    "YOU WIN!" if self.score >= 50 else "GAME OVER", 
                    True, WHITE
                )
                self.screen.blit(game_over_text, 
                    (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                     SCREEN_HEIGHT//2)
                )

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
