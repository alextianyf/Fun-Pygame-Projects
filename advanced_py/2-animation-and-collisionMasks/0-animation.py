import pygame
#Use 2D vectors
vector = pygame.math.Vector2

#Initialize pygame
pygame.init()

#Set display surface (tile size is 32x32 so 960/32 = 30 tiles wide, 640/32 = 20 tiles high)
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Making a tile map!")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Define classes
class Tile(pygame.sprite.Sprite):
    """A class to read and create individual tiles and place them in the display"""

    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        #Load in the correct image and add it to the correct sub groups
        if image_int == 1:
            self.image = pygame.image.load("./advanced_py/assets/dirt.png")
        elif image_int == 2:
            self.image = pygame.image.load("./advanced_py/assets/grass.png")
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load("./advanced_py/assets/water.png")
            sub_group.add(self)
        
        #Add every tile to the main tile group
        main_group.add(self)

        #Get the rect of the image and position within the grid
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Player(pygame.sprite.Sprite):
    """玩家类：可以移动、跳跃、播放动画，并与地面和水体碰撞"""

    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()

        # --- 动画帧列表 ---
        self.move_right_sprites = self.load_images("./advanced_py/assets/boy", "Run", 8)    # 向右跑步帧
        self.move_left_sprites = [pygame.transform.flip(s, True, False) for s in self.move_right_sprites]  # 向左跑步帧（翻转）

        self.idle_right_sprites = self.load_images("./advanced_py/assets/boy", "Idle", 8)   # 向右待机帧
        self.idle_left_sprites = [pygame.transform.flip(s, True, False) for s in self.idle_right_sprites]  # 向左待机帧（翻转）

        # --- 初始图像与位置 ---
        self.current_sprite = 0                    # 当前帧索引（可为小数）
        self.image = self.idle_right_sprites[0]    # 初始图像
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        # --- 状态管理 ---
        self.facing_right = True     # 是否面朝右侧
        self.starting_x = x
        self.starting_y = y

        # --- 碰撞目标 ---
        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles

        # --- 向量运动模型 ---
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        # --- 运动常数 ---
        self.HORIZONTAL_ACCELERATION = 1
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCLERATION = 0.5       # 重力
        self.VERTICAL_JUMP_SPEED = 15         # 跳跃速度

    def load_images(self, folder, prefix, count):
        """
        批量加载并缩放动画帧
        folder: 子文件夹名 (如 "boy")
        prefix: 文件名前缀 (如 "Run")
        count: 帧数量
        """
        return [
            pygame.transform.scale(
                pygame.image.load(f"{folder}/{prefix} ({i}).png"), (64, 64)
            ) for i in range(1, count + 1)
        ]

    def update(self):
        self.move()
        self.check_collisions()

    def move(self):
        # 初始加速度只考虑重力
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

        # 摩擦力计算
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION

        # 更新速度和位置（基本运动学公式）
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # 屏幕左右循环
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        # 更新图像位置
        self.rect.bottomleft = self.position

    def check_collisions(self):
        # 与草地碰撞检测
        collided_platforms = pygame.sprite.spritecollide(self, self.grass_tiles, False)
        if collided_platforms and self.velocity.y > 0:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0

        # 与水体碰撞（重置位置）
        if pygame.sprite.spritecollide(self, self.water_tiles, False):
            print("YOU CAN'T SWIM!!!")
            self.position = vector(self.starting_x, self.starting_y)
            self.velocity = vector(0, 0)

    def jump(self):
        # 仅允许在草地上跳跃
        if pygame.sprite.spritecollide(self, self.grass_tiles, False):
            self.velocity.y = -self.VERTICAL_JUMP_SPEED

    def animate(self, sprite_list, speed):
        """
        播放指定动画帧列表
        sprite_list: 图像帧序列
        speed: 帧切换速度（建议 0.1 ~ 0.3）
        """
        self.current_sprite = (self.current_sprite + speed) % len(sprite_list)
        self.image = sprite_list[int(self.current_sprite)]


#Create sprite groups
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()

#Create the tile map: 0 -> no tile, 1 -> dirt, 2 -> grass, 3 -> water, 4 -> player
#20 rows and 30 columns
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

#Create individual Tile objects from the tile map
#Loop through the 20 lists in tile_map (i moves us down the map)
for i in range(len(tile_map)):
    #Loop through the 30 elements in a given list (j moves us across the map)
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

#Load in a background image
background_image = pygame.image.load("./advanced_py/assets/background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

#The main game loop
running = True
while running:
    #Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Player wants to jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()

    #Blit the background
    display_surface.blit(background_image, background_rect)

    #Draw tiles
    main_tile_group.draw(display_surface)

    #Update and draw sprites
    my_player_group.update()
    my_player_group.draw(display_surface)

    #Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()