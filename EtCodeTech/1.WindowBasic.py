import pygame as pg

# initialize pygame
pg.init()

# set up the display
width, height = 800, 600
screen = pg.display.set_mode((width, height))
# Window Title
pg.display.set_caption("Window Basic")

# Change the background color
lightCoral = (240, 128, 128)
screen.fill(lightCoral)

# Colors
ivory = (255, 255, 240)
lavender = (230, 230, 250)
khaki = (240, 230, 140)
indigo = (75, 0, 130)

# Circle position
pointX = 250
pointY = 400
radius = 49
# Circle
pg.draw.circle(screen, lavender, (pointX, pointY), radius)

# Line position
length = 50
lineWidth = 5
# Line
pg.draw.line(screen, indigo, (pointX, pointY - length), (pointX, pointY + length), lineWidth)

runs = True
while runs:
    # Loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            runs = False

    pg.display.update()

# Quit
pg.quit()
