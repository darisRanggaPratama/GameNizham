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
def tank(x, y):
    image = pg.image.load("OOP/picture/tanker64.png")
    screen.blit(image, (x, y))



# Move the image
x = 300
y = 300
x_point = 0
y_point = 0

runs = True
while runs:
    # Loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            runs = False

        if event.type == pg.KEYDOWN:
            # Load music
            pg.mixer.music.load("tank-move.mp3")
            pg.mixer.music.play(-1)

            if event.key == pg.K_LEFT or event.key == ord("a"):
                x_point -= 0.1
            elif event.key == pg.K_RIGHT or event.key == ord("d"):
                x_point += 0.1
            elif event.key == pg.K_UP or event.key == ord("w"):
                y_point -= 0.1
            elif event.key == pg.K_DOWN or event.key == ord("s"):
                y_point += 0.1

        if event.type == pg.KEYUP:
            # Load music
            pg.mixer.music.load("cat.mp3")
            pg.mixer.music.play(-1)

            if event.key == pg.K_LEFT or event.key == ord("a"):
                x_point = 0
            elif event.key == pg.K_RIGHT or event.key == ord("d"):
                x_point = 0
            elif event.key == pg.K_UP or event.key == ord("w"):
                y_point = 0
            elif event.key == pg.K_DOWN or event.key == ord("s"):
                y_point = 0

    # Move the image
    x += x_point
    y += y_point

    # Periksa posisi objek
    image = pg.image.load("OOP/picture/tanker64.png")
    x = max(0, min(x, width - image.get_width()))
    y = max(0, min(y, height - image.get_height()))

    tank(x, y)

    # Clear the screen
    screen.fill(lightCoral)

    # Blit the image
    screen.blit(image, (x, y))

    pg.display.update()

# Quit
pg.quit()
