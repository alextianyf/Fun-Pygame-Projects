import pygame

class Ship():

    def __init__(self, game_settings, screen):
        self.screen = screen

        self.image = pygame.image.load('Space_Invaders/assets/images/player_ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False

        self.game_settings = game_settings


    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.game_settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.game_settings.ship_speed
    
    def ship_blit(self):
        self.screen.blit(self.image, self.rect)