import pygame
import random

pygame.init()

# grid settings
grid = 25 # px
screen_width = 30 * grid
screen_height = 20 * grid
refresh_rate = 1 # ms

# character
width = grid
height = grid

win = pygame.display.set_mode((screen_width, screen_height))

alive = True

def decide(x, y): # decide direction
    global length
    global move
    if (length == 1 or move != 'RIGHT') and x >= 0:
        move = random.choice(['LEFT', 'UP', 'DOWN'])
    elif (length == 1 or move != 'LEFT') and x <= screen_width - width:
        move = random.choice(['RIGHT', 'UP', 'DOWN'])
    elif (length == 1 or move != 'UP') and y >= 0:
        move = random.choice(['LEFT', 'RIGHT', 'DOWN'])
    elif (length == 1 or move != 'DOWN') and y <= screen_height - height:
        move = random.choice(['LEFT', 'RIGHT', 'UP'])
    # if keys[pygame.K_LEFT] and x >= 0:
    #     if length == 1 or move != 'RIGHT': # prevent moving into self
    #         move = 'LEFT'
    # if keys[pygame.K_RIGHT] and x <= screen_width - width:
    #     if length == 1 or move != 'LEFT':
    #         move = 'RIGHT'
    # if keys[pygame.K_UP] and y >= 0:
    #     if length == 1 or move != 'DOWN':
    #         move = 'UP'
    # if keys[pygame.K_DOWN] and y <= screen_height - height:
    #     if length == 1 or move != 'UP':
    #         move = 'DOWN'

# main loop
while True:
    x = random.randrange(grid, screen_width - 2*grid, grid) # snake starting coordinates
    y = random.randrange(grid, screen_height - 2*grid, grid)
    x_hist = [0, x]
    y_hist = [0, y]
    move = 'STOP'
    apple_x = random.randrange(grid, screen_width - 2*grid, grid) # apple starting coordinates
    apple_y = random.randrange(grid, screen_height - 2*grid, grid)
    eaten = False
    length = 1

    while alive:
        # determine direction
        decide(x, y)

        if x < 0 or x > screen_width - width or y < 0 or y > screen_height - height: # hit walls
            move = 'STOP'
            alive = False

        if x == apple_x and y == apple_y: # eat apple
            apple_x = random.randrange(grid, screen_width - 2*grid, grid)
            apple_y = random.randrange(grid, screen_height - 2*grid, grid)
            length += 1
            eaten = False # new apple only generated once per collision

        for i in range(0, length):
            if x == x_hist[::-1][1+i] and y == y_hist[::-1][1+i]: # collide with self 
                move = 'STOP'
                alive = False

        if move == 'LEFT':
            x -= grid
            x_hist.append(x)
            y_hist.append(y)
        elif move == 'RIGHT':
            x += grid
            x_hist.append(x)
            y_hist.append(y)
        elif move == 'UP':
            y -= grid
            y_hist.append(y)
            x_hist.append(x)
        elif move == 'DOWN':
            y += grid
            y_hist.append(y)
            x_hist.append(x)
        else:
            break

        win.fill((0,0,0))

        for i in range(0, length):
            pygame.draw.rect(win, (0,255,0), (x_hist[::-1][0+i], y_hist[::-1][0+i], grid, grid)) # draw character

        if eaten is False: # draw apple
            pygame.draw.rect(win, (255,0,0), (apple_x, apple_y, grid, grid))

        pygame.display.update()
        pygame.time.delay(refresh_rate)

    while alive == False:
        print(length)
        alive = True

pygame.quit()