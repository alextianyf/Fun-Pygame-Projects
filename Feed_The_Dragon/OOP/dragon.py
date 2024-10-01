import pygame

class Dragon():
    def __init__(self, game_settings, screen):
        self.game_settings = game_settings
        self.screen = screen
        self.image = pygame.image.load("Feed_The_Dragon/OOP/assets/images/dragon_right.png")
        self.rect = self.image.get_rect()
        self.rect.left = self.game_settings.dragon_x_position
        self.rect.centery = self.game_settings.dragon_y_position

    def show_dragon(self):
        self.screen.blit(self.image,self.rect)