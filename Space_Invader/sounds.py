import pygame

class Sounds():

    def __init__(self, path):
        self.enter_sound = pygame.mixer.Sound(path+'intro.wav')
        self.fire_sound = pygame.mixer.Sound(path+'fire.wav')
        self.alien_hit_sound = pygame.mixer.Sound(path+'alien_hit.wav')
        self.fail_sound = pygame.mixer.Sound(path+'fail.wav')

    def play_enter_sound(self):
        self.enter_sound.play()
    
    def play_fire_sound(self):
        self.fire_sound.play()
    
    def play_alien_hit_sound(self):
        self.alien_hit_sound.play()
    
    def play_fail_sound(self):
        self.fail_sound.play()