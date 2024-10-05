import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,screen,game_settings):
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings

        self.image = pygame.image.load("./Space_Invader/assets/images/alien.png")
        self.rect = self.image.get_rect()

        self.rect.x= 20
        self.rect.y = 20

        self.x = float(self.rect.x)
    
    def display_alien(self):
        self.screen.blit(self.image, self.rect)

