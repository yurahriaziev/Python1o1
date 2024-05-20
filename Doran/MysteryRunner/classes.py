from settings import *
class Button:
    def __init__(self, x, y, type):
        if type == 'play':
            self.img = pygame.image.load('img/play-btn.png')
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.img, self.rect)

class World:
    def __init__(self, level_data, level_count):
        self.camera_x_offset = 200
        self.camera_y_offset = 70
        self.tiles = []
        #
        self.top_tiles = []
        row_c = 0

        self.tile_group = pygame.sprite.Group()

        self.level_count = level_count
        self.finish_x = None

        self.coins = pygame.sprite.Group()

        if self.level_count == 0:
            for row in level_data[0]:
                col_c = 0
                for tiletype in row:
                    tilefound = False
                    if tiletype == 41:
                        img = pygame.transform.scale(wood_f, (tile_size, tile_size))
                        marker = 1
                        tilefound = True
                    if tiletype == 52:
                        img = pygame.transform.scale(front_w, (tile_size, tile_size*3))
                        marker = 2
                        tilefound = True
                    if tiletype == 129:
                        # make left side wall
                        img = pygame.transform.scale(left_w, (tile_size, tile_size))
                        marker = 2
                        tilefound = True
                    if tiletype == 130:
                        # make right side wall
                        img = pygame.transform.scale(right_w, (tile_size, tile_size))
                        marker = 2
                        tilefound = True
                    if tiletype == 77:
                        # make back wall
                        img = pygame.transform.scale(back_w, (tile_size, tile_size))
                        marker = 2
                        tilefound = True
                    if tiletype == 104:
                        # make outer top left wall corner
                        img = pygame.transform.scale(outer_top_left, (tile_size, tile_size))
                        marker = 2
                        tilefound = True
                    if tiletype == 105:
                        # make outer top right wall corner
                        img = pygame.transform.scale(outer_top_right, (tile_size, tile_size))
                        marker = 2
                        tilefound = True
                    if tiletype == 154:
                        # make outer bottom left wall corner
                        img = pygame.transform.scale(outer_bottom_left, (tile_size, tile_size))
                        marker = 2
                        tilefound = True
                    if tiletype == 155:
                        # make outer bottom right wall corner
                        img = pygame.transform.scale(outer_bottom_right, (tile_size, tile_size))
                        marker = 2
                        tilefound = True
                    if tiletype == 78:
                        # make inner bottom left wall corner
                        img = pygame.transform.scale(inner_bottom_left, (tile_size, tile_size))
                        marker = 2
                        tilefound = True
                    if tiletype == 76:
                        # make inner bottom right wall corner
                        img = pygame.transform.scale(inner_bottom_right, (tile_size, tile_size))
                        marker = 2
                        tilefound = True
                    if tiletype == 101:
                        # make inner top right wall corner
                        img = pygame.transform.scale(inner_top_right, (tile_size, tile_size))
                        marker = 2
                        tilefound = True
                    
                    if tilefound:
                        tile_rect = img.get_rect()
                        if tiletype == 52:
                            tile_rect.x = col_c * tile_size - self.camera_x_offset
                            tile_rect.y = row_c * tile_size - tile_size*2 - self.camera_y_offset
                        else:
                            tile_rect.x = col_c * tile_size - self.camera_x_offset
                            tile_rect.y = row_c * tile_size - self.camera_y_offset
                        tile = (img, tile_rect, marker)
                        if tiletype == 101:
                            self.top_tiles.append(tile)
                        else:
                            self.tiles.append(tile)
                    col_c += 1
                row_c += 1
            row_c2 = 0
            for row in level_data[1]:
                col_c2 = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(pygame.image.load('img/start_level_text_lobby1.png'), (130, 50))
                        tile_rect = img.get_rect()
                        tile_rect.x = tile_size * col_c2
                        tile_rect.y = tile_size * row_c2 + 25
                        tile = (img, tile_rect)
                        self.top_tiles.append(tile)
                    if tile == 'F':
                        self.finish_x = col_c2 * tile_size
                    col_c2 += 1
                row_c2 += 1
        else:
            for layer in level_data.layers:
                if hasattr(layer, 'data'):
                    for x, y, surf in layer.tiles():
                        pos = (x*75,y*75+20)
                        surf = pygame.transform.scale(surf, (75, 75))
                            
                        if layer.name == 'coins':
                            coin = Coin(pos, surf, self.coins, layer.name)
                            self.coins.add(coin)
                        else:
                            tile = Tile(pos, surf, self.tile_group, layer.name)
                            self.tiles.append(tile)
                

    def draw(self, offset_x, offset_y):
        if self.level_count == 0:
            for tile in self.tiles:
                screen.blit(tile[0], (tile[1].x - offset_x, tile[1].y - offset_y))
            
            for tile in self.top_tiles:
                screen.blit(tile[0], (tile[1].x - offset_x, tile[1].y - offset_y))
        else:
            for tile in self.tiles:
                screen.blit(tile.image, (tile.rect.x - offset_x, tile.rect.y - offset_y))
            
            self.coins.update(offset_x, offset_y)

