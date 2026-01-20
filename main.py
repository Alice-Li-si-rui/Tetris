import tkinter as tk
import tkinter.ttk as ttk
import time
from tetris import Tetris
from constants import *

class Game:
    def __init__(self, root):
        """初始化游戏"""
        self.root = root
        self.root.title(SCREEN_TITLE)
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.resizable(False, False)
        
        # 初始化游戏逻辑
        self.tetris = Tetris()
        self.game_started = False  # 游戏是否已开始
        
        # 创建主框架
        self.main_frame = tk.Frame(root, bg=BLACK)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建游戏板框架
        self.board_frame = tk.Frame(self.main_frame, bg=BLACK)
        self.board_frame.place(x=50, y=50, width=BOARD_WIDTH*BLOCK_SIZE, height=BOARD_HEIGHT*BLOCK_SIZE)
        
        # 创建游戏板网格
        self.board_canvas = tk.Canvas(self.board_frame, width=BOARD_WIDTH*BLOCK_SIZE, height=BOARD_HEIGHT*BLOCK_SIZE, bg=BLACK)
        self.board_canvas.pack()
        
        # 创建信息面板
        self.info_frame = tk.Frame(self.main_frame, bg=BLACK)
        self.info_frame.place(x=350, y=50, width=150, height=500)
        
        # 创建下一个方块预览
        self.next_piece_label = tk.Label(self.info_frame, text="下一个方块", fg=WHITE, bg=BLACK, font=('Arial', 10))
        self.next_piece_label.pack(pady=(0, 5))
        self.next_piece_frame = tk.Frame(self.info_frame, width=100, height=100, bg=GRAY)
        self.next_piece_frame.pack(pady=(0, 20))
        self.next_piece_canvas = tk.Canvas(self.next_piece_frame, width=100, height=100, bg=GRAY)
        self.next_piece_canvas.pack()
        
        # 创建得分显示
        self.score_label = tk.Label(self.info_frame, text="得分", fg=WHITE, bg=BLACK, font=('Arial', 10))
        self.score_label.pack(pady=(0, 5))
        self.score_var = tk.StringVar(value="0")
        self.score_display = tk.Label(self.info_frame, textvariable=self.score_var, fg=WHITE, bg=BLACK, font=('Arial', 16, 'bold'))
        self.score_display.pack(pady=(0, 20))
        
        # 创建级别显示
        self.level_label = tk.Label(self.info_frame, text="级别", fg=WHITE, bg=BLACK, font=('Arial', 10))
        self.level_label.pack(pady=(0, 5))
        self.level_var = tk.StringVar(value="1")
        self.level_display = tk.Label(self.info_frame, textvariable=self.level_var, fg=WHITE, bg=BLACK, font=('Arial', 16, 'bold'))
        self.level_display.pack(pady=(0, 20))
        
        # 创建控制说明
        self.controls_label = tk.Label(self.info_frame, text="控制说明", fg=WHITE, bg=BLACK, font=('Arial', 10))
        self.controls_label.pack(pady=(0, 5))
        self.controls_text = "←→: 移动\n↑: 旋转\n↓: 加速\n空格: 快速下落\nP: 暂停\nQ: 退出\nR: 重新开始"
        self.controls_display = tk.Label(self.info_frame, text=self.controls_text, fg=LIGHT_GRAY, bg=BLACK, font=('Arial', 8), justify=tk.LEFT)
        self.controls_display.pack(pady=(0, 20))
        
        # 创建游戏状态标签
        self.status_var = tk.StringVar(value="")
        self.status_label = tk.Label(self.main_frame, textvariable=self.status_var, fg=WHITE, bg=BLACK, font=('Arial', 16, 'bold'))
        self.status_label.place(x=50, y=20, width=BOARD_WIDTH*BLOCK_SIZE, anchor=tk.CENTER)
        
        # 游戏开始画面
        self.start_frame = tk.Frame(self.main_frame, bg=BLACK, relief=tk.RAISED, borderwidth=2)
        self.start_frame.place(x=50, y=200, width=BOARD_WIDTH*BLOCK_SIZE, height=200)
        
        self.start_title_label = tk.Label(self.start_frame, text="俄罗斯方块", fg=WHITE, bg=BLACK, font=('Arial', 24, 'bold'))
        self.start_title_label.pack(pady=(30, 20))
        
        self.start_button = tk.Button(self.start_frame, text="开始游戏", command=self.start_game, bg="#4CAF50", fg=WHITE, font=('Arial', 14))
        self.start_button.pack(pady=(10, 0))
        
        # 游戏结束画面
        self.game_over_frame = tk.Frame(self.main_frame, bg=BLACK, relief=tk.RAISED, borderwidth=2)
        self.game_over_frame.place(x=50, y=200, width=BOARD_WIDTH*BLOCK_SIZE, height=200)
        self.game_over_frame.pack_forget()  # 初始隐藏
        
        self.game_over_label = tk.Label(self.game_over_frame, text="游戏结束", fg=WHITE, bg=BLACK, font=('Arial', 20, 'bold'))
        self.game_over_label.pack(pady=(30, 20))
        
        self.final_score_var = tk.StringVar(value="得分: 0")
        self.final_score_label = tk.Label(self.game_over_frame, textvariable=self.final_score_var, fg=WHITE, bg=BLACK, font=('Arial', 14))
        self.final_score_label.pack(pady=(0, 20))
        
        self.restart_button = tk.Button(self.game_over_frame, text="重新开始", command=self.reset_game, bg="#4CAF50", fg=WHITE, font=('Arial', 12))
        self.restart_button.pack()
        
        # 绑定键盘事件
        self.root.bind('<Left>', lambda e: self.move_left())
        self.root.bind('<Right>', lambda e: self.move_right())
        self.root.bind('<Down>', lambda e: self.move_down())
        self.root.bind('<Up>', lambda e: self.rotate())
        self.root.bind('<space>', lambda e: self.hard_drop())
        self.root.bind('p', lambda e: self.toggle_pause())
        self.root.bind('q', lambda e: self.root.quit())
        self.root.bind('r', lambda e: self.reset_game())
        self.root.bind('<Return>', lambda e: self.start_game() if not self.game_started else None)  # 回车键开始游戏
        
        # 初始化游戏
        self.reset_game()
        
        # 开始游戏循环
        self.last_drop_time = time.time()
        self.game_loop()
    
    def reset_game(self):
        """重置游戏"""
        self.tetris.reset()
        self.game_started = False
        self.score_var.set(str(self.tetris.score))
        self.level_var.set(str(self.tetris.level))
        self.status_var.set("")
        self.game_over_frame.pack_forget()
        self.start_frame.place(x=50, y=200, width=BOARD_WIDTH*BLOCK_SIZE, height=200)
        self.draw_board()
        self.draw_next_piece()
    
    def start_game(self):
        """开始游戏"""
        self.game_started = True
        self.start_frame.pack_forget()
        self.status_var.set("")
        # 重置游戏状态
        self.tetris.reset()
        self.score_var.set(str(self.tetris.score))
        self.level_var.set(str(self.tetris.level))
        self.draw_board()
        self.draw_next_piece()
        # 重置下落计时器
        self.last_drop_time = time.time()
    
    def move_left(self):
        """向左移动方块"""
        if self.game_started and not self.tetris.game_over and not self.tetris.paused:
            self.tetris.move_left()
            self.draw_board()
    
    def move_right(self):
        """向右移动方块"""
        if self.game_started and not self.tetris.game_over and not self.tetris.paused:
            self.tetris.move_right()
            self.draw_board()
    
    def move_down(self):
        """向下移动方块"""
        if self.game_started and not self.tetris.game_over and not self.tetris.paused:
            moved = self.tetris.move_down()
            self.draw_board()
            if not moved:
                # 方块落地，检查游戏状态
                if self.tetris.game_over:
                    self.show_game_over()
                else:
                    self.draw_next_piece()
                # 更新得分和级别
                self.score_var.set(str(self.tetris.score))
                self.level_var.set(str(self.tetris.level))
    
    def hard_drop(self):
        """快速下落"""
        if self.game_started and not self.tetris.game_over and not self.tetris.paused:
            self.tetris.hard_drop()
            self.draw_board()
            if self.tetris.game_over:
                self.show_game_over()
            else:
                self.draw_next_piece()
            # 更新得分和级别
            self.score_var.set(str(self.tetris.score))
            self.level_var.set(str(self.tetris.level))
    
    def rotate(self):
        """旋转方块"""
        if self.game_started and not self.tetris.game_over and not self.tetris.paused:
            self.tetris.rotate()
            self.draw_board()
    
    def toggle_pause(self):
        """切换暂停状态"""
        if self.game_started and not self.tetris.game_over:
            self.tetris.toggle_pause()
            if self.tetris.paused:
                self.status_var.set("游戏暂停")
            else:
                self.status_var.set("")
                # 重置下落计时器
                self.last_drop_time = time.time()
    
    def show_game_over(self):
        """显示游戏结束画面"""
        self.final_score_var.set(f"得分: {self.tetris.score}")
        self.game_over_frame.place(x=50, y=200, width=BOARD_WIDTH*BLOCK_SIZE, height=200)
        self.game_started = False  # 游戏结束后设置为未开始状态
    
    def draw_board(self):
        """绘制游戏板"""
        self.board_canvas.delete('all')
        
        # 绘制游戏板网格
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                color = self.tetris.board[y][x]
                if color:
                    # 绘制方块
                    self.board_canvas.create_rectangle(
                        x*BLOCK_SIZE, y*BLOCK_SIZE, 
                        (x+1)*BLOCK_SIZE-2, (y+1)*BLOCK_SIZE-2, 
                        fill=BLOCK_COLORS[color], outline=WHITE
                    )
        
        # 绘制当前方块
        piece = self.tetris.current_piece
        shape = piece['shape']
        color = piece['color']
        x_offset = piece['x']
        y_offset = piece['y']
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    x = x_offset + j
                    y = y_offset + i
                    if y >= 0 and y < BOARD_HEIGHT and x >= 0 and x < BOARD_WIDTH:
                        # 绘制方块
                        self.board_canvas.create_rectangle(
                            x*BLOCK_SIZE, y*BLOCK_SIZE, 
                            (x+1)*BLOCK_SIZE-2, (y+1)*BLOCK_SIZE-2, 
                            fill=BLOCK_COLORS[color], outline=WHITE
                        )
        
        # 绘制网格线
        for x in range(BOARD_WIDTH+1):
            self.board_canvas.create_line(
                x*BLOCK_SIZE, 0, x*BLOCK_SIZE, BOARD_HEIGHT*BLOCK_SIZE, 
                fill=GRAY
            )
        for y in range(BOARD_HEIGHT+1):
            self.board_canvas.create_line(
                0, y*BLOCK_SIZE, BOARD_WIDTH*BLOCK_SIZE, y*BLOCK_SIZE, 
                fill=GRAY
            )
    
    def draw_next_piece(self):
        """绘制下一个方块预览"""
        self.next_piece_canvas.delete('all')
        
        piece = self.tetris.next_piece
        shape = piece['shape']
        color = piece['color']
        
        # 计算居中位置
        offset_x = (100 - len(shape[0])*20) // 2
        offset_y = (100 - len(shape)*20) // 2
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    # 绘制方块
                    self.next_piece_canvas.create_rectangle(
                        offset_x + j*20, offset_y + i*20, 
                        offset_x + (j+1)*20-2, offset_y + (i+1)*20-2, 
                        fill=BLOCK_COLORS[color], outline=WHITE
                    )
    
    def game_loop(self):
        """游戏主循环"""
        if self.game_started and not self.tetris.game_over and not self.tetris.paused:
            current_time = time.time()
            if current_time - self.last_drop_time > self.tetris.speed / 1000:
                self.move_down()
                self.last_drop_time = current_time
        
        # 继续循环
        self.root.after(50, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
