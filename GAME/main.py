import pygame
import random
import math
from tensorflow.keras.models import load_model
import numpy as np

pygame.init()

abs1 = 0

font = pygame.font.Font("04B_19.TTF", 25)

player2 = load_model('player2.h5')


def display():
    score1 = font.render(f"Score Of Player1: {player1_score}", True, (254 / 2, 254 / 2, 254 / 2))
    score2 = font.render(f"Score Of Player2: {player2_score}", True, (254 / 2, 254 / 2, 254 / 2))
    score1_rect = score1.get_rect(topleft=(10, 0))
    score2_rect = score2.get_rect(topright=(690, 0))
    screen.blit(score1, score1_rect)
    screen.blit(score2, score2_rect)


pygame.display.set_caption('PONG')
img = pygame.image.load('Image_collection/swords.png')
player_img = pygame.image.load('Image_collection/plate.png')
player_img1 = pygame.image.load('Image_collection/plate.png')
ball = pygame.image.load('Image_collection/ball.png')

player_x1 = 4
player_y1 = 250 - 54

player_x2 = 700 - 5
player_y2 = 250 - 54

ball_x = 700 / 2
ball_y = 250

ball_vel = 10
vel = 10

hitx1 = 1
hity1 = 1

hitx2 = 1
hity2 = 1

player1_dir = 1
player2_dir = 1

pygame.display.set_icon(img)

screen = pygame.display.set_mode((700, 500))


def movement():
    court = random.choice(("left", "right"))
    angle1 = random.randint(1, 10)
    if angle1 == 8 or angle1 == 5:
        angle1 = random.choice((3, 2, 6))
    return court, angle1


court, angle = movement()
if court == 'left':
    coeff = -1
else:
    coeff = 1

running1 = ''

x = False

player1_score = 0
player2_score = 0

key1 = [[[0.5]]]

while True:
    player1_rect = player_img.get_rect(topleft=(player_x1, player_y1))
    player2_rect = player_img1.get_rect(topleft=(player_x2, player_y2))
    ball_rect = ball.get_rect(topleft=(ball_x, ball_y))

    ball_x += ball_vel * math.cos(angle) * coeff * hitx1 * hitx2
    ball_y += ball_vel * math.sin(angle) * coeff * hity1 * hity2

    screen.fill((0, 0, 0))

    screen.blit(player_img, player1_rect)
    screen.blit(player_img, player2_rect)
    screen.blit(ball, ball_rect)
    display()

    pygame.time.delay(20)

    distance_player1 = ((player_x1 - ball_x) ** 2 + (player_y1 - ball_y) ** 2) ** 1 / 2
    distance_player2 = ((player_x2 - ball_x) ** 2 + (player_y2 - ball_y) ** 2) ** 1 / 2

    player_1_train = np.reshape(np.array([[[distance_player1 / (700 ** 2 + 500 ** 2) ** 1 / 2],
                                           [distance_player2 / (700 ** 2 + 500 ** 2) ** 1 / 2], [ball_y / 500],
                                           [(player_y1) / 500]]]), newshape=(1, 1, 4))
    player_2_train = np.reshape(np.array([[[distance_player2 / (700 ** 2 + 500 ** 2) ** 1 / 2],
                                           [distance_player1 / (700 ** 2 + 500 ** 2) ** 1 / 2], [ball_y / 500],
                                           [(player_y2) / 500]]]), newshape=(1, 1, 4))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running1 = 'qwerty'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                key1 = [[[0]]]
            if event.key == pygame.K_DOWN:
                key1 = [[[1]]]
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                key1 = [[[0.5]]]
            if event.key == pygame.K_DOWN:
                key1 = [[[0.5]]]


    key2 = player2.predict(player_2_train)

    if key1[0][0][0] < 0.5 and player_y1 + 10> vel:
        player_y1 = player_y1 - vel

    elif key1[0][0][0] > 0.5 and player_y1 < 500 - 110 - vel:
        player_y1 = player_y1 + vel

    if key2[0][0][0] < 0.5 and player_y2 + 10> vel:
        player_y2 -= vel
    elif key2[0][0][0] > 0.5 and player_y2 < 500 - 110 - vel:
        player_y2 += vel

    if ball_y < ball_vel:
        if hity1 == -1:
            hity1 = 1
        else:
            hity1 = -1
    elif ball_y > 500 - 5:
        if hity2 == -1:
            hity2 = 1
        else:
            hity2 = -1

    if player1_rect.colliderect(ball_rect) == 1:
        hitx1 = -1 * hitx1
        ball_x += ball_vel * math.cos(angle) * coeff * hitx1 * hitx2 * 2
        ball_y += ball_vel * math.sin(angle) * coeff * hity1 * hity2 * 2
        ball_vel += 0.1

    elif player2_rect.colliderect(ball_rect) == 1:
        hitx2 = -1 * hitx2
        ball_x += ball_vel * math.cos(angle) * coeff * hitx1 * hitx2 * 2
        ball_y += ball_vel * math.sin(angle) * coeff * hity1 * hity2 * 2
        ball_vel += 0.1

    if ball_x <= -20:
        player2_score += 1
        ball_x = 700 / 2
        ball_y = 250
        ball_vel = 10
        court, angle = movement()


    elif ball_x >= 720:
        player1_score += 1
        ball_x = 700 / 2
        ball_y = 250
        ball_vel = 10
        court, angle = movement()

    if running1 == 'qwerty':
        break

    pygame.display.update()

pygame.quit()
