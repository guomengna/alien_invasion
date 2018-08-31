import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from scoreboard import Scoreboard
import random

"""监听事件"""
def check_events(ai_settings, screen, stats, play_button, ship,
                 aliens, bullets):

    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单机play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    sb = Scoreboard(ai_settings, screen, stats)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()

        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏
        stats.reset_stats()
        stats.game_active = True

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #闯将一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        update_screen(ai_settings, screen, stats, sb, ship, aliens,
                          bullets, play_button)
        update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

def update_screen(ai_settings, screen, stats, sb, ship, aliens,
                  bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环时都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所有的子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #显示飞船
    ship.blitme()
    #显示外星人
    #alien.blitme()
    #显示一群外星人
    aliens.draw(screen)

    #显示得分
    sb.prep_score()
    sb.prep_level()
    sb.show_score()

    #如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()

def check_keyup_events(event, ship):
    """响应松开按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按下按键"""
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        #按q键退出
        sys.exit()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已经消失的子弹"""
    #更新子弹的位置
    bullets.update()

    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    #检查是否有子弹击中了外星人
    #如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_point
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        #清空屏幕上的所有子弹
        bullets.empty()
        sleep_time = random.uniform(1, 4)
        sleep(sleep_time)
        print(sleep_time)
        #删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        #增加玩家的等级
        stats.player_level += 1
        sb.prep_level()
        print("level = " + str(stats.player_level))
        sb.show_score()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

"""创建外星人群"""
def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    print("number_rows = " + str(number_rows))
    #随机产生rows_build_speed_factor到number_rows排外星人
    rows = random.randint(ai_settings.rows_build_speed_factor, number_rows)
    print("rows = "+str(rows))
    #每行随机产生从multialiens_build_speed_factor到number_aliens_x个外星人
    multi_alien = random.randint(ai_settings.multialiens_build_speed_factor, number_aliens_x)
    print("multi_alien = " + str(multi_alien))
    #创建第一个外星人
    for row_number in range(rows):
        for alien_number in range(multi_alien):
            create_aliens(ai_settings, screen, aliens,
                          alien_number, row_number)

#一行中可容纳的外星人数量，外星人间距为外星人宽度
def get_number_aliens_x(ai_settings, alien_width):
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x

def create_aliens(ai_settings, screen, aliens, alien_number, row_number):
    # 创建一个外星人并加入当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)

"""计算屏幕上可以容纳多少行外星人"""
def get_number_rows(ai_settings, ship_height, alien_height):
    avaliable_space_y = (ai_settings.screen_height -
                         (3 * alien_height)-ship_height)
    number_rows = int(avaliable_space_y / (2 * alien_height))
    return number_rows

#更新外星人位置
"""检查是否有外星人位于屏幕边缘，并改变他们的方向"""
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    """检查是否有外星人和飞船之间的碰撞"""
    if pygame.sprite.spritecollideany(ship, aliens):
        print("ship hit!!")
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将郑群外星人下移，并改变运动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应外星人撞到飞船"""
    sb = Scoreboard(ai_settings, screen, stats)
    if stats.ships_left > 0:
        #将ship_left减1
        stats.ships_left -= 1

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #清空记分
        #stats.score = 0
        stats.player_level = 1
        sb.prep_score()
        sb.prep_level()
        sb.show_score()

        #创建一群新的外星人，并将飞船放在屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #暂停
        sleep_time = random.uniform(1, 5)
        sleep(sleep_time)
        print(sleep_time)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect =screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船呗撞到一样处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break;

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """响应子弹和外星人发生碰撞"""
    #删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_point
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens):
        #删除现有的子弹，加快游戏节奏，并创建一群新的外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats, sb):
    """是否产生了最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()



