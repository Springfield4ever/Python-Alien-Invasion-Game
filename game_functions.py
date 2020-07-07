import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from sound import Sound

def start_game(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #重置游戏设置
    ai_settings.initialize_dynamic_settings()
    #隐藏光标
    pygame.mouse.set_visible(False)
    #重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    #重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    #清空子弹和外星人列表
    aliens.empty()
    bullets.empty()
    #创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()

def check_keydown_events(event,ai_settings,screen,stats,sb,ship,aliens,bullets,sound):
    '''响应按下'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #创建一颗子弹，并将其加入到编组bullets中
        fire_bullet(ai_settings,screen,ship,bullets,sound)
    elif event.key == pygame.K_q:
        sb.save_high_score()
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings,screen,stats,sb,ship,aliens,bullets)
def check_keyup_events(event,ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    '''让玩家在单击Play按钮时开始新游戏'''
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,sound):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sb.save_high_score()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,stats,sb,ship,aliens,bullets,sound)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    '''更新屏幕上的图像，并切换到新屏幕'''
    #每次循环时都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重新绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #显示得分
    sb.show_score()
    #如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    
    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,sound):
    '''更新子弹的位置，并删除已经消失的子弹'''
    #更新子弹的位置
    bullets.update()
    
    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets,sound)
    
def check_high_score(stats,sb):
    '''检查是否诞生了新的最高分'''
    if stats.score > stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets,sound):
    '''响应子弹和外星人的碰撞'''
    #检查是否有子弹击中了外星人；如果击中，就删除相应的子弹和外星人
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        sound.play_score()
        check_high_score(stats,sb)
    #如果外星人编队被清空，就删除现有的子弹，加快现有的游戏节奏，并新建一群外星人
    if len(aliens)==0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sound.play_level_up()
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)

def fire_bullet(ai_settings,screen,ship,bullets,sound):
    '''如果没有达到上限，就发射一颗子弹'''
    #创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet=Bullet(ai_settings,screen,ship)
        sound.play_laser()
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings,alien_width):
    '''计算每行可容纳多少个外星人'''
    available_space_x=ai_settings.screen_width-2*alien_width
    number_aliens_x=int(available_space_x/(2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    '''创建一个外星人并将其放在当前行'''
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien.x=alien_width+2*alien_width*alien_number
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    '''创建外星人群'''
    #创建一个外星人，并计算每行可容纳多少个外星人
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets,sound):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left>0:
        #飞船命数-1
        stats.ships_left -= 1
        sound.play_fail()
        #更新记分牌
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放置在屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets,sound):
    '''检测是否有外星人到达了屏幕底端'''
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞一样进行处理
            ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets,sound)
            break

def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets,sound):
    '''检查是否有外星人位于屏幕边缘，并更新外星人编队的位置'''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #监测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets,sound)
    #检查是否有外星人到达了屏幕底端
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets,sound)

def check_fleet_edges(ai_settings,aliens):
    '''当有外星人到达边缘时采取相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    '''将整群外星人下移，并改变它们的方向'''
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
        alien.play_animation()
    ai_settings.fleet_direction *= -1