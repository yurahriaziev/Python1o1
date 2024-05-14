import pygame, sys
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class World:
    def __init__(self, level_data, level_count):
        self.tiles = []
        for layer in level_data.layers:
            # if layer.name in ('Layer1-Tiles', 'Layer1-TopTiles')
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x*75,y*75-200)
                    surf = pygame.transform.scale(surf, (75, 75))
                    tile = Tile(pos, surf, sprite_group)
                    self.tiles.append(tile)

    def draw(self, x_offset, y_offset):
        for tile in self.tiles:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y+100))


pygame.init()
screen = pygame.display.set_mode((900, 600))
tmx_data = load_pygame('/Users/yuriihriaziev/Documents/Python1o1/Doran/MysteryRunner/level1.tmx')
print(tmx_data)

sprite_group = pygame.sprite.Group()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    level1 = World(tmx_data, 1)
    level1.draw(0,0)

    pygame.display.update()