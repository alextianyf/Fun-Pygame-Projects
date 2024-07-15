class Settings():
    # 我们用这个class来储存游戏中所有的设置
    def __init__(self):

        # screen的长宽设置
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        
        # 设置背景颜色
        self.bg_color = (0,0,0)

        # 设置飞船的速度
        self.ship_speed = 1

        # 设置子弹
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,255,255)

