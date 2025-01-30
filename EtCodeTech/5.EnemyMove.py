import pygame as pg
import random

# initialize pygame
pg.init()

# set up the display
width, height = 800, 600
screen = pg.display.set_mode((width, height))
# Window Title
pg.display.set_caption("Battle tank")

# Background Window
background = pg.image.load("OOP/picture/background.jpeg")

# Logo/icon
logo = pg.image.load("OOP/picture/tanker.png")
pg.display.set_icon(logo)

# Change the background color
lightCoral = (240, 128, 128)
screen.fill(lightCoral)


# Image
def tank(xa, ya):
    picture = pg.image.load("OOP/picture/tanker64.png")
    screen.blit(picture, (xa, ya))


# Move the image
x = 300
y = 300
x_point = 0
y_point = 0


# Enemy
class Enemy:
    picture = pg.image.load("OOP/picture/tankers64.png")

    def __init__(self):
        self.x = random.randint(0, width - self.picture.get_width())
        self.y = random.randint(0, height - self.picture.get_height())
        self.pointx = -0.1
        self.pointy = 0

    def move(self):
        self.x += self.pointx
        self.y += self.pointy

    def draw(self):
        screen.blit(self.picture, (self.x, self.y))


enemy_list = []
for i in range(random.randint(5, 20)):
    new_enemy = Enemy()
    enemy_list.append(new_enemy)

runs = True
while runs:
    # Blit the background
    screen.blit(background, (0, 0))
    # Loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            runs = False

        if event.type == pg.KEYDOWN:
            # Load music
            pg.mixer.music.load("motor-move.mp3")
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

    # Background spread
    background = pg.transform.scale(background, (width, height))

    # Move and draw the enemy
    if len(enemy_list) > 0:
        for enemy in enemy_list:
            enemy.move()
            enemy.draw()

    # Display Object
    tank(x, y)

    pg.display.update()

# Quit
pg.quit()
