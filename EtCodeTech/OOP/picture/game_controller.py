import pygame as pg
from game_window import GameWindow


class GameController:
    def __init__(self):
        self.window = GameWindow()
        self.is_running = True

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    def run(self):
        self.window.draw_background()
        self.window.draw_image("tanker64.png")

        while self.is_running:
            self.handle_events()
            self.window.update_display()

        pg.quit()
