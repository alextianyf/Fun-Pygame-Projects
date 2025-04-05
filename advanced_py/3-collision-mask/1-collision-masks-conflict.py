import pygame
#Use 2D vectors
vector = pygame.math.Vector2

#Initialize pygame
pygame.init()

#Set display surface
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Making a tile map!")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Define classes
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        if image_int == 1:
            self.image = pygame.image.load("./advanced_py/assets/dirt.png")
        elif image_int == 2:
            self.image = pygame.image.load("./advanced_py/assets/grass.png")
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load("./advanced_py/assets/water.png")
            sub_group.add(self)

        # 添加蓝色边框以观察碰撞边界
        pygame.draw.rect(self.image, (0, 0, 255), self.image.get_rect(), 1)

        main_group.add(self)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()

        self.move_right_sprites = self.load_images("./advanced_py/assets/boy", "Run", 8)
        self.move_left_sprites = [pygame.transform.flip(s, True, False) for s in self.move_right_sprites]
        for img in self.move_left_sprites:
            pygame.draw.rect(img, (0, 0, 255), img.get_rect(), 1)

        self.idle_right_sprites = self.load_images("./advanced_py/assets/boy", "Idle", 8)
        self.idle_left_sprites = [pygame.transform.flip(s, True, False) for s in self.idle_right_sprites]
        for img in self.idle_left_sprites:
            pygame.draw.rect(img, (0, 0, 255), img.get_rect(), 1)

        self.current_sprite = 0
        self.image = self.idle_right_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.facing_right = True
        self.starting_x = x
        self.starting_y = y

        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles

        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        self.HORIZONTAL_ACCELERATION = 1
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCLERATION = 0.5
        self.VERTICAL_JUMP_SPEED = 15

    def load_images(self, folder, prefix, count):
        frames = []
        for i in range(1, count + 1):
            img = pygame.transform.scale(
                pygame.image.load(f"{folder}/{prefix} ({i}).png"), (64, 64)
            )
            pygame.draw.rect(img, (0, 0, 255), img.get_rect(), 1)  # 添加蓝色边框
            frames.append(img)
        return frames

    def update(self):
        self.move()
        self.check_collisions()

    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -self.HORIZONTAL_ACCELERATION
            self.facing_right = False
            self.animate(self.move_left_sprites, 0.2)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.facing_right = True
            self.animate(self.move_right_sprites, 0.2)
        else:
            if self.facing_right:
                self.animate(self.idle_right_sprites, 0.2)
            else:
                self.animate(self.idle_left_sprites, 0.2)

        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        collided_platforms = pygame.sprite.spritecollide(self, self.grass_tiles, False)
        if collided_platforms and self.velocity.y > 0:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0

        if pygame.sprite.spritecollide(self, self.water_tiles, False):
            print("YOU CAN'T SWIM!!!")
            self.position = vector(self.starting_x, self.starting_y)
            self.velocity = vector(0, 0)

    def jump(self):
        if pygame.sprite.spritecollide(self, self.grass_tiles, False):
            self.velocity.y = -self.VERTICAL_JUMP_SPEED

    def animate(self, sprite_list, speed):
        self.current_sprite = (self.current_sprite + speed) % len(sprite_list)
        self.image = sprite_list[int(self.current_sprite)]


#Create sprite groups
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()

#Tile map
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

#Create Tile and Player objects
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

#Background
background_image = pygame.image.load("./advanced_py/assets/background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

#Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            my_player.jump()

    display_surface.blit(background_image, background_rect)
    main_tile_group.draw(display_surface)
    my_player_group.update()
    my_player_group.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()