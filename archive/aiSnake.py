import pygame
import random
import numpy as np
import tensorflow as tf

# VARIABLE DECLARATION #
#
# grid settings
grid = 25
screen_width = 30 * grid
screen_height = 20 * grid
refresh_rate = 100
pygame.init()
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake! Score: 0')
#
# start of game settings

#
# END VARIABLE DECLARATION #

class nn:
    def __init__(self):
        pass

def run_pygame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

def eat_apple(eaten):
    global length
    if eaten is True:
        new_apple_x = random.randrange(grid, screen_width - 2*grid, grid)
        new_apple_y = random.randrange(grid, screen_height - 2*grid, grid)
        length += 1
        pygame.display.set_caption('Snake! Score: ' + str(length - 1))
        eaten = False # new apple only generated once per collision
        return (new_apple_x, new_apple_y)

def move_snake(move, length):
    global position
    x = position[::-1][0][0]
    y = position[::-1][0][1]
    if move == 'left' and (move != 'right' or length == 1):
        x -= grid
        position.append((x, y))
    elif move == 'right' and (move != 'left' or length == 1):
        x += grid
        position.append((x, y))
    elif move == 'up' and (move != 'down' or length == 1):
        y -= grid
        position.append((x, y))
    elif move == 'down' and (move != 'up' or length == 1):
        y += grid
        position.append((x, y))

def refresh(eaten, apple):
    global position
    global length
    win.fill((0,0,0))
    for i in range(0, length):
        pygame.draw.rect(win, (0,255,0), (position[::-1][0+i][0], position[::-1][0+i][1], grid, grid)) # draw character

    if eaten is False: # draw apple
        pygame.draw.rect(win, (255,0,0), (apple[0], apple[1], grid, grid))

    pygame.display.update()
    pygame.time.delay(refresh_rate)

def run_game():
    global position
    global length
    length = 1
    highscore = 0
    generations = 0
    # life = 0
    # last_life = 0
    # last_length = 1
    position = [(random.randrange(grid, screen_width - 2*grid, grid), random.randrange(grid, screen_height - 2*grid, grid))] # starting position
    apple = (random.randrange(grid, screen_width - 2*grid, grid), random.randrange(grid, screen_height - 2*grid, grid)) # starting apple
    move = 'stop'
    hide_apple = False
    alive = True
    
    while alive:
        alive = run_pygame()

        x = position[::-1][0][0]
        y = position[::-1][0][1]

        if x < 0 or x > screen_width - grid or y < 0 or y > screen_height - grid: # hit walls
            alive = False

        if x == apple[0] and y == apple[1]: # eat apple
            apple = eat_apple(True) # create new apple
            hide_apple = True
        else:
            eat_apple(False)
            hide_apple = False

        # for i in range(0, length): # eat self
        #     if x == x_hist[::-1][1+i] and y == y_hist[::-1][1+i]:
        #         alive = False

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     alive = False # manual override

        # life += 1

        move_snake(move, length)
        refresh(hide_apple, apple)

    print('Score: ' + str(length - 1) + '. Generation: ' + str(generations) + '. Highscore: ' + str(highscore) + '.')
    generations += 1
    # last_length = length
    if length - 1 > highscore:
        highscore = length - 1
    # last_life = life
    alive = True

run = True

while run:
    run_game()

    # nn.create_training_data()
    # nn.train()
    # nn.run()

pygame.quit()