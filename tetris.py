import random
from constants import *

class Tetris:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置游戏状态"""
        # 初始化游戏板
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        # 初始化当前方块和下一个方块
        self.current_piece = self.generate_piece()
        self.next_piece = self.generate_piece()
        # 初始化游戏状态
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        # 计算当前游戏速度
        self.update_speed()
    
    def generate_piece(self):
        """生成随机方块"""
        shape_index = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[shape_index]
        return {
            'shape': shape,
            'color': shape_index + 1,  # 颜色索引从1开始
            'x': BOARD_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }
    
    def update_speed(self):
        """根据级别更新游戏速度"""
        self.speed = max(MIN_SPEED, INITIAL_SPEED - (self.level - 1) * SPEED_DECREASE)
    
    def move_left(self):
        """向左移动方块"""
        if not self.game_over and not self.paused:
            if self.can_move(self.current_piece['shape'], self.current_piece['x'] - 1, self.current_piece['y']):
                self.current_piece['x'] -= 1
    
    def move_right(self):
        """向右移动方块"""
        if not self.game_over and not self.paused:
            if self.can_move(self.current_piece['shape'], self.current_piece['x'] + 1, self.current_piece['y']):
                self.current_piece['x'] += 1
    
    def move_down(self):
        """向下移动方块"""
        if not self.game_over and not self.paused:
            if self.can_move(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y'] + 1):
                self.current_piece['y'] += 1
                return True
            else:
                print(f"方块触地，位置: ({self.current_piece['x']}, {self.current_piece['y']})")
                self.lock_piece()
                self.clear_lines()
                # 先生成新的方块，然后检查游戏是否结束
                print(f"生成新方块前，next_piece位置: ({self.next_piece['x']}, {self.next_piece['y']})")
                self.current_piece = self.next_piece
                self.next_piece = self.generate_piece()
                print(f"生成新方块后，current_piece位置: ({self.current_piece['x']}, {self.current_piece['y']})")
                # 检查新方块是否可以放置
                can_place = self.can_move(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y'])
                print(f"新方块是否可以放置: {can_place}")
                if not can_place:
                    self.game_over = True
                    print("游戏结束！")
                return False
    
    def hard_drop(self):
        """快速下落"""
        if not self.game_over and not self.paused:
            while self.move_down():
                pass
    
    def rotate(self):
        """旋转方块"""
        if not self.game_over and not self.paused:
            rotated_shape = self.rotate_shape(self.current_piece['shape'])
            if self.can_move(rotated_shape, self.current_piece['x'], self.current_piece['y']):
                self.current_piece['shape'] = rotated_shape
    
    def rotate_shape(self, shape):
        """旋转形状矩阵"""
        n = len(shape)
        rotated = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                rotated[j][n - 1 - i] = shape[i][j]
        return rotated
    
    def can_move(self, shape, x, y):
        """检查方块是否可以移动到指定位置"""
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    new_x = x + j
                    new_y = y + i
                    if (new_x < 0 or new_x >= BOARD_WIDTH or
                        new_y >= BOARD_HEIGHT or
                        (new_y >= 0 and self.board[new_y][new_x])):
                        return False
        return True
    
    def lock_piece(self):
        """将当前方块锁定到游戏板"""
        shape = self.current_piece['shape']
        color = self.current_piece['color']
        x = self.current_piece['x']
        y = self.current_piece['y']
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    board_y = y + i
                    board_x = x + j
                    if board_y >= 0:
                        self.board[board_y][board_x] = color
    
    def clear_lines(self):
        """消除完整的行"""
        lines_to_clear = []
        
        # 找出所有完整的行
        for i in range(BOARD_HEIGHT):
            if all(self.board[i]):
                lines_to_clear.append(i)
        
        # 消除行并更新得分
        lines_cleared = len(lines_to_clear)
        if lines_cleared > 0:
            # 消除行
            for line in sorted(lines_to_clear, reverse=True):
                del self.board[line]
                self.board.insert(0, [0 for _ in range(BOARD_WIDTH)])
            
            # 更新得分
            self.score += LINE_SCORES[lines_cleared] * self.level
            self.lines_cleared += lines_cleared
            
            # 检查是否升级
            new_level = self.lines_cleared // LINES_PER_LEVEL + 1
            if new_level > self.level:
                self.level = new_level
                self.update_speed()
    

    
    def toggle_pause(self):
        """切换游戏暂停状态"""
        if not self.game_over:
            self.paused = not self.paused
