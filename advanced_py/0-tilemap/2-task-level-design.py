# 导入 pygame 模块（用于游戏开发）和 sys 模块（用于退出程序）
import pygame
import sys

# 初始化 pygame 所有模块，必须调用一次
pygame.init()

# 设置窗口的宽和高
WINDOW_WIDTH, WINDOW_HEIGHT = 960, 640
TILE_SIZE = 32  # 每个 tile 的像素大小为 32x32

# 创建窗口并设置标题，screen 是主画布 Surface，用来绘制所有内容
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tile Map 优化版（保留原地图）")

# 创建时钟对象，用于控制帧率（FPS）
FPS = 60
clock = pygame.time.Clock()

# 设置所有图像资源所在的目录路径前缀
TILE_PATH = "./advanced_py/0-tilemap/"

# 加载瓦片图像，并用字典来映射 tile 编号 → 对应图片
# convert_alpha() 保留透明背景并优化显示速度
tile_images = {
    1: pygame.image.load(TILE_PATH + "dirt.png").convert_alpha(),   # 土
    2: pygame.image.load(TILE_PATH + "grass.png").convert_alpha(),  # 草
    3: pygame.image.load(TILE_PATH + "water.png").convert_alpha()   # 水
}

# 加载背景图像（.convert() 不需要透明通道，速度更快）
background_image = pygame.image.load(TILE_PATH + "background.png").convert()

# 获取背景图的位置和尺寸（topleft 设为左上角）
background_rect = background_image.get_rect(topleft=(0, 0))

# 创建地图二维数组，每个元素是一个 tile 类型编号
# 0 表示空白（不显示），1 表示 dirt，2 表示 grass，3 表示 water
tile_map = [
    # 总共 20 行 x 30 列，每个数字代表一个 tile 的类型
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

# 创建精灵组，用于存放所有瓦片 Tile 实例
tile_group = pygame.sprite.Group()

# 定义 Tile 类，继承 Sprite，用于在屏幕上绘制瓦片
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))  # 设置瓦片位置

# 遍历地图数组，根据编号生成对应的 Tile 精灵并加入组
for row_index, row in enumerate(tile_map):
    for col_index, tile_code in enumerate(row):
        if tile_code != 0:  # 忽略空 tile（编号 0）
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            tile = Tile(x, y, tile_images[tile_code])
            tile_group.add(tile)

# 主游戏循环
running = True
while running:
    # 处理窗口关闭事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 先绘制背景图，再绘制瓦片图层（图层顺序很重要）
    screen.blit(background_image, background_rect)
    tile_group.draw(screen)

    # 刷新窗口显示
    pygame.display.update()

    # 控制帧率，限制为每秒 60 帧
    clock.tick(FPS)

# 游戏退出，释放资源
pygame.quit()
sys.exit()