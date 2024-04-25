from settings import *
from classes import Button, World, Player, Weapon, Enemy, Item
from levels import LEVEL_1_DATA

def play_screen(level):
    clock = pygame.time.Clock()
    level_bg, level_assets = return_level_bg(level)
    level = World(LEVEL_1_DATA, level_assets)

    projectile_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    wand1 = Weapon(400, 560, 'wand1', projectile_group)

    coin_group = pygame.sprite.Group()

    player = Player(200, 200, 'white', level, wand1, coin_group)

    enemy = Enemy(800, 515, projectile_group)
    enemy_group.add(enemy)
    for enemy in enemy_group:
        coin = Item('Coin', None, None, enemy)
        level.items.append(coin)

    run = True
    while run:
        clock.tick(FPS)
        
        SCREEN.blit(level_bg, (0,0))

        level.draw()

        player.update()

        wand1.update(player)

        enemy_group.update()


        projectile_group.update()
        projectile_group.draw(SCREEN)


        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if key[pygame.K_ESCAPE]:
                start_screen()

        pygame.display.update()

    pygame.quit()

def choose_player_screen():
    pass

def start_screen():
    run = True
    while run:
        # background
        SCREEN.blit(START_MENU_BG, (0, 0))

        play_btn = Button(S_W//2-200, S_H//2-170, 'play')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and play_btn.clicked():
                print('play clicked')
                play_screen(1)

        pygame.display.update()

    pygame.quit()