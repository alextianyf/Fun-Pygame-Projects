import pygame, random

pygame.init()

WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Clown")

running = True

while running:
    for behavior in pygame.event.get():

        if behavior.type == pygame.QUIT:
            running = False

        if behavior.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = behavior.pos[0]
            mouse_y = behavior.pos[1]
            print(mouse_x, mouse_y)

pygame.quit()