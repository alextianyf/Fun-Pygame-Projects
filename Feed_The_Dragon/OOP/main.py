import pygame
from settings import game_settings
from dragon import Dragon

def run_game():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((game_settings.WINDOW_WIDTH, game_settings.WINDOW_HEIGHT))
    pygame.display.set_caption(game_settings.game_title)
    clock = pygame.time.Clock()# get clock for FPS

    # Creating a dragon object
    dragon = Dragon(game_settings, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        dragon.show_dragon()
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(game_settings.FPS)  

    pygame.quit()

run_game()