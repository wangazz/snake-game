import pygame
import random


class Grid:
    grid_size = 25
    screen_width = 30 * grid_size
    screen_height = 20 * grid_size
    refresh_rate = 70
    velocity = grid_size

    def __init__(self):
        pygame.init()
        win = pygame.display.set_mode((screen_width, screen_height))

    def refresh(self):
        pygame.display.update()
        pygame.time.delay(refresh_rate - length + 1)

    @staticmethod
    def start():
        pygame.run()
