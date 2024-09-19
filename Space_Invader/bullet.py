import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,display_screen, game_settings, ship):
        super(self).__init__()
        self.screen = display_screen
        self.rect = pygame.Rect(0,0,3,15)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.bullet_position = float(self.rect.y)
