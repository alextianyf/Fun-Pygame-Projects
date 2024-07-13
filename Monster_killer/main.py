import pygame, random
from player import Player
from monster import Monster

pygame.init()

# set windows size
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Killer")

FPS = 60
clock = pygame.time.Clock()

my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

my_monster_group = pygame.sprite.Group()

class Game_control():
    def __init__(self, player, monster_group):
        self.score = 0
        self.font = pygame.font.Font("Monster_killer/Abrushow.ttf", 24)

        self.player = player
        self.monster_group = monster_group

        blue_image = pygame.image.load("Monster_killer/blue_monster.png")
        green_image = pygame.image.load("Monster_killer/green_monster.png")
        purple_image = pygame.image.load("Monster_killer/purple_monster.png")
        yellow_image = pygame.image.load("Monster_killer/yellow_monster.png")

        self.monster_group.add(Monster(150,300, blue_image))
        self.monster_group.add(Monster(400,300, green_image))
        self.monster_group.add(Monster(450,500, purple_image))
        self.monster_group.add(Monster(200,300, yellow_image))
        
    def display(self):
        WHITE = (255,255,255)
        score_text= self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10,10)

        display_surface.blit(score_text, score_rect)
    
    def check_collision(self):
        collide_monsters = pygame.sprite.spritecollide(self.player, self.monster_group, True)
        self.score += len(collide_monsters)



game = Game_control(my_player, my_monster_group)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.warp()

    display_surface.fill((0,0,0))

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_monster_group.update()
    my_monster_group.draw(display_surface)

    game.display()
    game.check_collision()

    pygame.display.update()  
    clock.tick(FPS)

pygame.quit()