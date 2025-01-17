import pygame
import tkinter as tk
from tkinter import ttk
import turtle
import threading
import time
import math

# Initialize pygame mixer
pygame.mixer.init()

# Create the main app window
root = tk.Tk()
root.title("MP3 Player with Visualizer")
root.geometry("600x400")

# Load music file (Change 'your_music.mp3' to your actual MP3 file)
music_file = "music.mp3"
pygame.mixer.music.load(music_file)

# Global state
is_playing = False
is_looping = False
volume = 0.5  # Initial volume


# Initialize Turtle for visualizer
def setup_turtle_visualizer():
    screen = turtle.Screen()
    screen.setup(width=600, height=400)
    screen.bgcolor("black")
    screen.title("Music Visualizer")
    return screen


def draw_heartbeat():
    t = turtle.Turtle()
    t.hideturtle()
    t.color("red")
    t.width(2)
    t.speed(0)

    # Infinite animation loop
    while is_playing:
        t.clear()
        t.penup()
        t.goto(-300, 0)
        t.pendown()
        for x in range(-300, 301, 5):
            y = 50 * math.sin(0.02 * x) if -100 <= x <= 100 else 20 * math.sin(0.05 * x)
            t.goto(x, y)
        time.sleep(0.1)


# Start the visualizer in a separate thread
def start_visualizer():
    screen = setup_turtle_visualizer()
    visualizer_thread = threading.Thread(target=draw_heartbeat, daemon=True)
    visualizer_thread.start()


# Control functions
def play_music():
    global is_playing
    is_playing = True
    pygame.mixer.music.play(loops=-1 if is_looping else 0)
    threading.Thread(target=start_visualizer, daemon=True).start()


def pause_music():
    global is_playing
    is_playing = False
    pygame.mixer.music.pause()


def stop_music():
    global is_playing
    is_playing = False
    pygame.mixer.music.stop()


def toggle_loop():
    global is_looping
    is_looping = not is_looping


def adjust_volume(val):
    global volume
    volume = float(val)
    pygame.mixer.music.set_volume(volume)


# Progress bar updater
def update_progress():
    while is_playing:
        time.sleep(1)
        current_time = pygame.mixer.music.get_pos() / 1000
        progress.set(current_time)


# UI Components
play_button = tk.Button(root, text="Play", command=play_music)
play_button.pack(pady=10)

pause_button = tk.Button(root, text="Pause", command=pause_music)
pause_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_music)
stop_button.pack(pady=10)

loop_button = tk.Button(root, text="Loop", command=toggle_loop)
loop_button.pack(pady=10)

volume_slider = ttk.Scale(root, from_=0, to=1, orient="horizontal", command=adjust_volume)
volume_slider.set(volume)
volume_slider.pack(pady=10)

progress = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress, maximum=100)
progress_bar.pack(pady=10)

# Run the Tkinter mainloop
root.mainloop()
