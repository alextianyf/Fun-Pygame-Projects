import pygame
import sys

def check_keydown(ship, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

def check_keyup(ship, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_mouse_key_events(ship):
    # 监视键盘和鼠标的事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown(ship, event)
        elif event.type == pygame.KEYUP:
            check_keyup(ship, event)

def update_screen(screen, game_settings, ship, bullet):
    # 每次循环时，都重新绘制屏幕颜色
    screen.fill(game_settings.bg_color)
    ship.move_ship()
    ship.display_ship()

    
    bullet.draw_bullet()
    bullet.update()
    

    # 让最近绘制的屏幕可见
    pygame.display.flip()