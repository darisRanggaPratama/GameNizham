import pygame as pg
import random
import math

# initialize pygame
pg.init()

# set up the display
width, height = 800, 600
screen = pg.display.set_mode((width, height))
# Window Title
pg.display.set_caption("Window Basic")

# Background Window
background = pg.image.load("OOP/picture/background.jpeg")

# Logo/icon
logo = pg.image.load("OOP/picture/tanker.png")
pg.display.set_icon(logo)

# Change the background color
lightCoral = (240, 128, 128)
screen.fill(lightCoral)


# Player
def tank(xa, ya):
    picture = pg.image.load("OOP/picture/tanker64.png")
    screen.blit(picture, (xa, ya))


# Move the image
x = 300
y = 300
x_point = 0
y_point = 0

# Lives
lives = 3
font = pg.font.Font('freesansbold.ttf', 36)


def show_lives():
    x_lives = 10
    y_lives = 10
    lives_number = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(lives_number, (x_lives, y_lives))


# Enemy
def tanker(xb, yb):
    picture = pg.image.load("OOP/picture/tankers64.png")
    screen.blit(picture, (xb, yb))


# Move the image
xs = random.randint(0, width)
ys = random.randint(0, height)


# x_points = 0
# y_points = 0

# Tabrakan
def collision(x, y, xs, ys):
    distance = math.sqrt((x - xs) ** 2 + (y - ys) ** 2)
    if distance < 50:
        return True
    else:
        return False


runs = True
while runs:
    # Loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            runs = False

        if event.type == pg.KEYDOWN:
            # Load music
            pg.mixer.music.load("motor-move.mp3")
            pg.mixer.music.play(-1)

            if event.key == pg.K_LEFT or event.key == ord("a"):
                x_point -= 1
            elif event.key == pg.K_RIGHT or event.key == ord("d"):
                x_point += 1
            elif event.key == pg.K_UP or event.key == ord("w"):
                y_point -= 1
            elif event.key == pg.K_DOWN or event.key == ord("s"):
                y_point += 1

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

    # Periksa posisi objek
    images = pg.image.load("OOP/picture/tankers64.png")
    xs = max(0, min(xs, width - images.get_width()))
    ys = max(0, min(ys, height - images.get_height()))

    # Clear the screen
    screen.fill(lightCoral)

    # Background spread
    background = pg.transform.scale(background, (width, height))

    # Blit the background
    screen.blit(background, (0, 0))

    # Tabrakan
    if collision(x, y, xs, ys):
        lives -= 1
    else:
        lives += 0

    # Game Over
    if lives <= 0:
        break

    # Lives
    show_lives()

    # Display Object
    tank(x, y)
    tanker(xs, ys)

    pg.display.update()

# Quit
pg.quit()
