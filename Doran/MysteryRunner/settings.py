import pygame
screen_w = 900
screen_h = 700
# screen_w = 500
# screen_h = 400
screen = pygame.display.set_mode((screen_w, screen_h))

bg = pygame.transform.scale(pygame.image.load('img/void.png'), (screen_w, screen_h))

tile_size = 75

# defining tiles here
# floors
wood_f = pygame.image.load('img/floor/wood_floor.png')

# walls
front_w = pygame.image.load('img/walls/front-wall.png')
left_w = pygame.image.load('img/walls/left-side-wall.png')
right_w = pygame.image.load('img/walls/right-side-wall.png')
back_w = pygame.image.load('img/walls/back-wall.png')

# wall corners
outer_top_left = pygame.image.load('img/corners/out-top-l-corner.png')
outer_top_right = pygame.image.load('img/corners/out-top-r-corner.png')
outer_bottom_left = pygame.image.load('img/corners/out-bottom-l-corner.png')
outer_bottom_right = pygame.image.load('img/corners/out-bottom-r-corner.png')
inner_bottom_left = pygame.image.load('img/corners/inner-bottom-l-corner.png')
inner_bottom_right = pygame.image.load('img/corners/inner-bottom-r-corner.png')
inner_top_right = pygame.image.load('img/corners/inner-top-r-corner.png')