from settings import *
from classes import *
from levels import lobby

def draw_grid():
    for line in range(screen_w//tile_size):
        pygame.draw.line(screen, (255,255,255), (0,line*tile_size), (screen_w, line*tile_size))
        pygame.draw.line(screen, (255,255,255), (line*tile_size, 0), (line*tile_size, screen_w))

def startscreen():
    clock = pygame.time.Clock()
    level0 = World(lobby)

    plr = Player(300, 300, level0)
    # offset_x = 0
    # offset_y = 0
    # scroll_area_width = 130

    run = True
    while run:
        clock.tick(60)
        screen.blit(bg, (0,0))

        level0.draw()

        plr.update()
        # level0.draw(offset_x, offset_y)

        # plr.update(offset_x, offset_y)

        # # draw_grid()

        # if ((plr.rect.right - offset_x >= screen_w - scroll_area_width) and plr.dx > 0) or ((plr.rect.left - offset_x <= scroll_area_width) and plr.dx < 0):
        #     offset_x += plr.dx
        # if ((plr.rect.bottom - offset_y >= screen_h - scroll_area_width) and plr.dy > 0) or ((plr.rect.top - offset_y <= scroll_area_width) and plr.dy < 0):
        #     offset_y += plr.dy
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()