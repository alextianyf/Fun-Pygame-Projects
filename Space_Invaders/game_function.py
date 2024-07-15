import sys, pygame
from bullet import Bullet

# 键盘按下检查
def check_keydown_events(event, game_settings, screen, ship, bullets):
    if event.key ==pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key ==pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)

# 键盘松开检查
def check_keyup_events(event, ship):
    if event.key ==pygame.K_RIGHT:
        ship.moving_right = False        
    elif event.key ==pygame.K_LEFT:
        ship.moving_left = False

# 监视键盘和鼠标事件
def check_events(game_settings, screen, ship, bullets):

    for event in pygame.event.get():
        # 退出游戏检测
        if event.type == pygame.QUIT:
            sys.exit()
        # player飞船的按键响应
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


# 用来更新屏幕
def update_screen(game_settings, screen, ship, bullets):
        screen.fill(game_settings.bg_color)

        for bullet in bullets.sprites():
            bullet.draw_bullets()
        ship.ship_blit()

        # 让最近绘制的屏幕可见，每个while循环都会擦去就屏幕，绘制新屏幕
        pygame.display.flip()

