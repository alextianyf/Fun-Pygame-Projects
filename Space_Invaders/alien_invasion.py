import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from aliens import Alien
import game_function as gf

def run_game():

    # 初始化游戏，并且创建一个screen的Object
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT))
    pygame.display.set_caption("Alien Invasion")

    # 创建一艘飞船
    ship = Ship(game_settings, screen)

    bullets_group = Group()
    aliens_group = Group()

    gf.create_aliens_group(game_settings, screen, ship, aliens_group)

    # 开始游戏的主循环
    while True:
        gf.check_events(game_settings, screen, ship, bullets_group)
        ship.update()

        gf.update_bullets(bullets_group)

        print(len(bullets_group))
        gf.update_screen(game_settings, screen, ship, aliens_group, bullets_group)


run_game()