class Player:
    def __init__(self, x_pos, y_pos, level):
        self.sprite_sheet_img = pygame.transform.scale_by(pygame.image.load('img/Idle-Sheet.png').convert_alpha(), 2)
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_img)

        self.idle_animation_list = []
        self.animation_steps = 4
        self.last_update = pygame.time.get_ticks()
        self.anim_cooldown = 200
        self.frame = 0

        self.current_level = 0

        self.current_coins_amount = 0

        for x in range(self.animation_steps):
            self.idle_animation_list.append(self.sprite_sheet.get_image(x, 64, 64))
        
        self.rect = self.idle_animation_list[0].get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.width = self.idle_animation_list[0].get_width()
        self.height = self.idle_animation_list[0].get_height()

        self.level = level

        self.wall_hitbox = pygame.Rect(self.rect.x+10, self.rect.y + 30, self.width-20, 35)

    def update(self, offset_x, offset_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.anim_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.idle_animation_list):
                self.frame = 0

        # moving player
        self.dx = 0
        self.dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            self.dx += 5
            self.direction = 'd'
        if key[pygame.K_a]:
            self.dx -= 5
            self.direction = 'a'
        if key[pygame.K_w]:
            self.dy -= 5
            self.direction = 'w'
        if key[pygame.K_s]:
            self.dy += 5
            self.direction = 's'

        # collisions with walls
        # wall tile has marker of 2 in the tile tuple in world.tiles
        
        for tile in self.level.tiles:
            if self.level.level_count == 0:
                if tile[2] == 2:
                    tile_rect = tile[1]
                    if tile_rect.colliderect(self.wall_hitbox.x, self.wall_hitbox.y+self.dy, self.width-20, 35):
                        self.dy = 0
                    if tile_rect.colliderect(self.wall_hitbox.x+self.dx, self.wall_hitbox.y, self.width-20, 35):
                        self.dx = 0
            else:
                if tile.name == 'walls':
                    tile_rect = tile.rect
                    # pygame.draw.rect(screen, 'white', tile.rect, 2)
                    if tile_rect.colliderect(self.wall_hitbox.x, self.wall_hitbox.y+self.dy, self.width-20, 35):
                        self.dy = 0
                    if tile_rect.colliderect(self.wall_hitbox.x+self.dx, self.wall_hitbox.y, self.width-20, 35):
                        self.dx = 0
                for coin in self.level.coins:
                    if self.rect.colliderect(coin.coin_hitbox):
                        self.current_coins_amount += 1
                        coin.kill()  

        # display number of coins  
        self.show_number_of_coins()        
        
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.wall_hitbox.x += self.dx
        self.wall_hitbox.y += self.dy
        
        screen.blit(self.idle_animation_list[self.frame], (self.rect.x - offset_x, self.rect.y - offset_y))
        # pygame.draw.rect(screen, 'white', (self.wall_hitbox.x-offset_x, self.wall_hitbox.y - offset_y, self.width-20, 35), 2)

    def show_number_of_coins(self):
        frame = pygame.transform.scale_by(pygame.image.load('img/coin_frame.png'), 3)
        coin_image = pygame.transform.scale_by(pygame.image.load('img/coin.png'), 4)
        coin_text = font.render(str(self.current_coins_amount), True, (255,255,255))

        screen.blit(frame, (10, 10))
        screen.blit(coin_image, (20, 15))
        screen.blit(coin_text, (95, 20))

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height):
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        self.image.set_colorkey((0,0,0))

        return self.image
    
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, name):
        super().__init__(groups)
        self.name = name
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, name):
        super().__init__(groups)
        self.name = name
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.width = 25
        self.rect.height = 25
        self.coin_hitbox = pygame.Rect(pos[0]+25, pos[1]+25, self.rect.width, self.rect.height)

    def update(self, offset_x, offset_y):
        screen.blit(self.image, (self.rect.x-offset_x, self.rect.y-offset_y))
        ### draw position rect
        # pygame.draw.rect(screen, 'white', (self.rect.x-offset_x, self.rect.y-offset_y, self.rect.width, self.rect.height), 1)
        ### draw coin hitbox rect
        # pygame.draw.rect(screen, 'red', (self.coin_hitbox.x-offset_x, self.coin_hitbox.y-offset_y, self.coin_hitbox.width, self.coin_hitbox.height), 1)

