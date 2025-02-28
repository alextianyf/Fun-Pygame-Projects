import pygame
from settings import game_settings
from game_stats import GameStats
import game_functions
from ship import Ship
from button import Button
from pygame.sprite import Group


def run_game():
    clock = pygame.time.Clock()
    pygame.init()

    screen = pygame.display.set_mode((game_settings.WINDOW_WIDTH,game_settings.WINDOW_HEIGHT))# 创建一个游戏窗口界面
    pygame.display.set_caption("Alien Invasion")# 设置游戏的名称

    # Creating a object called ship(创建一个飞船的object)
    ship = Ship(screen, game_settings)

    # Creating Button Object
    play_button = Button(game_settings,screen, "Play")

    bullets_group = Group()
    aliens_group = Group()

    stats = GameStats(game_settings)

    game_functions.create_alien_grid(game_settings,screen, aliens_group, ship)
    # 开始游戏的主循环
    game_running = True
    while game_running:
        clock.tick(game_settings.FPS)
        # 监视键盘和鼠标的事件
        game_functions.check_mouse_key_events(screen, game_settings,ship, bullets_group)

        if stats.game_active:
            # 更新屏幕
            game_functions.update_screen(screen, game_settings, ship, aliens_group, bullets_group, stats)

        else:
            play_button.draw_button()
            pygame.display.flip()

run_game()