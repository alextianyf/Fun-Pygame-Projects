import sys, pygame
from bullet import Bullet
from aliens import Alien

# 键盘按下检查
def check_keydown_events(event, game_settings, screen, ship, bullets_group):
    if event.key ==pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key ==pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets_group)


def fire_bullet(game_settings, screen, ship, bullets_group):
    if len(bullets_group) < game_settings.num_of_bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets_group.add(new_bullet)

# 键盘松开检查
def check_keyup_events(event, ship):
    if event.key ==pygame.K_RIGHT:
        ship.moving_right = False        
    elif event.key ==pygame.K_LEFT:
        ship.moving_left = False

# 监视键盘和鼠标事件
def check_events(game_settings, screen, ship, bullets_group):

    for event in pygame.event.get():
        # 退出游戏检测
        if event.type == pygame.QUIT:
            sys.exit()
        # player飞船的按键响应
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets_group)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


# 用来更新屏幕
def update_screen(game_settings, screen, ship, aliens_group, bullets_group):
        screen.fill(game_settings.bg_color)

        for bullet in bullets_group.sprites():
            bullet.draw_bullets()
        ship.ship_blit()
        aliens_group.draw(screen)

        # 让最近绘制的屏幕可见，每个while循环都会擦去就屏幕，绘制新屏幕
        pygame.display.flip()

def update_bullets(bullets_group):
    bullets_group.update()

    for bullet in bullets_group.copy():
        if bullet.rect.bottom <= 0:
            bullets_group.remove(bullet)

def create_aliens_group(game_settings, screen, ship, aliens_group):
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(game_settings, alien_width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens_group, alien_number, row_number)

def get_number_aliens_x(game_settings, alien_width):
    available_sapce_x = game_settings.SCREEN_WIDTH - 2 * alien_width
    number_aliens_x = int(available_sapce_x/(2 * alien_width))
    
    return number_aliens_x

def create_alien(game_settings, screen, aliens_group, alien_number, row_number):
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.rect.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens_group.add(alien)

def get_number_rows(game_settings, ship_height, alien_height):
    available_sapce_y = (game_settings.SCREEN_HEIGHT - (3* alien_height)- ship_height) 
    number_rows = int(available_sapce_y / (2*alien_height))
    return number_rows