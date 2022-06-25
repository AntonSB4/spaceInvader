import math
import pygame
import random
from pygame import mixer

# Git commit

# Initialize the pygame
pygame.init()

#  create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background/space_planets.jpg')

# Background sound
mixer.music.load('sound/bg_games.mp3')
mixer.music.play(-1)

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
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 8
for i in range(num_of_aliens):
    alienImg.append(pygame.image.load(random.choice(['alien/alien.png', 'alien/space-ship.png',
                                                     'alien/alien2.png'])))
    alienX.append(random.randint(0, 735))
    alienY.append(random.randint(50, 50))
    alienX_change.append(0.3)
    alienY_change.append(20)

# Ready - you can't see the bullet on the screen
# Fire - the bullet is currently moving.
bulletImg = pygame.image.load('player/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

# Score text
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 54)
textX = 10
textY = 10

# Game over text
font_over = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (230, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


# noinspection PyShadowingNames
def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


# noinspection PyShadowingNames
def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


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
                playerX_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7
            elif event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('sound/shot.wav')
                    bullet_sound.play()
                    # Get the current x coordinate of te spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #  Checking for boundaries of spaceship so it doesn't out of bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 735

    #  Alien movement
    for i in range(num_of_aliens):

        # Game over
        if alienY[i] > 440:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 0.3
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.3
            alienY[i] += alienY_change[i]

        # Collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('sound/boom.mp3')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            alienImg[i] = pygame.image.load(random.choice(['alien/alien.png', 'alien/space-ship.png',
                                                           'alien/alien2.png']))
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 50)

        alien(alienX[i], alienY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
