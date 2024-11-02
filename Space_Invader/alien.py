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
        self.direction = 1
        self.drop_speed = 10
    
    def display_alien(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        self.alien_position += 0.6 * self.direction
        self.rect.x = self.alien_position
    
    def check_edges(self):
        pass

