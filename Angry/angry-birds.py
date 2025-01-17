import pygame
import math
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Angry Birds Clone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# Game parameters
GRAVITY = 0.5
POWER_MULTIPLIER = 0.3

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.velocity_x = 0
        self.velocity_y = 0
        self.launched = False
        self.dragging = False
        self.start_pos = (x, y)
    
    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)
        
    def launch(self, start_pos, end_pos):
        if not self.launched:
            dx = start_pos[0] - end_pos[0]
            dy = start_pos[1] - end_pos[1]
            self.velocity_x = dx * POWER_MULTIPLIER
            self.velocity_y = dy * POWER_MULTIPLIER
            self.launched = True
            
    def update(self):
        if self.launched:
            self.velocity_y += GRAVITY
            self.x += self.velocity_x
            self.y += self.velocity_y
            
            # Simple boundary checking
            if self.y > WINDOW_HEIGHT - self.radius:
                self.y = WINDOW_HEIGHT - self.radius
                self.velocity_y = 0
                self.velocity_x *= 0.8  # Friction
                
            if self.x < self.radius or self.x > WINDOW_WIDTH - self.radius:
                self.velocity_x *= -0.8
                
    def reset(self):
        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
        self.velocity_x = 0
        self.velocity_y = 0
        self.launched = False

class Target:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = True
        
    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, GREEN, self.rect)
            
    def check_collision(self, bird):
        if self.active:
            bird_rect = pygame.Rect(bird.x - bird.radius, bird.y - bird.radius,
                                  bird.radius * 2, bird.radius * 2)
            if self.rect.colliderect(bird_rect):
                self.active = False
                return True
        return False

def main():
    clock = pygame.time.Clock()
    bird = Bird(100, WINDOW_HEIGHT - 100)
    
    # Create targets
    targets = [
        Target(600, WINDOW_HEIGHT - 200, 40, 40),
        Target(650, WINDOW_HEIGHT - 200, 40, 40),
        Target(700, WINDOW_HEIGHT - 200, 40, 40)
    ]
    
    # Slingshot positions
    slingshot_pos = (100, WINDOW_HEIGHT - 100)
    
    running = True
    drag_start = None
    
    while running:
        screen.fill(WHITE)
        
        # Draw ground
        pygame.draw.rect(screen, BROWN, (0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50))
        
        # Draw slingshot
        pygame.draw.line(screen, BROWN, slingshot_pos, 
                        (slingshot_pos[0], WINDOW_HEIGHT - 150), 5)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                
            elif event.type == MOUSEBUTTONDOWN and not bird.launched:
                mouse_pos = pygame.mouse.get_pos()
                bird_rect = pygame.Rect(bird.x - bird.radius, bird.y - bird.radius,
                                      bird.radius * 2, bird.radius * 2)
                if bird_rect.collidepoint(mouse_pos):
                    bird.dragging = True
                    drag_start = mouse_pos
                    
            elif event.type == MOUSEBUTTONUP and bird.dragging:
                bird.dragging = False
                if drag_start:
                    bird.launch(drag_start, pygame.mouse.get_pos())
                    
            elif event.type == KEYDOWN:
                if event.key == K_r:  # Reset game
                    bird.reset()
                    for target in targets:
                        target.active = True
        
        # Update bird position while dragging
        if bird.dragging:
            mouse_pos = pygame.mouse.get_pos()
            max_drag = 100
            dx = mouse_pos[0] - slingshot_pos[0]
            dy = mouse_pos[1] - slingshot_pos[1]
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > max_drag:
                scale = max_drag / distance
                dx *= scale
                dy *= scale
            
            bird.x = slingshot_pos[0] + dx
            bird.y = slingshot_pos[1] + dy
            
            # Draw elastic
            pygame.draw.line(screen, BLACK, slingshot_pos, (bird.x, bird.y), 2)
        
        # Update bird physics
        bird.update()
        
        # Check collisions
        for target in targets:
            target.check_collision(bird)
        
        # Draw everything
        for target in targets:
            target.draw(screen)
        bird.draw(screen)
        
        # Show instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Press 'R' to reset", True, BLACK)
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
