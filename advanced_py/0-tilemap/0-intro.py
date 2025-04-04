# 导入 pygame 模块（制作游戏用）和 sys 模块（用于退出程序）
import pygame
import sys

# 初始化 pygame，必须调用才能使用图形、声音等功能
pygame.init()

# 设置窗口宽度和高度
screen_width, screen_height = 320, 160

# 创建窗口，大小为 320x160 像素，并返回一个“画布”Surface对象
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置窗口标题栏上的文字
pygame.display.set_caption("简单Tile教学")

# 加载水瓦片图片（路径使用你的目录结构）
# convert_alpha() 保留透明通道并加速显示
water = pygame.image.load("./advanced_py/0-tilemap/water.png").convert_alpha()

# 加载土瓦片图片（同样使用 convert_alpha 保留透明度）
dirt = pygame.image.load("./advanced_py/0-tilemap/dirt.png").convert_alpha()

# 设置瓦片的大小，单位为像素（Tile 是 32x32 的正方形）
TILE_SIZE = 32

# 设置游戏是否运行的布尔变量（控制主循环）
running = True

# 进入主游戏循环
while running:
    # 用黑色清空屏幕，防止残影或旧图
    screen.fill((0, 0, 0))  # RGB(0, 0, 0) 是黑色

    # Step 1: 在屏幕上绘制一张水的瓦片图片
    # 坐标 (0, 0) 表示贴在屏幕的左上角
    screen.blit(water, (0, 0))

    # 监听所有玩家操作（鼠标、键盘、窗口事件等）
    for event in pygame.event.get():
        # 如果用户点击了关闭窗口按钮，就退出循环
        if event.type == pygame.QUIT:
            running = False

    # 更新屏幕内容，把刚刚绘制的瓦片显示出来
    pygame.display.update()

# 主循环结束后，关闭 pygame 并退出程序
pygame.quit()
sys.exit()