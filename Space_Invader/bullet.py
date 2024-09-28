from typing import Any
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,display_screen, game_settings, ship):
        super().__init__()
        self.game_settings = game_settings
        self.screen = display_screen
        self.rect = pygame.Rect(0,0,self.game_settings.bullet_width,self.game_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        self.bullet_y_position = float(self.rect.y)
    
    def display_bullet(self):
        self.bullet_y_position -= self.game_settings.bullet_speed
        self.rect.y = self.bullet_y_position

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.game_settings.bullet_color, self.rect)
