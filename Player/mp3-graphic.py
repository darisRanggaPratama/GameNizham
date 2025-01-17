import pygame
from tkinter import Tk, Label, Button, Scale, HORIZONTAL, filedialog, StringVar
import threading
import time
import math

# Initialize pygame mixer
pygame.mixer.init()

class MP3PlayerWithVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player with Waveform Visualizer")

        # Variable initialization
        self.current_file = None
        self.playing = False
        self.loop = False

        # GUI Elements
        self.label = Label(root, text="No file selected", font=("Arial", 14))
        self.label.pack(pady=10)

        self.play_button = Button(root, text="Play", command=self.play)
        self.play_button.pack(pady=5)

        self.pause_button = Button(root, text="Pause", command=self.pause)
        self.pause_button.pack(pady=5)

        self.stop_button = Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(pady=5)

        self.loop_button = Button(root, text="Loop", command=self.toggle_loop)
        self.loop_button.pack(pady=5)

        self.volume_scale = Scale(root, from_=0, to=1, resolution=0.1, orient=HORIZONTAL, label="Volume", command=self.set_volume)
        self.volume_scale.set(0.5)
        self.volume_scale.pack(pady=5)

        self.progress_label = Label(root, text="Progress: 0:00 / 0:00")
        self.progress_label.pack(pady=5)

        self.progress_bar = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=300)
        self.progress_bar.pack(pady=10)

        self.file_button = Button(root, text="Select File", command=self.select_file)
        self.file_button.pack(pady=5)

        # Visualization thread
        self.visual_thread = threading.Thread(target=self.visualizer, daemon=True)
        self.visual_running = False

    def select_file(self):
        self.current_file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if self.current_file:
            self.label.config(text=f"Selected: {self.current_file.split('/')[-1]}")

    def play(self):
        if not self.current_file:
            self.label.config(text="No file selected")
            return

        if not self.playing:
            pygame.mixer.music.load(self.current_file)
            pygame.mixer.music.play(loops=-1 if self.loop else 0)
            self.playing = True
            self.visual_running = True

            if not self.visual_thread.is_alive():
                self.visual_thread = threading.Thread(target=self.visualizer, daemon=True)
                self.visual_thread.start()

        self.update_progress()

    def pause(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.visual_running = False

    def toggle_loop(self):
        self.loop = not self.loop
        self.loop_button.config(text="Loop: ON" if self.loop else "Loop: OFF")

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def update_progress(self):
        while self.playing:
            if pygame.mixer.music.get_busy():
                position = pygame.mixer.music.get_pos() // 1000
                minutes, seconds = divmod(position, 60)
                self.progress_label.config(text=f"Progress: {minutes}:{seconds:02d}")
                time.sleep(1)

    def visualizer(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Waveform Visualizer")

        clock = pygame.time.Clock()
        amplitude = 100
        frequency = 0.1
        phase = 0

        while self.visual_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.visual_running = False

            screen.fill((0, 0, 0))

            # Draw waveform
            for x in range(0, 800):
                y = 200 + amplitude * math.sin(frequency * x + phase)
                color = (255, 0, 0) if x % 20 < 10 else (0, 0, 255)
                pygame.draw.line(screen, color, (x, 200), (x, y), 2)

            phase += 0.1
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    root = Tk()
    player = MP3PlayerWithVisualizer(root)
    root.mainloop()
