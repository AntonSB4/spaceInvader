import pygame
import random

# Git commit

# Initialize the pygame
pygame.init()

#  create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background/space_planets.jpg')

# Title and Icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('icons/spaceship.png')
pygame.display.set_icon(icon)

#  Player
playerImg = pygame.image.load('player/player.png')
playerX = 370
playerY = 480
playerX_change = 0

#  Alien
alienImg = pygame.image.load(random.choice(['alien/alien.png', 'alien/space-ship.png', 'alien/alien2.png']))
alienX = random.randint(0, 800)
alienY = random.randint(50, 50)
alienX_change = 0.3
alienY_change = 20

# Ready - you can't see the bullet on the screen
# Fire - the bullet is currently moving.
bulletImg = pygame.image.load('player/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y):
    screen.blit(alienImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


#  Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    #  Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #  if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            elif event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    # Get the current x coordinate of te spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    #  5 = 5 + 0.1
    #  Checking for boundaries of spaceship so it doesn't out of bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 735

    #  Alien movement
    alienX += alienX_change
    if alienX <= 0:
        alienX_change = 0.3
        alienY += alienY_change
    elif alienX >= 736:
        alienX_change = -0.3
        alienY += alienY_change

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    alien(alienX, alienY)
    pygame.display.update()
