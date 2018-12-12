import pygame
import random
import numpy as np
pygame.init()

# grid settings
grid = 25
screen_width = 30 * grid
screen_height = 20 * grid
refresh_rate = 5

win = pygame.display.set_mode((screen_width, screen_height))

# character
width = grid
height = grid
vel = grid 
highscore = 0 
# W = 2*np.random.rand(8,4) - 1 
W = np.array([[0.0,0,0,0], # weights matrix (floats)
              [0,0,0,0],
              [0,0,0,0], 
              [0,0,0,0], 
              [0,0,0,0], 
              [0,0,0,0], 
              [0,0,0,0], 
              [0,0,0,0]])

class nn:
    def __init__(self, x, y, apple_x, apple_y, move):
        self.x = x
        self.y = y
        self.apple_x = apple_x
        self.apple_y = apple_y
        self.move = move
    
    @staticmethod
    def decide(apple_x, apple_y, wall_x, wall_y, move, bias, generation):
        global W
        if move == 'left':
            left = 1
            right = 0
            up = 0
            down = 0
        elif move == 'right':
            left = 0
            right = 1
            up = 0
            down = 0
        elif move == 'up':
            left = 0
            right = 0
            up = 1
            down = 0
        elif move == 'down':
            left = 0
            right = 0
            up = 0
            down = 1
        else:
            left = 0
            right = 0
            up = 0
            down = 0
        input = np.array([apple_x, apple_y, wall_x, wall_y, left, right, up, down]) # 1x8
        output = sigmoid(np.dot(input, W)) # 1x4
        
        d = dict(left = output[0], right = output[1], up = output[2], down = output[3])
        return max(d, key = d.get)

    @staticmethod
    def update(W, length, last_length, life, last_life, highscore):
        train = 10 # training speed
        innovate = 100 # random innovations
        if length >= highscore or length >= last_length or life >= last_life:
            W += train * (2*np.array(np.random.rand(8,4)) - 1)
        else:
            W += innovate * (2*np.array(np.random.rand(8,4)) - 1)
        return W

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def run_pygame():
    global run_AI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_AI = False

def eat_apple(eaten):
    global length
    global apple_x
    global apple_y
    if eaten is True:
        apple_x = random.randrange(grid, screen_width - 2*grid, grid)
        apple_y = random.randrange(grid, screen_height - 2*grid, grid)
        length += 1
        pygame.display.set_caption('Snake! Score: ' + str(length - 1))
        eaten = False # new apple only generated once per collision

def refresh():
    win.fill((0,0,0))
    global x
    global y
    global length
    if move == 'left' and (move != 'right' or length == 1):
        x -= vel
        x_hist.append(x)
        y_hist.append(y)
    elif move == 'right' and (move != 'left' or length == 1):
        x += vel
        x_hist.append(x)
        y_hist.append(y)
    elif move == 'up' and (move != 'down' or length == 1):
        y -= vel
        y_hist.append(y)
        x_hist.append(x)
    elif move == 'down' and (move != 'up' or length == 1):
        y += vel
        y_hist.append(y)
        x_hist.append(x)

    for i in range(0, length):
        pygame.draw.rect(win, (0,255,0), (x_hist[::-1][0+i], y_hist[::-1][0+i], grid, grid)) # draw character

    if eaten is False: # draw apple
        pygame.draw.rect(win, (255,0,0), (apple_x, apple_y, grid, grid))

    pygame.display.update()
    pygame.time.delay(refresh_rate)

run_AI = True
alive = True
generation = 1
life = 0
last_life = 0
last_length = 1

while run_AI:
    x = random.randrange(grid, screen_width - 2*grid, grid) # starting coordinates
    y = random.randrange(grid, screen_height - 2*grid, grid)
    x_hist = [0, x]
    y_hist = [0, y]
    move = 'stop'
    apple_x = random.randrange(grid, screen_width - 2*grid, grid) # starting apple
    apple_y = random.randrange(grid, screen_height - 2*grid, grid)
    eaten = False
    length = 1
    life = 0
    pygame.display.set_caption('Snake! Score: 0')

    while alive:
        run_pygame()
        aiSnake = nn(x, y, apple_x, apple_y, move)

        move = aiSnake.decide(apple_x - x, apple_y - y, screen_width - x, screen_height - y, move, 0, generation)

        if x < 0 or x > screen_width - width or y < 0 or y > screen_height - height: # hit walls
            alive = False

        if x == apple_x and y == apple_y: # eat apple
            eat_apple(True)
        else:
            eat_apple(False)

        # for i in range(0, length):
        #     if x == x_hist[::-1][1+i] and y == y_hist[::-1][1+i]:
        #         alive = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            alive = False # manual override

        life += 1
        refresh()

    print('Score: ' + str(length - 1) + '. Generation: ' + str(generation) + '. Highscore: ' + str(highscore) + '.')
    generation += 1
    W = aiSnake.update(W, length, last_length, life, last_life, highscore)
    last_length = length
    if length - 1 > highscore:
        highscore = length - 1
    last_life = life
    alive = True
    
pygame.quit()