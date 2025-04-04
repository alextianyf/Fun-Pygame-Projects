import pygame  # 导入 pygame 模块
pygame.init()  # 初始化 pygame 所有子模块

# 向量运算（便于实现物理运动：加速度、速度、位置）
vector = pygame.math.Vector2

# 屏幕尺寸设置
WINDOW_WIDTH = 960  # 宽度 960 像素
WINDOW_HEIGHT = 640  # 高度 640 像素
TILE_SIZE = 32  # 每一个 tile（瓦片）的像素大小为 32x32
FPS = 60  # 每秒帧率设置为 60，控制刷新速度

# 创建显示窗口，大小为 (960, 640)
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tilemap with Player Movement")  # 设置窗口标题
clock = pygame.time.Clock()  # 创建时钟对象，用于控制帧率

# 加载图片资源，返回的是 Surface 对象
dirt_img = pygame.image.load("./advanced_py/assets/dirt.png")  # 泥土图块
grass_img = pygame.image.load("./advanced_py/assets/grass.png")  # 草地图块
water_img = pygame.image.load("./advanced_py/assets/water.png")  # 水图块
knight_img = pygame.image.load("./advanced_py/assets/knight.png")  # 骑士角色图像
background_img = pygame.image.load("./advanced_py/assets/background.png")  # 背景图像
background_rect = background_img.get_rect(topleft=(0, 0))  # 获取背景图像的矩形区域，并设定左上角为 (0, 0)

# 定义 Tile 类，继承自 pygame.sprite.Sprite，用于创建地图瓦片
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type, all_tiles, special_group=None):
        super().__init__()  # 初始化父类
        # tile_type 是瓦片类型，决定显示哪张图片
        if tile_type == 1:
            self.image = dirt_img  # 泥土
        elif tile_type == 2:
            self.image = grass_img  # 草地
            special_group.add(self)  # 加入特殊组（grass_tiles）
        elif tile_type == 3:
            self.image = water_img  # 水
            special_group.add(self)  # 加入特殊组（water_tiles）

        self.rect = self.image.get_rect(topleft=(x, y))  # 设置瓦片位置
        all_tiles.add(self)  # 把这个 tile 加入总瓦片组中

# 定义玩家类，继承自 Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # 初始化父类
        self.image = knight_img  # 使用骑士图像
        self.rect = self.image.get_rect(bottomleft=(x, y))  # 设置初始位置（角色脚落点）

        self.position = vector(x, y)  # 玩家当前位置（向量）
        self.velocity = vector(0, 0)  # 初始速度为 0
        self.acceleration = vector(0, 0)  # 初始加速度为 0

        self.HORIZONTAL_ACCELERATION = 2  # 水平方向加速度大小
        self.HORIZONTAL_FRICTION = 0.15  # 水平方向摩擦力

    def update(self):
        self.acceleration = vector(0, 0)  # 每次更新先重置加速度
        keys = pygame.key.get_pressed()  # 获取当前按键状态
        if keys[pygame.K_LEFT]:  # 如果按左键
            self.acceleration.x = -self.HORIZONTAL_ACCELERATION  # 加速度设为负值
        if keys[pygame.K_RIGHT]:  # 如果按右键
            self.acceleration.x = self.HORIZONTAL_ACCELERATION  # 加速度为正值

        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION  # 应用摩擦力：越快摩擦越大
        self.velocity += self.acceleration  # 更新速度 = 原速度 + 加速度
        self.position += self.velocity + 0.5 * self.acceleration  # 更新位置（用经典加速度公式）
        self.rect.bottomleft = self.position  # 更新角色位置

# 创建所有精灵组
all_tiles = pygame.sprite.Group()  # 所有 tile 的组
grass_tiles = pygame.sprite.Group()  # 草地组
water_tiles = pygame.sprite.Group()  # 水组
player_group = pygame.sprite.Group()  # 玩家组（这里只有一个玩家）

# tile_map 是地图布局数据（二维列表）：0=空格，1=泥土，2=草地，3=水，4=玩家
# 地图有 20 行，30 列（对应窗口大小 / TILE_SIZE = 640/32 行, 960/32 列）
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1]
]

# 遍历 tile_map，逐格创建对应的 Tile 或 Player 实例
for i, row in enumerate(tile_map):  # i 表示行号（纵向），row 是一整行
    for j, value in enumerate(row):  # j 表示列号（横向），value 是该格子数值
        x, y = j * TILE_SIZE, i * TILE_SIZE  # 把格子索引换算成像素位置
        if value == 1:
            Tile(x, y, 1, all_tiles)  # 创建泥土 tile
        elif value == 2:
            Tile(x, y, 2, all_tiles, grass_tiles)  # 创建草地 tile
        elif value == 3:
            Tile(x, y, 3, all_tiles, water_tiles)  # 创建水 tile
        elif value == 4:
            player = Player(x, y + TILE_SIZE)  # 创建玩家（注意位置偏移一格）
            player_group.add(player)  # 添加到玩家组

# 主游戏循环
running = True  # 控制定时退出
while running:
    for event in pygame.event.get():  # 处理事件队列
        if event.type == pygame.QUIT:  # 如果点击关闭按钮
            running = False  # 退出主循环

    display_surface.blit(background_img, background_rect)  # 绘制背景图像
    all_tiles.draw(display_surface)  # 绘制所有 tile
    player_group.update()  # 更新玩家位置（处理键盘移动）
    player_group.draw(display_surface)  # 绘制玩家

    pygame.display.update()  # 刷新屏幕
    clock.tick(FPS)  # 控制帧率为 FPS（60）

pygame.quit()  # 退出 pygame，释放资源