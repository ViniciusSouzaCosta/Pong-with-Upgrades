import pygame
import random
from ball import ball, ball_x, ball_y, ball_dx, ball_dy
from padds import player_1, player_1_y, player_1_move_up, player_1_move_down, player_2, player_2_y, player_2_dy

pygame.init()

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

SCORE_MAX = 4

size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MyPong - PyGame Edition - 2022-12-12")

# score text
score_font = pygame.font.Font('assets/PressStart2P-vaV7.ttf', 44)
score_text = score_font.render('00   00', True, COLOR_WHITE, COLOR_BLACK)
score_text_rect = score_text.get_rect()
score_text_rect.center = (680, 50)

# middle line

# victory text
victory_font = pygame.font.Font('assets/PressStart2P-vaV7.ttf', 100)
victory_text = victory_font .render('VICTORY', True, COLOR_WHITE, COLOR_BLACK)
victory_text_rect = score_text.get_rect()
victory_text_rect.center = (450, 350)

# defeat text
defeat_font = pygame.font.Font('assets/PressStart2P-vaV7.ttf', 100)
defeat_text = defeat_font .render('DEFEAT', True, COLOR_WHITE, COLOR_BLACK)
defeat_text_rect = score_text.get_rect()
defeat_text_rect.center = (450, 350)

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav')

# score
score_1 = 0
score_2 = 0

check = 0

# game loop
game_loop = True
game_clock = pygame.time.Clock()

while game_loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        #  keystroke events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_1_move_up = True
            if event.key == pygame.K_DOWN:
                player_1_move_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_1_move_up = False
            if event.key == pygame.K_DOWN:
                player_1_move_down = False

    # checking the victory condition
    if score_1 < SCORE_MAX and score_2 < SCORE_MAX:

        # clear screen
        screen.fill(COLOR_BLACK)

        # ball collision with the wall
        if ball_y > 700:
            ball_dy *= -1
            bounce_sound_effect.play()
        elif ball_y <= 0:
            ball_dy *= -1
            bounce_sound_effect.play()
        # exponential speed increase after each paddle collision
        # ball collision with the player 1 's paddle
        if 100 <= ball_x <= 101:  # bugfix paddle sides colliders
            if player_1_y < ball_y + 20:
                if player_1_y + 150 > ball_y:
                    ball_dx *= -1.5
                    check = random.randint(0,1)
                    bounce_sound_effect.play()
        # ball collision with the player 1 's above and under
        if 50 <= ball_x < 100:
            if ball_y + 20 >= player_1_y >= ball_y:

                ball_dy *= -1
                ball_y = player_1_y - 21
                ball_dx *= -1
                check = random.randint(0, 1)
                bounce_sound_effect.play()

            elif player_1_y + 150 >= ball_y and player_1_y <= ball_y + 20:
                ball_dy *= -1
                ball_y = player_1_y + 151
                ball_dx *= -1
                check = random.randint(0, 1)
                bounce_sound_effect.play()

        # ball collision with the player 2 's paddle
        if ball_x == 1180:  # bugfix paddle sides collider
            if player_2_y < ball_y + 20:
                if player_2_y + 150 > ball_y:
                    ball_dx *= -1
                    check = 0
                    bounce_sound_effect.play()

        if ball_x + 20 >= 1180 and ball_x <= 1130:  # bugfix under and above paddle collider
            if player_1_y + 150 <= ball_y or player_1_y > ball_y + 20:
                ball_dx *= -1
                ball_dy *= random.randint(-1, 1) * abs(ball_dy)
                check = 0
                bounce_sound_effect.play()
        # ball speed halved after each score
        # scoring points
        if ball_x < 0:
            ball_x = 640
            ball_y = 360
            ball_dy = 5
            ball_dx = 5
            score_2 += 1
            scoring_sound_effect.play()
        elif ball_x > 1280:
            ball_x = 640
            ball_y = 360
            ball_dy = -5
            ball_dx = -5
            score_1 += 1
            scoring_sound_effect.play()

        # ball movement
        ball_x = ball_x + ball_dx
        ball_y = ball_y + ball_dy
        # increased player 1 overall speed
        # player 1 up movement
        if player_1_move_up:
            player_1_y -= 10
        else:
            player_1_y += 0

        # player 1 down movement
        if player_1_move_down:
            player_1_y += 10
        else:
            player_1_y += 0

        # player 1 collides with upper wall
        if player_1_y <= 0:
            player_1_y = 0

        # player 1 collides with lower wall
        elif player_1_y >= 570:
            player_1_y = 570

        # player 1 collides with upper wall
        if player_2_y <= 0:
            player_2_y = 0

        # player 1 collides with lower wall
        elif player_2_y >= 570:
            player_2_y = 570

        # player 2 "Artificial Intelligence"
        if check > 0:
            if ball_dy > 0 or ball_dy < 0 or ball_dy == 0:
                player_2_y += player_2_dy
                if player_2_y + 150 == 720:
                    player_2_dy *= -1
                if player_2_y == 100:
                    player_2_dy *= -1

        elif check == 0:
            if player_2_y >= ball_y or player_2_y + 75 >= ball_y + 20 <= player_2_y:
                player_2_y -= 5
            elif player_2_y + 150 <= ball_y + 20 or player_2_y + 75 <= ball_y <= player_2_y + 150:
                player_2_y += 5

        # update score hud
        score_text = score_font.render(str(score_1) + '   ' + str(score_2), True, COLOR_WHITE, COLOR_BLACK)

        # drawing objects
        screen.blit(ball, (ball_x, ball_y))
        screen.blit(player_1, (50, player_1_y))
        screen.blit(player_2, (1180, player_2_y))
        screen.blit(score_text, score_text_rect)
        pygame.draw.aaline(screen, COLOR_WHITE, (1280/2,0), (1280 / 2,720))
    else:
        if score_1 == SCORE_MAX:
            # drawing victory
            screen.fill(COLOR_BLACK)
            screen.blit(score_text, score_text_rect)
            screen.blit(victory_text, victory_text_rect)
        if score_2 == SCORE_MAX:
            # drawing defeat
            screen.fill(COLOR_BLACK)
            screen.blit(score_text, score_text_rect)
            screen.blit(defeat_text, defeat_text_rect)
    # update screen
    pygame.display.flip()
    game_clock.tick(120)

pygame.quit()

