import pygame

class Button():

    def __init__(self, game_functions, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # setting button attributes
        self.width, self.height = 200, 50
        self.button_color = (128,128,128)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)

        # create button and place it in the center
        self.rect = pygame.Rect(0,0,self.width, self.height)
        self.rect.center = self.screen_rect.center

        # only create once when creating button object
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)