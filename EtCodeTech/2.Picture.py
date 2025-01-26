import pygame as pg

# initialize pygame
pg.init()

# set up the display
width, height = 800, 600
screen = pg.display.set_mode((width, height))
# Window Title
pg.display.set_caption("Window Basic")

# Logo/icon
icon = pg.image.load("OOP/picture/tanker.png")
pg.display.set_icon(icon)

# Change the background color
lightCoral = (240, 128, 128)
screen.fill(lightCoral)

# Image
image = pg.image.load("OOP/picture/tanker64.png")
screen.blit(image, (200, 200))

runs = True
while runs:
    # Loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            runs = False

    pg.display.update()

# Quit
pg.quit()
