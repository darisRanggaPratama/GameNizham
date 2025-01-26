import pygame as pg

class GameWindow:
    def __init__(self, width=800, height=600, title="PyGame Window"):
        pg.init()
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        
        self.background_color = (240, 128, 128)  # Light Coral
        self._set_icon()

    def _set_icon(self, icon_path="tanker.png"):
        try:
            icon = pg.image.load(icon_path)
            pg.display.set_icon(icon)
        except FileNotFoundError:
            print(f"Icon file {icon_path} not found.")

    def draw_background(self):
        self.screen.fill(self.background_color)

    def draw_image(self, image_path, position=(200, 200)):
        try:
            image = pg.image.load(image_path)
            self.screen.blit(image, position)
        except FileNotFoundError:
            print(f"Image file {image_path} not found.")

    def update_display(self):
        pg.display.update()
