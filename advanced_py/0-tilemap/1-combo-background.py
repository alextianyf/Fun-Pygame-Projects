# 导入 pygame 模块和 sys 模块（用于关闭程序）
import pygame
import sys

# 初始化 pygame 所有模块（必须执行）
pygame.init()

# 设置窗口宽度和高度为 800x600 像素
# 这决定了游戏画面的大小，也就是屏幕显示区域
screen_width, screen_height = 320, 160
screen = pygame.display.set_mode((screen_width, screen_height))  # 创建窗口 Surface
pygame.display.set_caption("Tilemap 教学")  # 设置窗口标题

# 加载背景图和三种瓦片图像
# 注意路径使用你给定的目录 "./advanced_py/tilemap/"
# convert() 用于优化图片显示速度（背景不透明）
# convert_alpha() 保留透明度（瓦片通常有透明背景）
# background = pygame.image.load("./advanced_py/assets/background.png").convert()
dirt = pygame.image.load("./advanced_py/assets/dirt.png").convert_alpha()
grass = pygame.image.load("./advanced_py/assets/grass.png").convert_alpha()
water = pygame.image.load("./advanced_py/assets/water.png").convert_alpha()

# 设置瓦片大小为 32x32 像素
# 之后所有瓦片都会按这个单位进行定位、绘制
TILE_SIZE = 32

# 创建 tilemap（二维数组），代表地图结构
# 每个数字代表一种瓦片：0 = dirt, 1 = grass, 2 = water. 3 = background
# 每行代表一排瓦片，每列就是横向排列
tilemap = [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [1, 1, 4, 1, 1, 1, 4, 4, 1, 1],
    [0, 0, 2, 0, 0, 0, 2, 2, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 2, 0, 0],
]

# 定义一个函数专门用于绘制 tilemap
# 枚举每一行（y 表示行号），再枚举每一列（x 表示列号）
# 用 x * TILE_SIZE 和 y * TILE_SIZE 计算每个 tile 的坐标
# 根据 tile 类型决定绘制哪张图片
def draw_tilemap():
    for y, row in enumerate(tilemap):           # 遍历每一行
        for x, tile in enumerate(row):          # 遍历行内每一个瓦片
            if tile == 0:
                screen.blit(dirt, (x * TILE_SIZE, y * TILE_SIZE))   # dirt tile
            elif tile == 1:
                screen.blit(grass, (x * TILE_SIZE, y * TILE_SIZE))  # grass tile
            elif tile == 2:
                screen.blit(water, (x * TILE_SIZE, y * TILE_SIZE))  # water tile
            # elif tile == 3:
                # screen.blit(background, (x * TILE_SIZE, y * TILE_SIZE))
                

# 创建时钟对象，用于控制帧率
clock = pygame.time.Clock()

# 控制主循环的变量，设为 True 表示游戏继续运行
running = True

# 主游戏循环
while running:
    #screen.blit(background, (0, 0))  # 每帧先绘制背景图，避免残影
    screen.fill((0, 0, 0))  # RGB(0, 0, 0) 是黑色
    draw_tilemap()                   # 然后在上面画出 tilemap（地形）

    # 处理所有 pygame 事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果用户点击关闭按钮，退出游戏
            running = False

    pygame.display.update()   # 更新显示内容，把所有画面呈现在屏幕上
    clock.tick(60)            # 每秒最多 60 帧，限制游戏速度稳定运行

# 游戏结束后退出 pygame，并关闭窗口
pygame.quit()
sys.exit()