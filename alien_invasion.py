#包含开发游戏所需的功能
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #初始化游戏并创建一个屏幕对象
    # 初始化背景设置
    pygame.init()
    ai_settings = Settings()
    # 指定游戏窗口的尺寸
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建play按钮
    play_button = Button(ai_settings, screen, "Play")

    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    #创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    #创建一个外星人编组
    aliens = Group()
    #创建一个外星人
    alien = Alien(ai_settings, screen)
    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    #创建存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, play_button, ship,
                 aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        #每次循环时都重绘制屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         bullets, play_button)

run_game()

