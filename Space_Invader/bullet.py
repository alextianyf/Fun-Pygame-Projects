import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,display_screen, game_settings, ship):
        super().__init__()
        self.game_settings = game_settings
        self.screen = display_screen
        self.rect = pygame.Rect(0,0,3,15)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.bullet_position = float(self.rect.y)
    
    def draw_bullet(self):
        pygame.draw.rect(self.screen, (0, 255, 0), self.rect)
