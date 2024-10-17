import pygame
from settings import game_settings
import game_functions
from ship import Ship
from alien import Alien
from pygame.sprite import Group


def run_game():
    pygame.init()

    screen = pygame.display.set_mode((game_settings.WINDOW_WIDTH,game_settings.WINDOW_HEIGHT))# 创建一个游戏窗口界面
    pygame.display.set_caption("Alien Invasion")# 设置游戏的名称

    # Creating a object called ship(创建一个飞船的object)
    ship = Ship(screen, game_settings)

    bullets_group = Group()
    aliens_group = Group()

    game_functions.create_aliens_in_a_row(game_settings,screen, aliens_group)
    # 开始游戏的主循环
    game_running = True
    while game_running:
        # 监视键盘和鼠标的事件
        game_functions.check_mouse_key_events(screen, game_settings,ship, bullets_group)
        # 更新屏幕
        game_functions.update_screen(screen, game_settings, ship, aliens_group, bullets_group)

run_game()