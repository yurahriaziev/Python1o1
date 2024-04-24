# file that will hold the game's settings

import pygame
import random

S_W, S_H = 1400, 800
SCREEN = pygame.display.set_mode((S_W, S_H))
TILE_SIZE = 50
FPS = 120

bg = pygame.image.load('img/bg_start_screen.png')
START_MENU_BG = pygame.transform.scale(bg, (1400, 800))

def return_level_bg(level):
    if level == 1:
        LEVEL_BG = START_MENU_BG
        level_top_tile = pygame.image.load('img/lvl1_grass.png')
        level_top_tile = pygame.transform.scale(level_top_tile, (TILE_SIZE, TILE_SIZE))

        level_dirt_tile = pygame.image.load('img/lvl1_dirt.png')
        level_dirt_tile = pygame.transform.scale(level_dirt_tile, (TILE_SIZE, TILE_SIZE))
        LVL_ASSETS = [level_top_tile, level_dirt_tile]

    return LEVEL_BG, LVL_ASSETS