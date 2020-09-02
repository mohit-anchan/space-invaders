import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
running = True

pygame.display.set_caption("Space Invaders")
favicon = pygame.image.load('images/ufo.png')
pygame.display.set_icon(favicon)

bg_pic = pygame.image.load('images/background.png')

playerImg = pygame.image.load('images/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

num_of_enemies = 9
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(30)

bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 400
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"

score = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    return distance <= 27


while running:
    screen.fill((0, 0, 0))
    screen.blit(bg_pic, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE and bullet_state is "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        if is_collision(enemyX[i], bulletX, enemyY[i], bulletY):
            bullet_state = "ready"
            bulletY = 400
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            score += 1
            print(score)

        enemy(enemyX[i], enemyY[i], i)

    playerX += playerX_change
    player(playerX, playerY)

    # Bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY < -19:
        bullet_state = "ready"
        bulletY = 400

    pygame.display.update()
