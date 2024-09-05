from typing import *
import pygame

# Worker bee + blinker: [[3, 3], [4, 3], [4, 4], [4, 5], [5, 6], [6, 6], [6, 5], [9, 7], [9, 8], [9, 9], [12, 7], [12, 8], [12, 9], [3, 13], [4, 13], [4, 12], [4, 11], [
# 5, 10], [6, 10], [6, 11], [15, 5], [15, 6], [16, 6], [17, 5], [17, 4], [17, 3], [18, 3], [18, 13], [15, 10], [16, 10], [15, 11], [17, 11], [17, 12], [17, 13], [20, 20], [20, 21], [20, 22]]


class Cell():
    pass

PLAY = 1
PAUSE = 0
CURRENT_STATE = PLAY

MARGIN_TOP = 100
MARGIN_BOTTOM = 20
MARGIN_LEFT = 20
MARGIN_RIGHT = 20
BLOCK_SIZE = 10

C_WHITE = tuple([255] * 3)
C_FIELD_GRAY = tuple([166] * 3)
C_BLACK = tuple([0] * 3)

FIELD_SIZE_X = 88
FIELD_SIZE_Y = 88

WINDOW_SIZE_X = 920
WINDOW_SIZE_Y = 1000

PRESET_ALIVE = [[34, 3], [34, 4], [35, 3], [35, 4], [41, 4], [42, 4], [41, 5], [42, 5], [39, 8], [40, 8], [39, 9], [40, 9], [45, 10], [46, 10], [45, 11], [46, 11], [44, 17], [45, 17], [44, 18], [45, 19], [44, 20], [45, 20], [10, 8], [11, 8], [10, 9], [11, 9], [4, 12], [5, 12], [4, 13], [5, 13], [8, 14], [9, 14], [8, 15], [9, 15], [3, 19], [3, 20], [4, 19], [4, 20], [17, 9], [17, 10], [18, 10], [19, 9], [20, 9], [20, 10], [9, 34], [10, 34],
                [9, 35], [10, 36], [9, 37], [10, 37], [8, 43], [9, 43], [8, 44], [9, 44], [14, 45], [15, 45], [14, 46], [15, 46], [12, 49], [13, 49], [12, 50], [13, 50], [19, 50], [19, 51], [
                    20, 51], [20, 50], [23, 40], [23, 41], [24, 40], [34, 44], [24, 42], [25, 42], [26, 40], [26, 42], [27, 39], [28, 39], [28, 41], [29, 39], [30, 38], [34, 45], [35, 45],
                [36, 44], [37, 44], [37, 45], [50, 34], [51, 34], [50, 35], [51, 35], [45, 39], [45, 40], [46, 39], [46, 40], [49, 41], [50, 41], [49, 42], [50, 42], [43, 45], [44, 45], [43, 46], [44, 46]]

PRESET_ALIVE.extend([[33, 63], [34, 63], [34, 64], [34, 65], [35, 66], [36, 66], [36, 65], [39, 67], [39, 68], [39, 69], [42, 67], [42, 68], [42, 69], [33, 73], [34, 73], [34, 72], [34, 71], [35, 70], [36, 70], [36, 71], [45, 65], [45, 66], [46, 66], [47, 65], [47, 64], [47, 63], [48, 63], [48, 73], [45, 70], [46, 70], [45, 71], [47, 71], [47, 72], [47, 73], [50, 80], [50, 81], [50, 82]])

