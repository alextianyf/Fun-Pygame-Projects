import pygame
from settings import game_settings
import game_functions
from ship import Ship

def run_game():
    pygame.init()

    screen = pygame.display.set_mode((game_settings.WINDOW_WIDTH,game_settings.WINDOW_HEIGHT))# 创建一个游戏窗口界面
    pygame.display.set_caption("Alien Invasion")# 设置游戏的名称

    # 创建一个飞船的object
    ship = Ship(screen, game_settings)

    # 开始游戏的主循环
    game_running = True
    while game_running:
        # 监视键盘和鼠标的事件
        game_functions.check_mouse_key_events(ship)
        ship.move_ship()
        # 更新屏幕
        game_functions.update_screen(screen, game_settings, ship)

run_game()