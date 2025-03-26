import pygame, random

pygame.init()

WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Clown")

# Load images
background_image = pygame.image.load("Catch_the_Clone/background.png") # 加载图片
background_rect = background_image.get_rect() # 获取盛放图片的矩形容器
background_rect.topleft = (0, 0) # 把容器放在窗口左上角

clown_image = pygame.image.load("Catch_the_Clone/clown.png")
clown_rect = clown_image.get_rect() 
clown_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

# Load text
BLUE = (1, 175, 209)
YELLOW = (248, 231, 28)
font = pygame.font.Font("Catch_the_Clone/Franxurter.ttf", 32)

title_text = font.render("Catch the Clown", True, BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (50, 10)

running = True

while running:
    for behavior in pygame.event.get():

        if behavior.type == pygame.QUIT:
            running = False

        if behavior.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = behavior.pos[0]
            mouse_y = behavior.pos[1]
            print(mouse_x, mouse_y)
    
    display_surface.blit(background_image, background_rect)
    display_surface.blit(clown_image, clown_rect)
    display_surface.blit(title_text, title_rect)

    pygame.display.update()

pygame.quit()