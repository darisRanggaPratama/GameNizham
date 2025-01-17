import pygame
from tkinter import Tk, Label, Button, Scale, HORIZONTAL, filedialog, StringVar
from turtle import Screen, Turtle
import threading
import time

# Initialize pygame mixer
pygame.mixer.init()

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player with Visualizer")

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
        screen = Screen()
        screen.setup(width=800, height=600)
        screen.bgcolor("black")
        screen.tracer(0)

        stars = [self.create_star() for _ in range(20)]

        while self.visual_running:
            for star in stars:
                star.sety(star.ycor() - 5)
                star.setx(star.xcor() - 3)
                if star.ycor() < -300 or star.xcor() < -400:
                    star.hideturtle()
                    star.goto(400, 300)
                    star.showturtle()

            screen.update()
            time.sleep(0.05)

        screen.bye()

    def create_star(self):
        star = Turtle()
        star.shape("circle")
        star.color(self.random_color())
        star.penup()
        star.goto(400, 300)
        return star

    def random_color(self):
        import random
        return random.choice(["red", "blue", "green", "yellow", "purple", "orange"])

if __name__ == "__main__":
    root = Tk()
    player = MP3Player(root)
    root.mainloop()
