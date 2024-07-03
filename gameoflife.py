from typing import *
import pygame

class Cell(): pass


MARGIN_TOP = 100
MARGIN_BOTTOM = 20
MARGIN_LEFT = 20
MARGIN_RIGHT = 20
BLOCK_SIZE = 20

FIELD_SIZE_X = 80
FIELD_SIZE_Y = 80

class Field():
    size_x = FIELD_SIZE_X
    size_y = FIELD_SIZE_Y

    def __init__(self):
        self.__field = list()
        for y in range(self.size_y):
            new_row = list()
            for x in range(self.size_x):
                new_row.append(Cell(x, y, False))

    def get_neighbors(self, target_x: int, target_y: int) -> list:
        neighbors = list()
        neighbors.append(self.__field[target_y - 1][target_x - 1])
        neighbors.append(self.__field[target_y - 1][target_x])
        neighbors.append(self.__field[target_y][target_x - 1])

        neighbors.append(self.__field[target_y - 1][(target_x + 1) % FIELD_SIZE_X])
        neighbors.append(self.__field[target_y][(target_x + 1) % FIELD_SIZE_X])
        neighbors.append(self.__field[(target_y + 1) % FIELD_SIZE_Y][(target_x + 1) % FIELD_SIZE_X])
        neighbors.append(self.__field[(target_y)])
        


    def update(self):
        field = list()
        for y in range(self.size_y):
            new_row = list()
            for x in range(self.size_x):
                neighbors = self.get_neighbords(x, y)
        pass




class Cell():
    def __init__(self, x: int, y: int, alive: bool) -> Cell:
        self.x = x
        self.y = y
        self.alive = alive



class Window():
    tick = 0
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.font.init()
        font = pygame.font.SysFont('couriernew', 40)
        text = font.render("""== Conway's "Game of life" ==""", Text, pygame.color.THECOLORS['white'])
        self.screen.blit(text, (255, 10))
        pass

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.flip()    
        pass

    def loop(self):
        pass


Window().run()