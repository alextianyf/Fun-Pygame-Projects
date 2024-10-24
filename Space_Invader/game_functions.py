import pygame
import sys
from bullet import Bullet
from alien import Alien

def get_number_aliens_in_a_row(game_settings, alien_width):
    # 获得一行能画多少外星人的数量
    available_space_x = game_settings.WINDOW_WIDTH - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(game_settings, alien_height,ship_height):
    available_space_y = game_settings.WINDOW_HEIGHT - (3*alien_height + ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(screen,game_settings,number,aliens_group,alien_width, alien_height, row_number):
    # 用来创造一个外星人
    alien =Alien(screen, game_settings)
    alien.rect.x = alien_width + 2 * alien_width * number
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens_group.add(alien)

def create_aliens_in_a_row(game_settings, screen, aliens_group, ship):
    # 用来实际画出一行的外星人
    alien =Alien(screen, game_settings)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = ship.rect.height
    number_of_aliens= get_number_aliens_in_a_row(game_settings, alien_width)
    number_rows = get_number_rows(game_settings, alien_height,ship_height)
    for row_number in range(number_rows):
        for number in range(number_of_aliens):
            create_alien(screen,game_settings,number,aliens_group,alien_width,alien_height, row_number)

def fire_bullet(bullets_group,screen,game_settings,ship):
    if len(bullets_group) < game_settings.bullet_num_allowed:
                bullets_group.add(Bullet(screen, game_settings, ship))

def check_keydown(screen, game_settings,ship, bullets_group, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets_group, screen, game_settings,ship)

def check_keyup(ship, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_mouse_key_events(screen, game_settings,ship, bullets_group):
    # 监视键盘和鼠标的事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown(screen, game_settings,ship, bullets_group, event)
        elif event.type == pygame.KEYUP:
            check_keyup(ship, event)

def update_bullet(bullets_group):
    for bullet in bullets_group.sprites():
        bullet.draw_bullet()
        bullet.display_bullet()
    
    for bullet in bullets_group.sprites():
        if bullet.rect.bottom <= 0:
            bullets_group.remove(bullet)
    # Debugging purpose
    #print(len(bullets_group))

def update_screen(screen, game_settings, ship, aliens_group,bullets_group):
    # 每次循环时，都重新绘制屏幕颜色
    screen.fill(game_settings.bg_color)

    # 更新显示ship
    ship.move_ship()
    ship.display_ship()

    # 更新显示bullet
    update_bullet(bullets_group)

    # 更新显示alien
    aliens_group.draw(screen)

    # 让最近绘制的屏幕可见
    pygame.display.flip()