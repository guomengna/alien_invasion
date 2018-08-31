#设置类
class Settings():
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #飞船的设置
        #self.ship_speed_factor = 1.5
        self.ship_limit = 2#每次游戏有三条命

        #子弹设置
        #self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 200, 120, 10
        #允许同时存在的子弹数目
        self.bullets_allowed = 30

        #外星人设置
        #self.alien_speed_factor = 20
        self.fleet_drop_speed = 10
        #fleet_direction = 1表示向右移动，fleet_direction = -1表示向左移动
        #self.fleet_direction = 1

        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        #外星人点数提高
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        #产生的排数增加的速度
        self.rows_build_scale = 1.5
        #每排产生外星人增加的速度
        self.multialiens_build_scale = 1.5


    def initialize_dynamic_settings(self):
        """初始化随游戏进行变化的速度"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.rows_build_speed_factor = 1
        self.multialiens_build_speed_factor = 1


        # fleet_direction = 1表示向右移动，fleet_direction = -1表示向左移动
        self.fleet_direction = 1

        #记分
        self.alien_point = 50

    """提高速度"""
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_point = int(self.alien_point * self.score_scale)
        self.rows_build_speed_factor = int(self.rows_build_speed_factor * self.rows_build_scale)
        self.multialiens_build_speed_factor = int(self.multialiens_build_speed_factor * self.multialiens_build_scale)
        print(self.alien_point)

