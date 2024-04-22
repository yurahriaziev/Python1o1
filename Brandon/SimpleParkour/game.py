import pygame
from levels import level1_data
pygame.init()
s_w = 1000
s_h = 800
screen = pygame.display.set_mode((s_w, s_h))
bg = pygame.image.load('img/bg.png')

tile_size = 50

class Button:
    def __init__(self,btn_type,x,y):
        self.img = pygame.image.load(f'img/{btn_type}.png')
        if btn_type == 'blue_plr_btn' or btn_type == 'red_plr_btn':
            self.img = pygame.transform.scale(self.img, (200, 300))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.img,self.rect)

    def clicked(self):
        clicked = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            clicked = True

        return clicked
    
class Player:
    def __init__(self, player_look, x, y, level):
        self.level = level

        if player_look == 'blue':
            image = 'blue_plr'
        elif player_look == 'red':
            image = 'red_plr'

        self.img = pygame.image.load(f"img/{image}.png")
        self.img = pygame.transform.scale(self.img, (120, 170))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.y_vel = 0
        self.jumped = False
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def update(self, offset_x):
        self.dx = 0
        self.dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            self.dx+=5
        if key[pygame.K_a]:
            self.dx-=5
        if key[pygame.K_SPACE] and self.jumped == False:
            self.y_vel = -20
            self.jumped = True

        self.y_vel += 1
        if self.y_vel > 10:
            self.y_vel = 10
        self.dy += self.y_vel

        # collisions
        for tile in self.level.tiles:
            if tile[1].colliderect(self.rect.x, self.rect.y+self.dy, self.width, self.height):
                if tile[2] == 1:
                    if self.y_vel >= 0:
                        self.dy = tile[1].top - self.rect.bottom
                        self.jumped = False
            if tile[1].colliderect(self.rect.x+self.dx, self.rect.y, self.width, self.height):
                if tile[2] == 1:
                    self.dx = 0
                # if tile[3[]]

        self.rect.x += self.dx
        self.rect.y += self.dy
        screen.blit(self.img, (self.rect.x - offset_x, self.rect.y))

class World:
    def __init__(self, level):
        self.tiles = []
        grass = pygame.image.load('img/grass1.png')
        dirt = pygame.image.load('img/dirt1.png')
        border = pygame.image.load('img/border.png')
        spike1 = pygame.image.load('img/spike1.png')

        row_count = 0
        for row in level:
            col_count = 0
            for tile_type in row:
                # tile type - 1: have collision
                # tile type - 2: no collision
                if tile_type == 1:
                    img = pygame.transform.scale(grass, (50, 50))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, 1, 'grass')
                    self.tiles.append(tile)
                elif tile_type == 2:
                    img = pygame.transform.scale(dirt, (50, 50))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, 1, 'dirt')
                    self.tiles.append(tile)
                elif tile_type == 3:
                    img = pygame.transform.scale(border, (25, 50))
                    img_rect = img.get_rect()
                    img_rect.x = (col_count * tile_size) + 12.5
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, 1, 'border')
                    self.tiles.append(tile)
                elif tile_type == 4:
                    img = pygame.transform.scale(spike1, (50, 50))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, 2, 'trap')
                    self.tiles.append(tile)

                col_count+=1
            row_count+=1

    def draw(self, offset_x):
        for tile in self.tiles:
            screen.blit(tile[0], (tile[1].x - offset_x, tile[1].y))


def draw_frame():
    pass
    

def start_screen(player_option):
    run = True
    while run:
        screen.blit(bg,(0,0))

        # adding choose player button
        play_btn = Button('play_btn', 360, 300)
        choose_player_btn = Button('choose_plr_1', 200, 600)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and choose_player_btn.clicked():
                pass
            if event.type == pygame.MOUSEBUTTONDOWN and play_btn.clicked():
                play_screen(player_option)

        pygame.display.update()


    pygame.quit()


def play_screen(player_option):
    clock = pygame.time.Clock()

    level1 = World(level1_data)

    player = Player(player_option, 200, 500, level1)

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(120)

        screen.fill((255,255,255))

        level1.draw(offset_x)

        player.update(offset_x)

        if ((player.rect.right - offset_x >= s_w - scroll_area_width) and player.dx > 0) or ((player.rect.left - offset_x <= scroll_area_width) and player.dx < 0):
            offset_x += player.dx

        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if key[pygame.K_ESCAPE]:
                start_screen(player_option)

            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()

    pygame.quit()
    
start_screen('blue')
    
