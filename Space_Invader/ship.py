import pygame
from settings import game_settings

class Ship:
    """
    @Object:

        创建一个飞船类，用以管理飞船所有的属性和动作。
    """
    def __init__(self, display_screen):
        self.screen = display_screen

        # 加载飞船的图像并且设定显示位置
        self.image = pygame.image.load("./Space_Invader/assets/images/player_ship.png")
        self.rect = self.image.get_rect() # 外接矩形
        self.rect.center = (game_settings.WINDOW_WIDTH//2, (game_settings.WINDOW_HEIGHT-35))

    def display_ship(self):
        self.screen.blit(self.image, self.rect)