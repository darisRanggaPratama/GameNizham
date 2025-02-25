import pygame
from player import Player
from enemy import Enemy
from projectile import Projectile
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.score = 0
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        
        # Create player
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Enemy spawn timer
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.enemy_spawn_delay = 1000  # Spawn enemy every 1 second

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.player.shoot():
                    bullet = Projectile(self.player.rect.right, 
                                      self.player.rect.centery)
                    self.all_sprites.add(bullet)
                    self.player_bullets.add(bullet)

    def spawn_enemy(self):
        now = pygame.time.get_ticks()
        if now - self.last_enemy_spawn > self.enemy_spawn_delay:
            enemy = Enemy(800, 600)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
            self.last_enemy_spawn = now

    def update(self):
        self.all_sprites.update()
        self.spawn_enemy()
        
        # Check for collisions
        hits = pygame.sprite.groupcollide(self.enemies, self.player_bullets, 
                                        True, True)
        for hit in hits:
            self.score += 10
            
        # Check if player is hit
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if hits:
            self.player.health -= 1
            if self.player.health <= 0:
                self.running = False

    def draw(self):
        self.all_sprites.draw(self.screen)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        health_text = font.render(f'Health: {self.player.health}', True, 
                                (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(health_text, (10, 40))