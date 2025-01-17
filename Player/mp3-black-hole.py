import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]

# Window setup
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MP3 Player with Black Hole Visualizer")

# Font
font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False

    def draw(self, surface):
        color = (min(255, self.color[0]+30), min(255, self.color[1]+30), min(255, self.color[2]+30)) if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        return event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered

class BlackHoleVisualizer:
    def __init__(self):
        self.center_x = WINDOW_WIDTH // 2
        self.center_y = WINDOW_HEIGHT // 2
        self.max_radius = min(WINDOW_WIDTH, WINDOW_HEIGHT) // 2 - 100
        self.particles = []
        self.timer = 0
        
    def create_particle(self):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(50, self.max_radius)
        speed = random.uniform(1, 3)
        color = random.choice(COLORS)
        brightness = random.randint(100, 255)
        size = random.randint(2, 5)
        
        return {
            'angle': angle,
            'radius': radius,
            'speed': speed,
            'color': color,
            'brightness': brightness,
            'size': size
        }
    
    def update(self):
        self.timer += 1
        
        # Add new particles
        if len(self.particles) < 100:
            self.particles.append(self.create_particle())
            
        # Update existing particles
        for particle in self.particles:
            # Spiral movement
            particle['radius'] -= particle['speed']
            particle['angle'] += 0.05
            particle['brightness'] = max(0, particle['brightness'] - random.uniform(1, 3))
            
        # Remove particles that are too close to center or too dim
        self.particles = [p for p in self.particles if p['radius'] > 20 and p['brightness'] > 0]
        
    def draw(self, surface):
        # Draw black hole center
        pygame.draw.circle(surface, (20, 20, 40), (self.center_x, self.center_y), 30)
        
        # Draw particles
        for particle in self.particles:
            x = self.center_x + particle['radius'] * math.cos(particle['angle'])
            y = self.center_y + particle['radius'] * math.sin(particle['angle'])
            
            color = tuple(min(255, int(c * particle['brightness'] / 255)) 
                         for c in particle['color'])
            
            pygame.draw.circle(surface, color, (int(x), int(y)), particle['size'])
            
            # Draw trail
            trail_length = 10
            for i in range(trail_length):
                trail_x = self.center_x + (particle['radius'] + i * 2) * math.cos(particle['angle'] - i * 0.1)
                trail_y = self.center_y + (particle['radius'] + i * 2) * math.sin(particle['angle'] - i * 0.1)
                trail_color = tuple(max(0, int(c * (particle['brightness'] / 255) * (1 - i/trail_length))) 
                                  for c in particle['color'])
                pygame.draw.circle(surface, trail_color, (int(trail_x), int(trail_y)), max(1, particle['size'] - i))

# Create buttons
play_button = Button(50, 500, 100, 40, "Play", (0, 128, 0))
pause_button = Button(170, 500, 100, 40, "Pause", (128, 128, 0))
stop_button = Button(290, 500, 100, 40, "Stop", (128, 0, 0))
loop_button = Button(410, 500, 100, 40, "Loop", (0, 0, 128))
volume_up = Button(530, 500, 100, 40, "Vol +", (0, 128, 128))
volume_down = Button(650, 500, 100, 40, "Vol -", (128, 0, 128))

# Progress bar
progress_rect = pygame.Rect(50, 450, 700, 10)

# Initialize visualizer
visualizer = BlackHoleVisualizer()

def main():
    # Initialize game states
    is_playing = False
    is_looping = False
    current_volume = 0.5
    mixer.music.set_volume(current_volume)
    
    try:
        mixer.music.load("music.mp3")  # Make sure to have an MP3 file named "music.mp3"
    except:
        print("Please ensure 'music.mp3' exists in the same directory")
        return

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle button events
            if play_button.handle_event(event):
                if not is_playing:
                    mixer.music.play(-1 if is_looping else 0)
                    is_playing = True
                    
            if pause_button.handle_event(event):
                if is_playing:
                    mixer.music.pause()
                    is_playing = False
                else:
                    mixer.music.unpause()
                    is_playing = True
                    
            if stop_button.handle_event(event):
                mixer.music.stop()
                is_playing = False
                
            if loop_button.handle_event(event):
                is_looping = not is_looping
                if is_playing:
                    mixer.music.play(-1 if is_looping else 0)
                    
            if volume_up.handle_event(event):
                current_volume = min(1.0, current_volume + 0.1)
                mixer.music.set_volume(current_volume)
                
            if volume_down.handle_event(event):
                current_volume = max(0.0, current_volume - 0.1)
                mixer.music.set_volume(current_volume)

        # Update screen
        screen.fill(BLACK)
        
        # Update and draw visualizer
        if is_playing:
            visualizer.update()
        visualizer.draw(screen)
        
        # Draw progress bar
        pygame.draw.rect(screen, (64, 64, 64), progress_rect)
        if is_playing:
            progress = mixer.music.get_pos() / 1000  # Convert to seconds
            width = (progress % 60) / 60 * progress_rect.width
            pygame.draw.rect(screen, WHITE, 
                           (progress_rect.x, progress_rect.y, width, progress_rect.height))
        
        # Draw buttons
        play_button.draw(screen)
        pause_button.draw(screen)
        stop_button.draw(screen)
        loop_button.draw(screen)
        volume_up.draw(screen)
        volume_down.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
