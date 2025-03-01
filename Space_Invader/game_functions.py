import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep

def get_number_aliens_in_a_row(game_settings, alien_width):
    # 获得一行能画多少外星人的数量
    available_space_x = game_settings.WINDOW_WIDTH - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(game_settings, alien_height,ship_height):
    available_space_y = game_settings.WINDOW_HEIGHT - (3*alien_height + ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(screen, game_settings, x_position, y_position, aliens_group):
    # Create an alien and set its position
    alien = Alien(screen, game_settings, x_position, y_position)
    aliens_group.add(alien)

def create_alien_grid(game_settings, screen, aliens_group, ship):
    alien =Alien(screen, game_settings)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = ship.rect.height

    number_of_aliens= get_number_aliens_in_a_row(game_settings, alien_width)
    number_rows = get_number_rows(game_settings, alien_height,ship_height)

    for row_number in range(number_rows):
        for alien_number in range(number_of_aliens):
            x_position = alien_width + 2 * alien_width * alien_number
            y_position = alien_height + 2 * alien_height * row_number
            create_alien(screen, game_settings, x_position, y_position, aliens_group)

def change_alien_grid_direction(aliens_group):
    for alien in aliens_group.sprites():
        alien.rect.y += alien.drop_speed
        alien.direction *= -1

def check_alien_grid_hit_edge(aliens_group):
    for alien in aliens_group.sprites():
        if alien.hit_edges():
            change_alien_grid_direction(aliens_group)
            break

def fire_bullet(bullets_group,screen,game_settings,ship, sounds):
    if len(bullets_group) < game_settings.bullet_num_allowed:
                sounds.play_fire_sound()
                bullets_group.add(Bullet(screen, game_settings, ship))

def check_keydown(screen, game_settings,ship, bullets_group, event, sounds):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets_group, screen, game_settings,ship, sounds)

def check_keyup(ship, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_mouse_key_events(screen, game_settings,ship, bullets_group, stats, play_button, aliens_group, score,sounds):
    # 监视键盘和鼠标的事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown(screen, game_settings,ship, bullets_group, event, sounds)
        elif event.type == pygame.KEYUP:
            check_keyup(ship, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(screen, game_settings,ship, bullets_group, stats, play_button, aliens_group, mouse_x, mouse_y,score)

def check_play_button(screen, game_settings,ship, bullets_group, stats, play_button, aliens_group, mouse_x, mouse_y, score):
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)

    if button_clicked and not stats.game_active:
        game_settings.init_dynamic_settings()
        pygame.mouse.set_visible(False)

        if play_button.rect.collidepoint(mouse_x, mouse_y):
            stats.reset_stats()
            stats.game_active = True

            score.prep_score()
            score.prep_high_score()
            score.prep_level()
            score.prep_ships()

            aliens_group.empty()
            bullets_group.empty()

            create_alien_grid(game_settings, screen, aliens_group, ship)
            ship.center_ship()

def check_high_score(stats, score):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()

def check_bullet_alien_collisions(game_settings, screen, bullets_group, aliens_group, ship, stats, score, sounds):
    collisions = pygame.sprite.groupcollide(bullets_group, aliens_group,True, True)
    if collisions:
        # 如果检测到子弹击中alien，且希望增加分数或更新其他内容
        # 不改变alien_speed
        for aliens_group in collisions.values():
            sounds.play_alien_hit_sound()
            stats.score += game_settings.alien_points
            score.prep_score()
        check_high_score(stats, score)
    
    if len(aliens_group) <= 0:
        bullets_group.empty()
        game_settings.increase_speed()

        # level up
        stats.level += 1
        score.prep_level()

        create_alien_grid(game_settings, screen, aliens_group, ship)

def check_ship_aliens_collision(game_settings, aliens_group, bullets_group, ship,stats, screen, score, sounds):
    if pygame.sprite.spritecollideany(ship, aliens_group):
        ship_hit(game_settings, stats, aliens_group, bullets_group, ship, screen, score, sounds)

def ship_hit(game_settings, stats, aliens_group, bullets_group, ship, screen, score, sounds):
    if stats.player_life_remain > 1:
        stats.player_life_remain -= 1

        sounds.play_fail_sound()
        score.prep_ships()
        aliens_group.empty()
        bullets_group.empty()

        if len(aliens_group) == 0:
            create_alien_grid(game_settings, screen, aliens_group, ship)
            ship.center_ship()

        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(game_settings, stats, aliens_group, bullets_group, ship, screen, score, sounds):
    screen_rect = screen.get_rect()
    for alien in aliens_group.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            sounds.play_fail_sound()
            ship_hit(game_settings, stats, aliens_group, bullets_group, ship, screen, score, sounds)
            break # if any reach bottom, then break, which don't need to complete the for loop

def update_bullets(game_settings,screen,aliens_group, bullets_group, ship, stats, score, sounds):
    for bullet in bullets_group.sprites():
        bullet.draw_bullet()
        bullet.display_bullet()
    
    for bullet in bullets_group.sprites():
        if bullet.rect.bottom <= 0:
            bullets_group.remove(bullet)
    # Debugging purpose
    #print(len(bullets_group))
    check_bullet_alien_collisions(game_settings, screen, bullets_group, aliens_group, ship, stats, score, sounds)

def update_screen(screen, game_settings, ship, aliens_group,bullets_group, stats, score, sounds):
    # 每次循环时，都重新绘制屏幕颜色
    screen.fill(game_settings.bg_color)
    score.show_score()

    # 更新显示ship
    ship.move_ship()
    ship.display_ship()

    # 更新显示bullet
    update_bullets(game_settings, screen, aliens_group, bullets_group, ship, stats, score, sounds)

    # 更新显示alien
    check_alien_grid_hit_edge(aliens_group)
    check_ship_aliens_collision(game_settings, aliens_group, bullets_group, ship, stats, screen, score, sounds)
    check_aliens_bottom(game_settings, stats, aliens_group, bullets_group, ship, screen, score, sounds)
    aliens_group.update()
    aliens_group.draw(screen)

    # 让最近绘制的屏幕可见
    pygame.display.flip()