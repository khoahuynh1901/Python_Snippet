import pygame
import random
import math
from pygame import mixer

# initializing the game
pygame.init()
# Create window screen for game
screen = pygame.display.set_mode((800, 600))
# Background creation
background = pygame.image.load("bg.png")
# background sound
mixer.music.load("backgound.wav")
mixer.music.play(-1)
# Titile of the game
pygame.display.set_caption("The Invaders")
icon = pygame.image.load("Spaceship.png")
pygame.display.set_icon(icon)
# Player
Player_Im = pygame.image.load("UserSpaceship.png")
playerX = 370
playerY = 480
PlayerX_change = 0
# Create enemies
Enemy_Im = []
EX = []
EY = []
EX_change = []
EY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    Enemy_Im.append(pygame.image.load("Monster.png"))
    EX.append(random.randint(0, 735))
    EY.append(random.randint(50, 150))
    EX_change.append(0.4)
    EY_change.append(10)
# Create bullet for spaceship
bull_Im = pygame.image.load("bullit.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4.5
bullet_state = "ready"
# Font
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 22)
textX = 10
textY = 10
# Game over text
over_font = pygame.font.Font("freesansbold.ttf", 62)


def appear_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over():
    text_over = over_font.render("Game Over", True, (0, 255, 255))
    screen.blit(text_over, (250, 400))

def player(x, y):
    screen.blit(Player_Im, (x, y))

def enemy(x, y, i):
    screen.blit(Enemy_Im[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bull_Im, (x + 16, y + 10))

def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2))
    if distance < 27:
        return True
    else:
        return False

# Game loop to build inside the screen
running = True
while True:
    screen.fill((0, 0, 0))
    # bg image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if key stroked is pressed to check whether go right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -1
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # Get the current X coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0
    # Movement of userSpaceship
    playerX += PlayerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    # Movement of Enemies
    for i in range(num_of_enemies):
        # Game over the end of game
        if EY[i] > 440:
            for j in range(num_of_enemies):
                EY[j] = 2000
            game_over()
            break
        EX[i] += EX_change[i]
        if EX[i] <= 0:
            EX_change[i] = 0.4
            EY[i] += EY_change[i]
        elif EX[i] >= 736:
            EX_change[i] = -0.4
            EY[i] += EY_change[i]
        # isCollision
        collision = isCollision(EX[i], EY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosionsound.wav")
            explosion_sound.play()
            bulletY = 400
            bullet_state = "ready"
            score_value += 1
            EX[i] = random.randint(0, 635)
            EY[i] = random.randint(50, 150)
        enemy(EX[i], EY[i], i)
    # Movement of bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    appear_score(textX, textY)
    pygame.display.update()
