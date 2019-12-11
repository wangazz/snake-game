import random


class Snake:
    alive = True
    highscore = 0
    length = 1
    score = 0
    history = [[]]

    def __init__(self, grid_size, grid_width, grid_height):
        self.width = grid_size
        self.height = grid_size
        self.position = [random.randrange(grid_size, grid_width - 2*grid_size, grid_size),
                         random.randrange(grid_size, grid_height - 2*grid_size, grid_size)]

    def die(self):
        if self.score > self.highscore:
            self.highscore = self.score
        return self.highscore

    def eat_apple(self, eaten):
        if eaten is True:
            self.length += 1

    def move(self, key_pressed):
        if key_pressed == "L" and (self.length == 1 or self.direction != "R"):
            self.direction = "L"

        elif key_pressed == "R" and (self.length == 1 or self.direction != "L"):
            self.direction = "R"

        elif key_pressed == "U" and (self.length == 1 or self.direction != "D"):
            self.direction = "U"

        elif key_pressed == "D" and (self.length == 1 or self.direction != "U"):
            self.direction = "D"
