import pygame
import random
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
pygame.display.set_caption("MP3 Player with Lightning Visualizer")

# Font
font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False

    def draw(self, surface):
        color = (self.color[0]+30, self.color[1]+30, self.color[2]+30) if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class LightningVisualizer:
    def __init__(self):
        self.lightning_bolts = []
        
    def create_lightning(self):
        # Create new lightning bolt if there are less than 5 active bolts
        if len(self.lightning_bolts) < 5:
            start_x = random.randint(0, WINDOW_WIDTH)
            points = [(start_x, 0)]
            current_x = start_x
            current_y = 0
            
            while current_y < WINDOW_HEIGHT:
                current_y += random.randint(20, 50)
                current_x += random.randint(-30, 30)
                points.append((current_x, current_y))
                
            self.lightning_bolts.append({
                'points': points,
                'color': random.choice(COLORS),
                'life': 10  # Lightning will exist for 10 frames
            })
    
    def update(self):
        # Update existing lightning bolts
        self.create_lightning()
        self.lightning_bolts = [bolt for bolt in self.lightning_bolts if bolt['life'] > 0]
        for bolt in self.lightning_bolts:
            bolt['life'] -= 1
        
    def draw(self, surface):
        for bolt in self.lightning_bolts:
            points = bolt['points']
            for i in range(len(points) - 1):
                pygame.draw.line(surface, bolt['color'], 
                               points[i], points[i + 1], 3)

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
visualizer = LightningVisualizer()

def main():
    # Initialize game states
    is_playing = False
    is_looping = False
    current_volume = 0.5
    mixer.music.set_volume(current_volume)
    
    try:
        mixer.music.load("music3.mp3")  # Make sure to have an MP3 file named "music.mp3"
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
        
        # Update and draw visualizer if music is playing
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
