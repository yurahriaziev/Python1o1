from settings import *

class Button:
    def __init__(self, x, y, type):
        self.type = type
        if self.type == 'play':
            self.img = pygame.image.load('img/play.png')

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        SCREEN.blit(self.img, self.rect)

    def clicked(self):
        self.click = False

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.click = True

        return self.click
    
class World:
    def __init__(self, level_data, level_assets):
        self.tiles = []
        self.items = []

        row_c = 0
        for row in level_data:
            col_c = 0
            for tile_type in row:
                if tile_type == 1:
                    tile_img = level_assets[0]
                    tile_rect = tile_img.get_rect()
                    tile_rect.x = col_c * TILE_SIZE
                    tile_rect.y = row_c * TILE_SIZE
                    tile = (tile_img, tile_rect, 1)
                    self.tiles.append(tile)
                if tile_type == 2:
                    tile_img = level_assets[1]
                    tile_rect = tile_img.get_rect()
                    tile_rect.x = col_c * TILE_SIZE
                    tile_rect.y = row_c * TILE_SIZE
                    tile = (tile_img, tile_rect, 2)
                    self.tiles.append(tile)
                if tile_type == 'R':
                    x = col_c * TILE_SIZE
                    y = row_c * TILE_SIZE+30
                    item = Item(tile_type, x, y)
                    self.items.append(item)
                if tile_type == 'B':
                    x = col_c * TILE_SIZE
                    y = row_c * TILE_SIZE+30
                    item = Item(tile_type, x, y)
                    self.items.append(item)

                col_c += 1
            row_c += 1

    def draw(self):
        for tile in self.tiles:
            SCREEN.blit(tile[0], tile[1])

        for item in self.items:
            item.draw()

class Player:
    def __init__(self, x, y, p_option, level, weapon):
        self.level = level
        self.level_items = self.level.items
        self.weapon = weapon

        self.img = pygame.image.load(f'img/{p_option}_plr.png')
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = 0
        self.jumped = False
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.shot_cooldown = 0

        # inventory
        self.inventory = Inventory()

    def update(self):
        self.inventory.draw()

        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            dx += 5
            self.img = pygame.image.load('img/plr_right.png')
            self.direction = 'r'
        if key[pygame.K_a]:
            dx -= 5
            self.img = pygame.image.load('img/plr_left.png')
            self.direction = 'l'
        if key[pygame.K_SPACE] and self.jumped == False:
            self.y_vel = -20
            self.jumped = True
        if key[pygame.K_e] and self.weapon.picked_up:
            if self.shot_cooldown == 0:
                self.shot_cooldown = 35
                self.weapon.shoot_wand()

        self.y_vel += 1
        if self.y_vel > 10:
            self.y_vel = 10
        dy += self.y_vel

        for tile in self.level.tiles:
            if tile[1].colliderect(self.rect.x, self.rect.y+dy, self.width, self.height):
                if self.y_vel >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.jumped = False
            if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                dx = 0

        for item in self.level_items:
            if self.rect.colliderect(item.rect):
                self.inventory.current_item_list.append(item)
                print(len(self.inventory.current_item_list))
                self.inventory.add_item(item)

        self.rect.x += dx
        self.rect.y += dy

        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        SCREEN.blit(self.img, self.rect)

class Inventory:
    def __init__(self):
        self.slot_list = []
        self.current_item_list = []


        slot_x = 20
        slot_y = 20
        for i in range(8):
            self.slot_rect = pygame.Rect(slot_x, slot_y, 120, 120)
            self.slot_list.append(self.slot_rect)
            slot_x += 130

    def draw(self):
        for slot in self.slot_list:
            pygame.draw.rect(SCREEN, (255, 255, 255), slot, 3)

    def add_item(self, item):
        self.next_available_slot = len(self.current_item_list) - 1
 
        item.rect.x = self.slot_list[self.next_available_slot].x + 20
        item.rect.y = self.slot_list[self.next_available_slot].y + 20
        item.rect.width = 80
        item.rect.height = 80

class Item:
    def __init__(self, type, x, y):
        if type == 'R':
            self.color = (255, 0, 0)
        if type == 'B':
            self.color = (0, 0, 255)

        self.rect = pygame.Rect(x, y, 20, 20)

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 8
        self.image = pygame.transform.scale(pygame.image.load('img/fire.png'), (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

        if self.direction == 'l':
            self.speed *= -1
        else:
            self.speed = abs(self.speed)


    def update(self):
        self.rect.x += self.speed

        if self.rect.right < 0 or self.rect.left > S_W:
            self.kill()
            
class Weapon:
    def __init__(self, x, y, weapon_type, projectile_group):
        self.type = weapon_type
        if self.type == 'wand1':
            self.img = pygame.image.load('img/wand1.png')

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.picked_up = False

        self.projectile_group = projectile_group

    def update(self, player):
        self.player = player
        if player.rect.colliderect(self.rect):
            self.picked_up = True
            self.rect.x = player.rect.x + 30
            self.rect.y = player.rect.y + 30

        SCREEN.blit(self.img, self.rect)
    
    def shoot_wand(self):
        fire = Projectile(self.rect.x+30, self.rect.y, self.player.direction)
        self.projectile_group.add(fire)

    def swing_sword(self):
        pass

    def attack(self):
        pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, projectiles):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('img/enemy.png')
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3
        self.hit = False
        self.projectiles = projectiles

    def draw_health_bar(self):
        outline = pygame.Rect(self.rect.centerx - 45, self.rect.y - 20, 94, 15)
        health = pygame.Rect(self.rect.centerx - 43, self.rect.y - 18, (self.health * 30), 11)
        pygame.draw.rect(SCREEN, 'black', outline, border_radius=5)
        pygame.draw.rect(SCREEN, 'green', health, border_radius=5)

    def update_health(self):
        for projectile in self.projectiles:
            if projectile.rect.colliderect(self.rect):
                projectile.kill()
                self.health -= 1
                self.hit = True
        
        if self.hit:
            self.draw_health_bar()

        if self.health == 0:
            self.kill()


    def update(self):
        self.update_health()
        SCREEN.blit(self.img, self.rect)
        




