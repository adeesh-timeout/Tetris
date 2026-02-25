from time import sleep

from config import *
import pygame
import os
import random

def rowcol_to_xy(row, col) -> tuple:
    return BOARD_X + SIDE * (col - 1), BOARD_Y + SIDE * (row - 1)

grid = list(EMPTY_GRID)
tetris_blocks = []

pygame.mixer.init()
DROP = pygame.mixer.Sound(os.path.join('Data/sound', 'drop.wav'))
LOSE = pygame.mixer.Sound(os.path.join('Data/sound', 'lose.wav'))
WIN = pygame.mixer.Sound(os.path.join('Data/sound', 'win.wav'))
BREAK_LINE = pygame.mixer.Sound(os.path.join('Data/sound', 'break_line_1.wav'))

class Block():
    screen = None
    is_won = None
    next_block = random.choice(BLOCK_KEYS)
    is_volume = True
    lines = 0
    blocks = 0
    break_lines_data : dict= {} # {20: 9, 19:10}
    fire_delay = 0
    fire_row = 0
    score = 0
    fire_disp = False
    is_pause = False
    combo = 0
    combo_delay = 0

    def __init__(self, row, col, block):
        self.row = row
        self.col = col
        self.screen = Block.screen

        self.block : str = block
        self.color : tuple = tetris_data[self.block][-1]
        self.data : list = list(tetris_data[self.block][0])

        self.rotate_index = 0
        self.change_count = 1
        self.is_done = False

        self.seize_right = self.seize_move = self.seize_left = False

        self.ghost_move_down = True
        self.ghost_far_col = 0
        self.ghost_far_row = 0
        self.ghost_row, self.ghost_col = self.row, self.col
        self.ghost_x, self.ghost_y = rowcol_to_xy(self.ghost_row, self.ghost_col)

        self.coordinates = []
        self.move_delay = 0
        self.slide_delay = 0

    def change_block(self): # Only for Testing, Temporary
        # Only for development 
        if not self.change_count >= 7:
            self.block = BLOCK_KEYS[self.change_count]
            self.change_count += 1

        else:
            self.block = BLOCK_KEYS[0]
            self.change_count = 1

        self.color: tuple = tetris_data[self.block][-1]
        self.data: list = list(tetris_data[self.block][0])
        self.rotate_index = 0

    def rotate_block(self):
        self.rotate_index += 1
        if type(tetris_data[self.block][self.rotate_index]) != tuple:
            self.data = list(tetris_data[self.block][self.rotate_index])

        else:
            self.data = list(tetris_data[self.block][0])
            self.rotate_index = 0

        # Checking Border Violation
        self.draw_block(False) # No draw, Just need coordinates of future block
        self.check_collision_block()

        if self.seize_move:
            if self.rotate_index == 0:
                self.rotate_index = 1
            else:
                self.rotate_index -= 1
            self.data = list(tetris_data[self.block][self.rotate_index])
            self.seize_move = False

        self.avoid_collision()

    def move_block(self, dir):
        if self.far_row == ROWS:
            self.seize_move = True

        if dir == 'L' and self.col - 1 > 0 and not self.seize_left:
            self.col -= 1
        elif dir == 'R' and self.far_col < COLUMN and not self.seize_right:
            self.col += 1

        if not self.seize_move:
            if dir == 'D' and self.far_row < ROWS and self.move_delay > 5:
                self.row += 1
                self.move_delay = 0

            else:
                self.move_delay += 1

    def add_gravity(self):
        if self.move_delay > 25:
            self.move_block('D')

        else:
            self.move_delay += 1

    def check_win(self):
        if sum(grid[-1]) == 0 and len(tetris_blocks) > 1:
            Block.is_pause = True
            Block.is_won = True
            WIN.play()

    def update(self):
        self.x, self.y = rowcol_to_xy(self.row,self.col)
        self.draw_block()
        Block.update_combo()

        if not Block.is_pause:
            self.add_gravity()
            self.check_collision_block()
            self.break_blocks()

            if self.seize_move and not self.is_done:
                if self.row in (1,2):
                    Block.is_won = False
                    Block.is_pause = True
                    if Block.is_volume: LOSE.play()

                else:
                    if self.slide_delay > 15:
                        self.update_grid()
                        self.is_done = True
                        Block.spawn_block()
                        self.slide_delay = 0

                    else: self.slide_delay += 1


    def avoid_collision(self):
        if self.far_col > COLUMN:
            self.col -= self.far_col - COLUMN
        if self.far_row > ROWS:
            self.row -= self.far_row - ROWS

    def check_collision_block(self):
        nonzero_index = 0
        self.seize_right = False
        self.seize_left = False
        self.avoid_collision()

        row_length = len(self.data)
        for i, row_data in enumerate(self.data):
            col_length = len(row_data)
            for j, col_data in enumerate(row_data):
                if col_data == 1:
                    # Lateral Check
                    if j - nonzero_index == 0: # First Block
                        if self.col+j-2 >= 0 and grid[self.row+i-1][self.col+j-2] == 1: # Left Check # Random Error
                            self.seize_left = True

                    if j+1 == col_length: # Last Block
                        if self.far_col < COLUMN and grid[self.row+i-1][self.far_col] == 1: # Right Check
                            self.seize_right = True

                    # Last Row
                    if i+1 == row_length:
                        if self.far_row < ROWS and grid[self.far_row][self.col+j-1]:
                            self.seize_move = True

                    else:
                        # Check Below for 1
                        if self.data[i+1][j] == 0:
                            if grid[self.row+i][self.col+j-1] == 1:
                                self.seize_move = True

                else: nonzero_index += 1
            nonzero_index = 0

    def draw_block(self, outline=False, draw=True):
        self.coordinates = []
        self.far_col = self.ghost_far_col = 0
        self.far_row = self.ghost_far_row = 0

        for i, row_data in enumerate(self.data):
            for j, col_data in enumerate(row_data):
                if col_data == 1:
                    self.coordinates.append((self.col + j, self.row + i))
                    # Width and Height
                    if self.far_col < self.col + j:
                        self.far_col = self.col + j

                    if self.far_row < self.row + i:
                        self.far_row = self.row + i

                    if draw:
                        pygame.draw.rect(self.screen, self.color, (self.x + SIDE * j, self.y + SIDE * i, SIDE-1, SIDE-1))

    def update_grid(self): # Critical
        if Block.is_volume: DROP.play()
        row = self.row-1
        col = self.col-1
        for row_data in self.data:
            for j in row_data:
                if j == 1:
                    grid[row][col] = 1
                col += 1

            row += 1
            col = self.col - 1

    def break_blocks(self):
        if self.row > 1 and self.seize_move:
            for i, row_data in enumerate(list(self.data)):
                row = self.row + i - 1
                if sum(grid[row]) == 10:
                    if row not in Block.break_lines_data:
                        Block.break_lines_data[row] = sum(row_data)
                    else:
                        Block.break_lines_data[row] += sum(row_data)

                    self.data.remove(row_data)

        Block.clear_grid()

    @staticmethod
    def init(window, FIRE):
        Block.screen = window
        Block.FIRE = FIRE

    @staticmethod
    def spawn_block(row = 1, col= 4, bloc = ''):
        if Block.is_won == None:
            if bloc == '':
                bloc = Block.next_block
            tetris_blocks.append(Block(row,col, bloc))
            Block.next_block = random.choice(BLOCK_KEYS)
            Block.blocks += 1

    @staticmethod
    def redraw_next_block():
        color = tetris_data[Block.next_block][-1]
        data = list(tetris_data[Block.next_block][0])

        x, y = BOARD_X+BOARD_WIDTH+100 + SIDE*2, BOARD_Y+40 + SIDE*2
        for i, row_data in enumerate(data):
            for j, col_data in enumerate(row_data):
                if col_data == 1:
                    pygame.draw.rect(Block.screen, color,(x + SIDE * j, y + SIDE * i, SIDE - 1, SIDE - 1))

    @staticmethod
    def reset():
        global grid

        Block.is_won = None
        Block.next_block = random.choice(BLOCK_KEYS)
        Block.is_volume = True
        Block.lines = 0
        Block.blocks = 0
        Block.break_lines_data= {}  # {20: 9, 19:10}
        Block.fire_delay = 0
        Block.fire_row = 0
        Block.score = 0
        Block.fire_disp = False
        Block.is_pause = False
        Block.combo = 0
        Block.combo_delay = 0

        grid.clear()
        for i in range(ROWS):
            grid.append([])
            for _ in range(COLUMN):
                grid[-1].append(0)

        tetris_blocks.clear()

        Block.spawn_block()

    @staticmethod
    def clear_grid():
        del_row = []
        Block.flame_animation()
        items = Block.break_lines_data.items()

        if len(items) > Block.combo:
            Block.combo = len(items)

        for k, v in list(items)[::-1]:
            if v == COLUMN:
                Block.lines += 1
                grid.pop(k)
                grid.insert(0, list(EMPTY_ROW))

                del_row.append(k)
                Block.fire_disp = True
                Block.fire_row = k

                for block in tetris_blocks:
                    block.row += 1

                for row in del_row:
                    if Block.is_volume: BREAK_LINE.play()
                    del Block.break_lines_data[row]

                return

    @staticmethod
    def flame_animation():
        if Block.fire_disp:
            x, y = rowcol_to_xy(Block.fire_row + 1, COLUMN + 1)
            Block.screen.blit(Block.FIRE, (x, y + 5))

            if Block.fire_delay > 50:
                Block.fire_disp = False
                Block.fire_delay = 0
            else:
                Block.fire_delay += 1

    @staticmethod
    def update_combo():
        if 0 <= Block.combo_delay < 100 and Block.combo != 0:
            LOC_FONT = pygame.font.SysFont('Consolas', 20)
            text = LOC_FONT.render(LINE_COMBO[Block.combo][0], 1, WHITE)
            x, y = rowcol_to_xy(22, 4)
            Block.screen.blit(text, (x, y - 10))
            Block.combo_delay += 1

        else:
            if Block.combo != 0:
                Block.score += LINE_COMBO[Block.combo][-1]
                Block.combo = 0
            Block.combo_delay = 0
