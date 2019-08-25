import pygame
import random
pygame.init()

# grid settings
grid = 25
screen_width = 30 * grid
screen_height = 20 * grid
refresh_rate = 70

win = pygame.display.set_mode((screen_width, screen_height))

# character
width = grid
height = grid
vel = grid # velocity
highscore = 0

def die(length):
    global highscore
    global move
    if move != 'stop':
        if length - 1 > highscore:
            highscore = length - 1
        print('You scored ' + str(length - 1) + '! Your highscore is ' + str(highscore) + '. Press space to play again.')
    move = 'stop'
    alive = False
    return alive

def run_pygame():
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

def eat_apple(eaten):
    global length
    global apple_x
    global apple_y
    if eaten is True:
        apple_x = random.randrange(grid, screen_width - 2*grid, grid)
        apple_y = random.randrange(grid, screen_height - 2*grid, grid)
        length += 1
        pygame.display.set_caption('Snake! Score: ' + str(length - 1) + ' (Highscore: ' + str(highscore) + ')')
        eaten = False # new apple only generated once per collision

def refresh():
    global x
    global y
    if move == 'left':
        x -= vel
        x_hist.append(x)
        y_hist.append(y)
    elif move == 'right':
        x += vel
        x_hist.append(x)
        y_hist.append(y)
    elif move == 'up':
        y -= vel
        y_hist.append(y)
        x_hist.append(x)
    elif move == 'down':
        y += vel
        y_hist.append(y)
        x_hist.append(x)

    win.fill((0,0,0))

    for i in range(0, length):
        pygame.draw.rect(win, (0,255,0), (x_hist[::-1][0+i], y_hist[::-1][0+i], grid, grid)) # draw character

    if eaten is False: # draw apple
        pygame.draw.rect(win, (255,0,0), (apple_x, apple_y, grid, grid))

    pygame.display.update()
    pygame.time.delay(refresh_rate - length + 1)

run = True
alive = True

while run:
    x = random.randrange(grid, screen_width - 2*grid, grid) # starting coordinates
    y = random.randrange(grid, screen_height - 2*grid, grid)
    x_hist = [0, x]
    y_hist = [0, y]
    move = 'stop'
    apple_x = random.randrange(grid, screen_width - 2*grid, grid) # starting apple
    apple_y = random.randrange(grid, screen_height - 2*grid, grid)
    eaten = False
    length = 1
    pygame.display.set_caption('Snake! Score: 0 (Highscore: ' + str(highscore) + ')')

    while alive:
        run_pygame()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x >= 0: # movement
            if length == 1 or move != 'right':
                move = 'left'
        if keys[pygame.K_RIGHT] and x <= screen_width - width:
            if length == 1 or move != 'left':
                move = 'right'
        if keys[pygame.K_UP] and y >= 0:
            if length == 1 or move != 'down':
                move = 'up'
        if keys[pygame.K_DOWN] and y <= screen_height - height:
            if length == 1 or move != 'up':
                move = 'down'

        if x < 0 or x > screen_width - width or y < 0 or y > screen_height - height: # hit walls
            alive = die(length)


        if x == apple_x and y == apple_y: # eat apple
            eat_apple(True)
        else:
            eat_apple(False)

        for i in range(0, length):
            if x == x_hist[::-1][1+i] and y == y_hist[::-1][1+i]:
                alive = die(length)

        refresh()

    while alive is False:
        run_pygame()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            alive = True

pygame.quit()