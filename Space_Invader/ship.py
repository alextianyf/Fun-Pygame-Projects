import pygame

class Ship:
    """
    @Object:

        创建一个飞船类，用以管理飞船所有的属性和动作。
    """
    def __init__(self, display_screen, game_settings):
        self.screen = display_screen
        self.game_settings = game_settings

        # 加载飞船的图像并且设定显示位置
        self.image = pygame.image.load("./Space_Invader/assets/images/player_ship.png")
        self.rect = self.image.get_rect() # 外接矩形
        self.rect.centerx = self.game_settings.WINDOW_WIDTH//2
        self.rect.bottom = self.game_settings.WINDOW_HEIGHT

        # 设置一个移动标志（flag）
        self.moving_right = False
        self.moving_left = False

        self.position = float(self.rect.centerx)

    def move_ship(self):
        if self.moving_right and self.rect.right < self.game_settings.WINDOW_WIDTH:
            self.position += self.game_settings.ship_moving_speed
        if self.moving_left and self.rect.left > 0:
            self.position -= self.game_settings.ship_moving_speed
        
        self.rect.centerx = self.position

    def display_ship(self):
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        self.position = self.game_settings.WINDOW_WIDTH//2