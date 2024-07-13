import pygame, random
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

class Monster(pygame.sprite.Sprite):

    def __init__(self, x, y, image) :
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.velocity = random.randint(1,9)
        self.x_direction = random.choice([-1, 1])
        self.y_direction = random.choice([-1, 1])
    
    def update(self):
        self.rect.x += self.x_direction * self.velocity
        self.rect.y += self.y_direction * self.velocity

        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.x_direction = -1 * self.x_direction

        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.y_direction = -1 * self.y_direction