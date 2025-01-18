import pygame

# init
pygame.init()
# Variable running game

# Create display surface object
winHeight = 600
winWidth = 600
window = pygame.display.set_mode((winWidth, winHeight))

# Object game
# Position
x = 300
y = 300

# Size
heigt = 20
width = 20

# Speed
speed = 1

# User input
while True:
    # Delay
    pygame.time.delay(10)

    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Input Keyboard
    keys = pygame.key.get_pressed()
    # Left
    if keys[pygame.K_LEFT] and x > 0:
        x -= speed
    # Right
    if keys[pygame.K_RIGHT] and x < winWidth - width:
        x += speed
    # Down
    if keys[pygame.K_DOWN] and y < winHeight - heigt:
        y += speed
    # Up
    if keys[pygame.K_UP] and y > 0:
        y -= speed

    # Update Asset
    window.fill((255, 255, 255))
    pygame.draw.rect(window, (255, 0, 120), (x, y, heigt, width))
    # Render display
    pygame.display.update()