class Field():
    size_x = FIELD_SIZE_X
    size_y = FIELD_SIZE_Y

    def __init__(self):
        self.__field = list()
        for y in range(self.size_y):
            new_row = list()
            for x in range(self.size_x):
                new_row.append(
                    Cell(x, y, True if [x, y] in PRESET_ALIVE else False))
            self.__field.append(new_row)

    def get_neighbors(self, target_x: int, target_y: int) -> list:
        "Getting all 8 neighbors of the cell"
        # [1] [2] [4]
        # [3] [t] [5]
        # [8] [7] [6]
        # t — target cell, numbers — order of getting cells in neighbors.append instructions
        neighbors = list()
        neighbors.append(self.__field[target_y - 1][target_x - 1])
        neighbors.append(self.__field[target_y - 1][target_x])
        neighbors.append(self.__field[target_y][target_x - 1])

        neighbors.append(self.__field[target_y - 1]
                         [(target_x + 1) % FIELD_SIZE_X])
        neighbors.append(self.__field[target_y][(target_x + 1) % FIELD_SIZE_X])
        neighbors.append(self.__field[(target_y + 1) %
                         FIELD_SIZE_Y][(target_x + 1) % FIELD_SIZE_X])
        neighbors.append(self.__field[(target_y + 1) % FIELD_SIZE_Y][target_x])
        neighbors.append(self.__field[(target_y + 1) %
                         FIELD_SIZE_Y][target_x - 1])

        return neighbors

    def get_cell(self, x: int, y: int) -> Cell:
        if not (0 <= x < FIELD_SIZE_X and 0 <= y < FIELD_SIZE_Y):
            raise ValueError("Cell coordinate out of range.")

        return self.__field[y][x]

    def update(self):
        field = list()
        for y in range(self.size_y):
            new_row = list()
            for x in range(self.size_x):
                is_cell_currently_alive = self.get_cell(x, y).alive
                neighbors = self.get_neighbors(x, y)
                alive_neighbors = 0
                for neighbor in neighbors:
                    if neighbor.alive:
                        alive_neighbors += 1
                # * Rule 1: If alive and has < 2 alive neighbors, cell dies
                if is_cell_currently_alive and alive_neighbors < 2:
                    new_row.append(Cell(x, y, False))
                # * Rule 2: If alive and has 2 or 3 alive neighbors, cell doesn't change
                elif is_cell_currently_alive and 2 <= alive_neighbors <= 3:
                    new_row.append(Cell(x, y, True))
                # * Rule 3: If alive and has > 3 alive neighbirs, cell dies
                elif is_cell_currently_alive and alive_neighbors > 3:
                    new_row.append(Cell(x, y, False))
                # * Rule 4: If dead and has 3 alive neighbors, cell comes alive
                elif not is_cell_currently_alive and alive_neighbors == 3:
                    new_row.append(Cell(x, y, True))
                # * Keeping dead cells dead
                else:
                    new_row.append(Cell(x, y, False))
            field.append(new_row)
        self.__field = field

    def draw(self, surface):
        for x in range(MARGIN_LEFT, MARGIN_LEFT + BLOCK_SIZE * FIELD_SIZE_X + 1, BLOCK_SIZE):
            pygame.draw.line(surface, C_FIELD_GRAY, [
                x, MARGIN_TOP], [x, BLOCK_SIZE * FIELD_SIZE_Y + MARGIN_TOP], 1)
        for y in range(MARGIN_TOP, MARGIN_TOP + BLOCK_SIZE * FIELD_SIZE_Y + 1, BLOCK_SIZE):
            pygame.draw.line(surface, C_FIELD_GRAY, [MARGIN_LEFT, y], [
                             BLOCK_SIZE * FIELD_SIZE_X + MARGIN_LEFT, y], 1)

        for cell_row in self.__field:
            for cell in cell_row:
                if cell.alive:
                    pygame.draw.rect(surface, C_WHITE, (MARGIN_LEFT + BLOCK_SIZE * cell.x + 1,
                                     MARGIN_TOP + BLOCK_SIZE * cell.y + 1, BLOCK_SIZE - 1, BLOCK_SIZE - 1))
                else:
                    pygame.draw.rect(surface, C_BLACK, (MARGIN_LEFT + BLOCK_SIZE * cell.x + 1,
                                     MARGIN_TOP + BLOCK_SIZE * cell.y + 1, BLOCK_SIZE - 1, BLOCK_SIZE - 1))


class Cell():
    def __init__(self, x: int, y: int, alive: bool) -> Cell:
        self.x = x
        self.y = y
        self.alive = alive


class Window():
    tick = 0

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
        pygame.font.init()
        font = pygame.font.SysFont('couriernew', 40)
        text = font.render("""== Conway's "Game of life" ==""",
                           Text, pygame.color.THECOLORS['white'])
        self.screen.blit(text, (120, 10))

        self.field = Field()
        self.field.draw(self.screen)
        pygame.display.flip()
        pass

    def run(self):
        while True:
            pygame.time.Clock().tick(4)
            for event in pygame.event.get():
                # if event.type == pygame.K_
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.loop()

            pygame.display.flip()
        pass

    def loop(self):
        if CURRENT_STATE == PLAY:
            self.field.update()
        self.field.draw(self.screen)
        pass


try:
    while True:
        PRESET_ALIVE.append([int(input("Enter x: ")) + 3,
                            int(input("Enter y: ")) + 3])
except:
    pass
print('enough.\n', PRESET_ALIVE)
Window().run()
