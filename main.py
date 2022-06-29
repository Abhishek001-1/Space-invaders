# Pygame tutorial
import pygame
import random
import math

from pygame import mixer

# Initialize the pygame
pygame.init()
# init and update are important to include in pygame
# Create the screen
screen = pygame.display.set_mode((800, 600))
# (width,height)

# through writing this our screen will be showing for infinite time
# while True:
#     pass

# Background
background = pygame.image.load("back_img.jpg")

# Background_sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
# Placing player at our desired position
player_img = pygame.image.load('space-invaders.png')
player_x = 370
player_y = 480
playerx_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemyx_change = []
enemyy_change = []

num_of_enemies = 6
# Placing ufo at our desired position
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('spaceship11.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemyx_change.append(0.3)
    enemyy_change.append(40)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bulletx_change = 0
bullety_change = 1
bullet_state = "ready"

# Score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textx = 10
texty = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    # blit is a method ,means to draw on screen
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    # blit is a method ,means to draw on screen
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))
    # x+16 and y+10 because we want that bullet to came from middle of our spaceship


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


# This will run until close button of window is not pressed
running = True
while running:
    # RGB - Red/Green/Blue
    # Changing background screen, 000 -> Black
    # player_x+=0.1
    # player's coordinate will move as per set speed like here it'll move by 0.1 pixel per running of while loop
    screen.fill((0, 0, 0))

    # Background Image
    # we've included background image here becoz we want background image to show till our game is running
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # pygame.QUIT -> that cancel button on top right corner of opened window
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether its right or left
        # pygame.KEYDOWN -> pressing down any key
        if event.type == pygame.KEYDOWN:
            # print("A Keystroke is pressed")
            if event.key == pygame.K_LEFT:
                # print("Left arrow is pressed")
                playerx_change = -0.4
                # spaceship moves leftwards
            if event.key == pygame.K_RIGHT:
                # print("Right arrow is pressed")
                playerx_change = 0.4
                # spaceship moves rightwards
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                # Get the current x coordinate of the spaceship
                bullet_x = player_x
                fire_bullet(player_x, bullet_y)
        # pygame.KEYUP -> releasing pressed key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke has been released")
                playerx_change = 0
                # spaceship stops
    # Checking for boundaries of spaceship ,so it doesn't go out of bounds
    player_x += playerx_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemy_y[i] > 400:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over()
            break

        enemy_x[i] += enemyx_change[i]
        if enemy_x[i] <= 0:
            enemyx_change[i] = 0.3
            enemy_y[i] += enemyy_change[i]
        elif enemy_x[i] >= 736:
            enemyx_change[i] = -0.3
            enemy_y[i] += enemyy_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_val += 1
            # print(score_val)
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullety_change

    player(player_x, player_y)
    show_score(textx, texty)
    pygame.display.update()
