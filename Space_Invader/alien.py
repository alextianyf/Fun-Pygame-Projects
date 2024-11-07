import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, screen, game_settings, x_position=0, y_position=0):
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings

        self.image = pygame.image.load("./Space_Invader/assets/images/alien.png")
        self.rect = self.image.get_rect()

        self.rect.x = x_position
        self.rect.y = y_position

        self.alien_position = float(self.rect.x)
        self.direction = self.game_settings.alien_init_direction
        self.drop_speed = self.game_settings.alien_drop_speed
    
    def display_alien(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        self.alien_position += self.game_settings.alien_speed * self.direction
        self.rect.x = self.alien_position
    
    def hit_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

