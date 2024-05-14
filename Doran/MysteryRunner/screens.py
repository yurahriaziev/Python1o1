from settings import *
from classes import *
from levels import lobby

def draw_grid():
    for line in range(screen_w//tile_size):
        pygame.draw.line(screen, (255,255,255), (0,line*tile_size), (screen_w, line*tile_size))
        pygame.draw.line(screen, (255,255,255), (line*tile_size, 0), (line*tile_size, screen_w))

def startscreen():
    clock = pygame.time.Clock()
    level0 = World(lobby, 0)

    plr = Player(300, 300, level0)
    offset_x = 0
    offset_y = 0
    scroll_area_width = 130

    run = True
    while run:
        clock.tick(60)
        screen.blit(bg, (0,0))

        level0.draw(offset_x, offset_y)

        plr.update(offset_x, offset_y)

        # draw_grid()
        max_offset_x = max(17*75-screen_w, 0)
        max_offset_y = max(17*75-screen_h, 0)

        if ((plr.rect.right - offset_x >= screen_w - scroll_area_width) and plr.dx > 0) and (offset_x < max_offset_x):
            offset_x += plr.dx
        if ((plr.rect.left - offset_x <= scroll_area_width) and plr.dx < 0) and (offset_x > 0):
            offset_x += plr.dx
        if ((plr.rect.bottom - offset_y >= screen_h - scroll_area_width) and plr.dy > 0) and (offset_y < max_offset_y):
            offset_y += plr.dy
        if ((plr.rect.top - offset_y <= scroll_area_width) and plr.dy < 0) and (offset_y > 0):
            offset_y += plr.dy

        # move player to next level
        if plr.rect.x > level0.finish_x:
            print(plr.current_level)
            load_level(plr, )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()


def load_level(plr):
    level_data = levels[plr.current_level]

    plr.current_level += 1
    level = World(level_data, plr.current_level)

    plr.rect.x = 100
    plr.rect.y = 100
    run = True
    while run:
        screen.blit(bg, (0,0))

        level.draw(None, None)

        plr.update(0,0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()


