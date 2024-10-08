class Settings:
    """
    @Object(目的):

        储存游戏里所有的设置

    """

    # 初始化游戏的设置
    def __init__(self):

        # 屏幕尺寸的设置
        self.WINDOW_WIDTH = 1200
        self.WINDOW_HEIGHT = 800

        # 背景颜色的设置
        self.bg_color = (0,0,0)

        # 设置飞船移动速度
        self.ship_moving_speed = 0.5

        # 设置bullet
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_speed = 0.3
        self.bullet_color = (0,255,0)
        self.bullet_num_allowed = 8

game_settings = Settings()