import math
import random
import pygame
from pygame import mixer

# Inisialisasi Pygame
pygame.init()
mixer.init()

# Konstanta
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]

# Setup window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MP3 Player dengan Visualisasi Amoeba")
clock = pygame.time.Clock()

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Amoeba:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = []
        self.num_points = 12
        self.radius = 50
        self.time = 0
        self.generate_points()
        
    def generate_points(self):
        self.points = []
        for i in range(self.num_points):
            angle = (2 * math.pi * i) / self.num_points
            r = self.radius + random.randint(-20, 20)
            x = self.x + r * math.cos(angle)
            y = self.y + r * math.sin(angle)
            self.points.append((x, y))
            
    def update(self):
        self.time += 0.05
        for i in range(len(self.points)):
            x, y = self.points[i]
            noise = math.sin(self.time + i) * 10
            self.points[i] = (x + random.randint(-2, 2) + noise,
                            y + random.randint(-2, 2) + noise)
            
    def draw(self, surface):
        if len(self.points) >= 3:
            color = [abs(int(math.sin(self.time + i) * 255)) for i in range(3)]
            pygame.draw.polygon(surface, color, self.points)

class MP3Player:
    def __init__(self):
        self.playing = False
        self.paused = False
        self.current_volume = 0.5
        self.loop = False
        
        # Buttons
        self.play_button = Button(300, 500, 80, 40, "Play", WHITE)
        self.pause_button = Button(390, 500, 80, 40, "Pause", WHITE)
        self.stop_button = Button(480, 500, 80, 40, "Stop", WHITE)
        self.loop_button = Button(570, 500, 80, 40, "Loop", WHITE)
        self.vol_up_button = Button(660, 500, 40, 40, "+", WHITE)
        self.vol_down_button = Button(710, 500, 40, 40, "-", WHITE)
        
        # Progress bar
        self.progress_rect = pygame.Rect(50, 450, 700, 20)
        
        # Amoebas
        self.amoebas = [Amoeba(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        
    def load_music(self, music_file):
        mixer.music.load(music_file)
        mixer.music.set_volume(self.current_volume)
        
    def play_music(self):
        if not self.playing:
            mixer.music.play(-1 if self.loop else 0)
            self.playing = True
            self.paused = False
            
    def pause_music(self):
        if self.playing and not self.paused:
            mixer.music.pause()
            self.paused = True
        elif self.playing and self.paused:
            mixer.music.unpause()
            self.paused = False
            
    def stop_music(self):
        mixer.music.stop()
        self.playing = False
        self.paused = False
        
    def toggle_loop(self):
        self.loop = not self.loop
        if self.playing:
            self.stop_music()
            self.play_music()
            
    def change_volume(self, up=True):
        if up and self.current_volume < 1.0:
            self.current_volume = min(1.0, self.current_volume + 0.1)
        elif not up and self.current_volume > 0.0:
            self.current_volume = max(0.0, self.current_volume - 0.1)
        mixer.music.set_volume(self.current_volume)
        
    def update_amoebas(self):
        if self.playing and not self.paused:
            if random.random() < 0.02 and len(self.amoebas) < 5:
                x = random.randint(100, WINDOW_WIDTH-100)
                y = random.randint(100, WINDOW_HEIGHT-100)
                self.amoebas.append(Amoeba(x, y))
            
            for amoeba in self.amoebas:
                amoeba.update()
                
    def draw(self, surface):
        # Draw amoebas
        for amoeba in self.amoebas:
            amoeba.draw(surface)
            
        # Draw controls
        self.play_button.draw(surface)
        self.pause_button.draw(surface)
        self.stop_button.draw(surface)
        self.loop_button.draw(surface)
        self.vol_up_button.draw(surface)
        self.vol_down_button.draw(surface)
        
        # Draw progress bar
        pygame.draw.rect(surface, WHITE, self.progress_rect, 2)
        if self.playing:
            progress = pygame.Rect(
                self.progress_rect.x,
                self.progress_rect.y,
                self.progress_rect.width * (mixer.music.get_pos() / 1000) / 100,
                self.progress_rect.height
            )
            pygame.draw.rect(surface, WHITE, progress)

def main():
    player = MP3Player()
    
    # Load music file (ganti dengan path file MP3 Anda)
    try:
        player.load_music("music.mp3")
    except:
        print("Error: File musik tidak ditemukan!")
        return
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if player.play_button.is_clicked(pos):
                    player.play_music()
                elif player.pause_button.is_clicked(pos):
                    player.pause_music()
                elif player.stop_button.is_clicked(pos):
                    player.stop_music()
                elif player.loop_button.is_clicked(pos):
                    player.toggle_loop()
                elif player.vol_up_button.is_clicked(pos):
                    player.change_volume(True)
                elif player.vol_down_button.is_clicked(pos):
                    player.change_volume(False)
        
        # Update
        player.update_amoebas()
        
        # Draw
        screen.fill(BLACK)
        player.draw(screen)
        pygame.display.flip()
        
        # Cap framerate
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
