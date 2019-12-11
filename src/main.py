import pygame
from grid import Grid
from snake import Snake

grid = Grid()
snake = Snake()

while True:
    grid.start()
    while snake.alive:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and snake.direction != "L":
            key_pressed = "L"
        elif keys[pygame.K_RIGHT] and snake.direction != "R":
            key_pressed = "R"
        elif keys[pygame.K_UP] and snake.direction != "U":
            key_pressed = "U"
        elif keys[pygame.K_DOWN] and snake.direction != "D":
            key_pressed = "D"

        snake.move(key_pressed)
        grid.refresh()
