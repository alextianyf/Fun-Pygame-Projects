import pygame
import sys
from settings import game_settings

def run_game():
    pygame.init()

    screen = pygame.display.set_mode((game_settings.WINDOW_WIDTH,game_settings.WINDOW_HEIGHT))# 创建一个游戏窗口界面
    pygame.display.set_caption("Alien Invasion")# 设置游戏的名称

    # 开始游戏的主循环
    game_running = True
    while game_running:
        # 监视键盘和鼠标的事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # 每次循环时，都重新绘制屏幕颜色
        screen.fill(game_settings.bg_color)

        # 让最近绘制的屏幕可见
        pygame.display.flip()

run_game()