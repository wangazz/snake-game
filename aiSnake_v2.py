import pygame
import random
from tensorflow import keras

pygame.init()

# grid settings
grid = 25 # px
screen_width = 30 * grid
screen_height = 20 * grid
refresh_rate = 70 # ms

# character
width = grid
height = grid

win = pygame.display.set_mode((screen_width, screen_height))

alive = True

# AI setup
model = keras.models.Sequential([
    keras.layers.Dense(6, input_dim = 8, activation = 'relu'),
    keras.layers.Dense(1, activation = 'sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

def decide(x, y): # decide direction
    global length
    global move
    pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x >= 0:
        if length == 1 or move != 'RIGHT': # prevent moving into self
            move = 'LEFT'
    if keys[pygame.K_RIGHT] and x <= screen_width - width:
        if length == 1 or move != 'LEFT':
            move = 'RIGHT'
    if keys[pygame.K_UP] and y >= 0:
        if length == 1 or move != 'DOWN':
            move = 'UP'
    if keys[pygame.K_DOWN] and y <= screen_height - height:
        if length == 1 or move != 'UP':
            move = 'DOWN'

def ai_decide(x, y, apple_x, apple_y):
    x_distance = (apple_x - x) / x # normalised to [-1, 1]
    y_distance = (apple_y - y) / y
    pass

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
        # decide(x, y)
        ai_decide(x, y, apple_x, apple_y)

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
        pygame.time.delay(refresh_rate - length + 1)

    while alive == False:
        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            alive = True

pygame.quit()