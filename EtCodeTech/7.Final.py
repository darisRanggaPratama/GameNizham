import math
import random

import pygame as pg

# initialize pygame
pg.init()

# set up the display
width, height = 800, 600
screen = pg.display.set_mode((width, height))
# Window Title
pg.display.set_caption("Spaceship")
# Logo/icon
icon = pg.image.load("OOP/picture/tanker.png")
pg.display.set_icon(icon)

# Background image
background = pg.image.load("OOP/picture/space3.jpg")
background = pg.transform.scale(background, (width, height))

# Plane Image
jet = pg.image.load("OOP/picture/jet.png")
# Bomb Image
bomb = pg.image.load("OOP/picture/bomb.png")

# FPS
time = pg.time.Clock()

# Score
score = 0

# Font setup
font = pg.font.Font(None, 36)

def showScore(x, y):
    score_number = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_number, (x, y))




# Player
def player(x, y):
    imgPlayer = jet
    screen.blit(imgPlayer, (x, y))


x_player = random.randint(0, width - jet.get_width())
y_player = height - jet.get_height()
x_player_point = 0


# Enemy
def enemy(x, y):
    imgEnemy = bomb
    screen.blit(imgEnemy, (x, y))


x_enemy = random.randint(0, width - bomb.get_width())
y_enemy = random.randint(0, 300 - bomb.get_height())
y_enemy_point = 10

running = True


# Collision
def collision(xPlayer, yPlayer, xEnemy, yEnemy):
    distance = math.sqrt((xPlayer - xEnemy) ** 2 + (yPlayer - yEnemy) ** 2)
    if distance < 20:
        return True
    else:
        return False


# Game Loop
while running:
    # Background
    screen.blit(background, (0, 0))

    # FPS
    time.tick(60)

    # Score
    showScore(10, 10)

    # Loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                x_player_point -= 1
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                x_player_point += 1

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                x_player_point = 0
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                x_player_point = 0

    # Collision
    if collision(x_player, y_player, x_enemy, y_enemy):
        # Display score
        showScore(width // 2 - 50, height // 2 - 50)
        # Delay
        pg.time.delay(3000)
        running = False


    # Movement Player
    x_player += x_player_point

    # Movement Enemy
    y_enemy += y_enemy_point
    if y_enemy >= height - bomb.get_height():
        y_enemy = random.randint(0, 300 - bomb.get_height())
        x_enemy = random.randint(0, width - bomb.get_width())
        score += 1

    # Window Boundaries
    if x_player < 0:
        x_player = 0
    elif x_player >= width - jet.get_width():
        x_player = width - jet.get_width()

    # Player
    player(x_player, y_player)
    # Enemy
    enemy(x_enemy, y_enemy)

    pg.display.update()

pg.quit()
