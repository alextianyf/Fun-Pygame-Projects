import pygame
from pygame.sprite import Sprite

# 创建一个属于子弹的类，对于子弹进行管理
class Bullet(Sprite):
    def __init__(self, game_settings, screen, ship):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0,0, game_settings.bullet_width, game_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.color = game_settings.bullet_color
        self.velocity = game_settings.bullet_speed

    def update(self):
        self.rect.y -= self.velocity

    def draw_bullets(self):
        pygame.draw.rect(self.screen, self.color, self.rect)