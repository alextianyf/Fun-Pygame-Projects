import pygame
import sys
from bullet import Bullet
from alien import Alien

def get_number_aliens_in_a_row(game_settings, alien):
    alien_width = alien.rect.width
    available_space_x = game_settings.WINDOW_WIDTH - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x, alien_width

def create_aliens_in_a_row(game_settings, alien, screen, aliens_group):
    number_of_aliens, alien_width= get_number_aliens_in_a_row(game_settings, alien)
    for number in range(number_of_aliens):
        alien = Alien(screen, game_settings)
        alien.rect.x = alien_width + 2 * alien_width * number
        aliens_group.add(alien)

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