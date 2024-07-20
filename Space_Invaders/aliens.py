import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, game_settings, screen):
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings

        self.image = pygame.image.load('Space_Invaders/assets/images/alien.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def alien_blit(self):
        self.screen.blit(self.image, self.rect)
