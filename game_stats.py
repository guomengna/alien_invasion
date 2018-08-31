class GameStats():
    """跟踪游戏的统计信息"""
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings

        #让游戏刚启动时处于非活动状态
        self.game_active = False
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        # 玩家等级设置
        self.player_level = 1



