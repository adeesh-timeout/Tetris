import pygame
import os
import random

from pygame.mixer import pause

# Change Directory # Random Error 01
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Sub-files imports
from config import *
from block import *

run = True

pygame.init()

pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
FONT_1 = pygame.font.SysFont('Courier New', 30)
FONT_2 = pygame.font.SysFont('Comic Sans MS', 40)

FIRE = pygame.image.load(os.path.join('Data/image', 'fire.png'))
FIRE = pygame.transform.smoothscale(FIRE, (20, 20))
ICON = pygame.image.load(os.path.join('Data/image', 'tetris.png'))
pygame.display.set_icon(ICON)

PAUSE = pygame.image.load(os.path.join('Data/image', 'pause.png'))
PAUSE = pygame.transform.smoothscale(PAUSE, (50, 50))

PLAY = pygame.image.load(os.path.join('Data/image', 'play.png'))
PLAY = pygame.transform.smoothscale(PLAY, (50, 50))

VOLUME = pygame.image.load(os.path.join('Data/image', 'volume.png'))
VOLUME = pygame.transform.smoothscale(VOLUME, (50, 50))

MUTE = pygame.image.load(os.path.join('Data/image', 'mute.png'))
MUTE = pygame.transform.smoothscale(MUTE, (50, 50))

Block.init(screen, FIRE)

pause_x, pause_y = rowcol_to_xy(15,10)
pause_x += 220

def box_layout_generator(x, y, rows,cols,side):
    height = side*rows
    width = side*cols

    for row_n in range(rows+1):
        for col_n in range(cols+1):
            # Vertical Lines
            pygame.draw.line(screen, WHITE, (x+side*col_n, y), (x+side*col_n, y+height))
        # Horizontal Lines
        pygame.draw.line(screen, WHITE, (x, y+side*row_n), (x+width, y+side*row_n))

def display_status():
    text = FONT_2.render(f'Lines: {Block.lines}', 1, WHITE)
    screen.blit(text, (BOARD_X + BOARD_WIDTH + 100, BOARD_Y + 210))

    text = FONT_2.render(f'Blocks: {str(Block.blocks)}', 1, WHITE)
    screen.blit(text, (BOARD_X + BOARD_WIDTH + 100, BOARD_Y + 290))

def draw_layout():
    box_layout_generator(BOARD_X, BOARD_Y, 20, 10, SIDE)
    box_layout_generator(BOARD_X+BOARD_WIDTH+100, BOARD_Y+40, 4, 7, SIDE)

    text = FONT_1.render('Next Block', 1, WHITE)
    screen.blit(text, (BOARD_X+BOARD_WIDTH+100, BOARD_Y))

def game_over():
    x, y = rowcol_to_xy(8, 0)
    pygame.draw.rect(screen, (150, 0, 200), (x+SIDE+1, y+1, BOARD_WIDTH-1, -1 + SIDE*5))

    text = FONT_2.render('Game Over', 1, WHITE)
    screen.blit(text, (x+SIDE+1+50, y+1+10))

    LOC_FONT = pygame.font.SysFont('Consolas', 20)
    text = LOC_FONT.render('Press Enter to restart', 1, WHITE)
    screen.blit(text, (x+SIDE+1+30, y+1+85))

    if keys[pygame.K_RETURN]:
        Block.clear()

# First Block
Block.spawn_block()

def game_code():
    for block in tetris_blocks:
        block.update()
    Block.redraw_next_block()

def check_pressed(box_x, box_y, side):
    x, y = pygame.mouse.get_pos()
    if box_x < x < box_x + side and box_y < y < box_y + side: return True
    else: return False

def pause_play():
    if Block.is_pause:
        screen.blit(PLAY, (pause_x,pause_y))

        LOC_FONT = pygame.font.SysFont('Comic Sans MS', 35)
        text = LOC_FONT.render("PAUSED", 1, WHITE)
        x, _ = rowcol_to_xy(2,0)
        screen.blit(text, (x+BOARD_X+10, 0))

    else:
        screen.blit(PAUSE, (pause_x, pause_y))

def volume_func():
    if Block.is_volume:
        screen.blit(VOLUME, (pause_x,pause_y+100))
    else:
        screen.blit(MUTE, (pause_x, pause_y+100))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if check_pressed(pause_x, pause_y, 50):
                if Block.is_pause:
                    Block.is_pause = False
                else:
                    Block.is_pause = True

            if check_pressed(pause_x, pause_y+100, 50):
                if Block.is_volume:
                    Block.is_volume = False
                else:
                    Block.is_volume = True

        if event.type == pygame.KEYDOWN:
            if not Block.is_pause:
                if event.key == pygame.K_UP:
                    tetris_blocks[-1].rotate_block()

                if event.key == pygame.K_LCTRL:
                    tetris_blocks[-1].change_block()

                if event.key == pygame.K_RIGHT:
                    tetris_blocks[-1].move_block('R')

                elif event.key == pygame.K_LEFT:
                    tetris_blocks[-1].move_block('L')

            if event.key == pygame.K_ESCAPE:
                if Block.is_pause:
                    Block.is_pause = False
                else:
                    Block.is_pause = True

    keys = pygame.key.get_pressed()
    screen.fill(GREY)

    if keys[pygame.K_DOWN]:
        tetris_blocks[-1].move_block('D')

    # Main Code
    game_code()
    display_status()
    draw_layout()
    pause_play()
    volume_func()

    if Block.is_game_over:
        game_over()

    pygame.display.update()
    clock.tick(FPS)
