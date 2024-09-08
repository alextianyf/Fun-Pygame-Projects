import pygame
import sys

def check_mouse_key_events():
    # 监视键盘和鼠标的事件
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

def update_screen(screen, game_settings, ship):
    # 每次循环时，都重新绘制屏幕颜色
    screen.fill(game_settings.bg_color)
    ship.display_ship()

    # 让最近绘制的屏幕可见
    pygame.display.flip()