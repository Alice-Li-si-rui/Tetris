# 游戏常量定义

# 游戏窗口设置
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 650
SCREEN_TITLE = "俄罗斯方块"

# 游戏板设置
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30

# 游戏速度（毫秒）
INITIAL_SPEED = 1000
SPEED_DECREASE = 100
MIN_SPEED = 100

# 得分规则
LINE_SCORES = [0, 100, 300, 500, 800]  # 0, 1, 2, 3, 4行的得分

# 级别提升规则
LINES_PER_LEVEL = 10

# 方块形状定义
SHAPES = [
    # I 形
    [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
    # J 形
    [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    # L 形
    [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
    # O 形
    [[1, 1], [1, 1]],
    # S 形
    [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    # T 形
    [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    # Z 形
    [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
]

# 颜色定义（Tkinter格式）
BLACK = "#000000"
WHITE = "#FFFFFF"
GRAY = "#646464"
LIGHT_GRAY = "#C8C8C8"

# 方块颜色（Tkinter格式）
BLOCK_COLORS = [
    None,           # 0: 空
    "#FF0D72",      # 1: 红色
    "#0DC2FF",      # 2: 蓝色
    "#0DFF72",      # 3: 绿色
    "#F538FF",      # 4: 粉色
    "#FF8E0D",      # 5: 橙色
    "#FFE138",      # 6: 黄色
    "#3877FF"       # 7: 紫色
]
