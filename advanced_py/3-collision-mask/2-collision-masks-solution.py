import pygame
# Use 2D vectors
vector = pygame.math.Vector2

# Initialize pygame
pygame.init()

# Set display surface (tile size is 32x32 so 960/32 = 30 tiles wide, 640/32 = 20 tiles high)
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Making a tile map!")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Define classes
class Tile(pygame.sprite.Sprite):
    """A class to read and create individual tiles and place them in the display"""

    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        if image_int == 1:
            self.image = pygame.image.load("./advanced_py/assets/dirt.png")
        elif image_int == 2:
            self.image = pygame.image.load("./advanced_py/assets/grass.png")
            self.mask = pygame.mask.from_surface(self.image)
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load("./advanced_py/assets/water.png")
            sub_group.add(self)

        main_group.add(self)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pygame.draw.rect(display_surface, (0, 0, 255), self.rect, 1)


class Player(pygame.sprite.Sprite):
    """A player class the user can control"""

    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()

        self.move_right_sprites, self.move_right_masks = self.load_images("./advanced_py/assets/boy", "Run", 8)
        self.move_left_sprites, self.move_left_masks = self.flip_images(self.move_right_sprites)
        self.idle_right_sprites, self.idle_right_masks = self.load_images("./advanced_py/assets/boy", "Idle", 8)
        self.idle_left_sprites, self.idle_left_masks = self.flip_images(self.idle_right_sprites)

        self.current_sprite = 0
        self.image = self.move_right_sprites[self.current_sprite]
        self.mask = self.move_right_masks[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.starting_x = x
        self.starting_y = y
        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles

        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCLERATION = .5
        self.VERTICAL_JUMP_SPEED = 15

    def load_images(self, folder, prefix, count):
        sprites = []
        masks = []
        for i in range(1, count + 1):
            path = f"{folder}/{prefix} ({i}).png"
            sprite = pygame.transform.scale(pygame.image.load(path), (64, 64))
            sprites.append(sprite)
            masks.append(pygame.mask.from_surface(sprite))
        return sprites, masks

    def flip_images(self, sprite_list):
        flipped_sprites = []
        flipped_masks = []
        for sprite in sprite_list:
            flipped = pygame.transform.flip(sprite, True, False)
            flipped_sprites.append(flipped)
            flipped_masks.append(pygame.mask.from_surface(flipped))
        return flipped_sprites, flipped_masks

    def update(self):
        pygame.draw.rect(display_surface, (255, 255, 0), self.rect, 1)
        self.move()
        self.check_collisions()

    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, self.move_left_masks, 0.2)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, self.move_right_masks, 0.2)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, self.idle_right_masks, 0.2)
            else:
                self.animate(self.idle_left_sprites, self.idle_left_masks, 0.2)

        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        '''
        这一行使用了 pygame.sprite.collide_mask 而不是简单的 collide_rect。
		collide_mask 是 基于精确像素的不透明区域碰撞检测。
		这样即使角色的 rect 与平台有重叠，只要实际图片透明部分没碰到，就不会算作“站在平台上”。
        '''
        collided_platforms = pygame.sprite.spritecollide(self, self.grass_tiles, False, pygame.sprite.collide_mask)
        if collided_platforms:
            if self.velocity.y > 0:
                self.position.y = collided_platforms[0].rect.top + 10
                self.velocity.y = 0

        if pygame.sprite.spritecollide(self, self.water_tiles, False, pygame.sprite.collide_mask):
            print("YOU CANT SWIM!!!")
            self.position = vector(self.starting_x, self.starting_y)
            self.velocity = vector(0, 0)

    def jump(self):
        if pygame.sprite.spritecollide(self, self.grass_tiles, False, pygame.sprite.collide_mask):
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED

    def animate(self, sprite_list, mask_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        index = int(self.current_sprite)
        self.image = sprite_list[index]
        self.mask = mask_list[index]


# Create sprite groups
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()

# Tile map layout
# 0 = empty, 1 = dirt, 2 = grass, 3 = water, 4 = player
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1]
]

# Create tiles and player from map
for i in range(len(tile_map)):
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1:
            Tile(j*32, i*32, 1, main_tile_group)
        elif tile_map[i][j] == 2:
            Tile(j*32, i*32, 2, main_tile_group, grass_tile_group)
        elif tile_map[i][j] == 3:
            Tile(j*32, i*32, 3, main_tile_group, water_tile_group)
        elif tile_map[i][j] == 4:
            my_player = Player(j*32, i*32 + 32, grass_tile_group, water_tile_group)
            my_player_group.add(my_player)

# Load background
background_image = pygame.image.load("./advanced_py/assets/background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()

    display_surface.blit(background_image, background_rect)
    main_tile_group.draw(display_surface)
    main_tile_group.update()
    my_player_group.update()
    my_player_group.draw(display_surface)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()