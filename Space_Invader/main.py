import pygame, random
import sys #system
from setting import Settings

def run_game():
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.WINDOWS_WIDTH, game_settings.WINDOWS_HEIGHT))
    pygame.display.set_caption("Alien Invasion!")

    game_running = True
    while game_running:
        # 监控键盘和鼠标的事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(game_settings.bg_color)

        pygame.display.flip()

run_game()