import tkinter as tk
from back_end import Wordle
from PIL import Image, ImageTk
import random

def secretWord(fileName : str) -> str:
    with open(fileName, 'r') as f:
        words = f.read().splitlines()
    return random.choice(words)

class WordleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.colors = {
            'bg': "#FFFFFF",
            'tile_bg': "#d3d6da",
            'key_bg': "#d3d6da",
            'text': '#000000',
            'border': "#5f5f5f",
            'correct': "#4ea146",
            'present': "#e2c544",
            'absent': '#878a8c',
            'error_text': "#a00101",
            'btn_text': '#FFFFFF'
        }

        self.title("Wordle Game")
        self.geometry("800x950")
        self.resizable(False, False)
        
        self.bg_image = None
        if ImageTk:
            try:
                img = Image.open("bg.jpg")
                img = img.resize((800, 950), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                
                background_label = tk.Label(self, image=self.bg_image)
                background_label.place(x=0, y=0, relwidth=1, relheight=1)
            except FileNotFoundError:
                self.configure(bg=self.colors['bg'])
        else:
            self.configure(bg=self.colors['bg'])
        
        self.is_animating = False

        self.bind("<Key>", self.handle_key_press)
        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        self.game_name_label = tk.Label(self, text="WORDLE", font=("Helvetica", 32, "bold"), fg=self.colors['text'])
        if not self.bg_image:
            self.game_name_label.config(bg=self.colors['bg'])
        self.game_name_label.pack(pady=(20, 0))

        self.shake_container = tk.Frame(self)
        if not self.bg_image: self.shake_container.config(bg=self.colors['bg'])
        self.shake_container.pack(pady=10)

        self.grid_frame = tk.Frame(self.shake_container) 
        if not self.bg_image: self.grid_frame.config(bg=self.colors['bg'])
        self.grid_frame.pack()
        
        self.notification_label = tk.Label(self, text="", font=("Helvetica", 16, "bold"))
        if not self.bg_image: self.notification_label.config(bg=self.colors['bg'])
        self.notification_label.pack(pady=10)
        
        self.tiles = []
        for i in range(6):
            row_tiles = []
            for j in range(5):
                tile = tk.Label(self.grid_frame, text="", width=4, height=2,
                                bg=self.colors['tile_bg'], fg=self.colors['text'],
                                font=("Helvetica", 24, "bold"),
                                relief="solid", borderwidth=2)
                tile.grid(row=i, column=j, padx=5, pady=5)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

        self.create_virtual_keyboard()

    def new_game(self):
        """Bắt đầu một ván chơi mới."""
        secret = secretWord("output_words.txt")
        self.game = Wordle(secret)
        
        self.current_row = 0
        self.current_col = 0
        self.current_guess = ""

        if hasattr(self, 'tiles'):
            self.update_grid()
            self.hide_notification()
            if hasattr(self, 'play_again_button'):
                 self.play_again_button.pack_forget()
            if hasattr(self, 'keyboard_frame'):
                 self.reset_keyboard_colors()
            
    def add_letter(self, letter):
        if self.game.game_over or self.current_col >= 5:
            return
        
        self.current_guess += letter.lower()
        tile = self.tiles[self.current_row][self.current_col]
        tile.config(text=letter.upper())
        self.current_col += 1
                
    def delete_letter(self):
        if self.game.game_over or self.current_col <= 0:
            return
        
        self.current_col -= 1
        self.current_guess = self.current_guess[:-1]
        tile = self.tiles[self.current_row][self.current_col]
        tile.config(text="")

    def submit_guess_event(self):
        """Xử lý logic khi đoán chữ."""
        if self.game.game_over or self.is_animating:
            return
            
        if len(self.current_guess) != 5:
            self.show_notification("Your word must have 5 letters!", color=self.colors['error_text'])
            self.shake_grid()
            return
            
        feedback = self.game.check_guess(self.current_guess)
        
        self.animate_flip_row(self.current_row, feedback)
        
        self.current_row += 1
        self.current_col = 0
        self.current_guess = ""

    def animate_flip_row(self, row_index, feedback):
        """Tạo hiệu ứng lật cho một hàng ô chữ."""
        self.is_animating = True
        
        for col_index, tile_feedback in enumerate(feedback):
            tile = self.tiles[row_index][col_index]
            self.after(col_index * 200, lambda t=tile, fb=tile_feedback: self.flip_tile(t, fb))

        total_animation_time = len(feedback) * 200 + 200
        self.after(total_animation_time, self.check_game_over_state)

    def flip_tile(self, tile, feedback):
        """Thực hiện animation lật cho một ô chữ duy nhất."""
        tile.config(text="", bg=self.colors['border'])
        
        def reveal():
            tile.config(text=feedback['letter'], 
                        bg=self.colors[feedback['status']], 
                        fg=self.colors['btn_text'])

        self.after(100, reveal)
        
    def check_game_over_state(self):
        """Kiểm tra trạng thái thắng/thua sau khi animation kết thúc."""
        self.is_animating = False
        self.update_keyboard_colors(self.game.guesses[-1])
        
        if self.game.game_over:
            if self.game.win:
                self.show_notification("You won!", duration=5000, color=self.colors['correct'])
            else:
                msg = f"Secret word: {self.game.secret.upper()}"
                self.show_notification(msg, duration=5000)
            
            self.after(1000, self.play_again_button.pack)


    def handle_key_press(self, event):
        """Xử lý sự kiện gõ phím vật lý."""
        if self.is_animating: return
        key = event.keysym
        
        if key == 'Return':
            self.submit_guess_event()
        elif key == 'Delete' or key == "BackSpace":
            self.delete_letter()
        elif len(key) == 1 and 'a' <= key.lower() <= 'z':
            self.add_letter(key)
            
    def add_letter(self, letter):
        """Thêm một chữ cái vào lần đoán hiện tại."""
        if self.game.game_over or self.current_col >= 5 or self.is_animating:
            return
        
        self.current_guess += letter.lower()
        tile = self.tiles[self.current_row][self.current_col]
        tile.config(text=letter.upper())
        self.current_col += 1
        
    def delete_letter(self):
        """Xóa chữ cái cuối cùng khỏi lần đoán."""
        if self.game.game_over or self.current_col <= 0 or self.is_animating:
            return
            
        self.current_col -= 1
        self.current_guess = self.current_guess[:-1]
        tile = self.tiles[self.current_row][self.current_col]
        tile.config(text="")

    def update_grid(self):
        """Cập nhật lại giao diện lưới chữ."""
        for i in range(6):
            for j in range(5):
                tile = self.tiles[i][j]
                if i < len(self.game.guesses):
                    feedback_row = self.game.guesses[i]
                    feedback = feedback_row[j]
                    tile.config(text=feedback['letter'], bg=self.colors[feedback['status']], fg=self.colors['btn_text'])
                else:
                    tile.config(text="", bg=self.colors['tile_bg'], fg=self.colors['text'])

    def create_virtual_keyboard(self):
        """Tạo và hiển thị bàn phím ảo trên màn hình."""
        self.keyboard_frame = tk.Frame(self)
        if not self.bg_image: self.keyboard_frame.config(bg=self.colors['bg'])
        self.keyboard_frame.pack(side="bottom", pady=20)
        self.key_buttons = {}

        key_layout = [
            "q w e r t y u i o p",
            "a s d f g h j k l",
            "Enter z x c v b n m Delete"
        ]

        for row_layout in key_layout:
            row_frame = tk.Frame(self.keyboard_frame)
            if not self.bg_image: row_frame.config(bg=self.colors['bg'])
            row_frame.pack()
            for key in row_layout.split():
                if len(key) > 1: 
                    width = 8
                    command = self.submit_guess_event if key == 'Enter' else self.delete_letter
                else:
                    width = 4
                    command = lambda k=key: self.add_letter(k)
                
                button = tk.Button(row_frame, text=key.upper(), width=width, height=2,
                                   bg=self.colors['bg'], fg=self.colors['text'],
                                   font=("Helvetica", 10, "bold"),
                                   command=command)
                button.pack(side="left", padx=2, pady=2)
                if len(key) == 1:
                    self.key_buttons[key] = button
        
        self.play_again_button = tk.Button(self.keyboard_frame, text="Play Again", command=self.new_game,
                                           bg=self.colors['correct'], fg=self.colors['btn_text'],
                                           font=("Helvetica", 14), relief="flat", width=15, height=2)

    def update_keyboard_colors(self, feedback):
        """Cập nhật màu sắc của các phím dựa trên kết quả đoán."""
        for item in feedback:
            key = item['letter'].lower()
            status = item['status']
            button = self.key_buttons.get(key)
            if not button: continue

            current_color = button.cget("background")
            if current_color == self.colors['correct']:
                continue
            if current_color == self.colors['present'] and status == 'absent':
                continue
                
            button.config(bg=self.colors[status])

    def reset_keyboard_colors(self):
        """Reset màu sắc của tất cả các phím về mặc định."""
        for button in self.key_buttons.values():
            button.config(bg=self.colors['bg'])

    def show_notification(self, message, color=None, duration=2000):
        self.notification_label.config(text=message)
        if not self.bg_image:
             self.notification_label.config(bg=self.colors['bg'])
        if color:
            self.notification_label.config(fg=color)
        
        if hasattr(self, '_notification_timer'):
            self.after_cancel(self._notification_timer)
            
        self._notification_timer = self.after(duration, self.hide_notification)

    def hide_notification(self):
        self.notification_label.config(text="")
        if not self.bg_image:
             self.notification_label.config(bg=self.colors['bg'])

    def shake_grid(self, shakes=8, offset=5, delay=50):
        def do_shake(count):
            if count <= 0:
                self.shake_container.pack_configure(padx=0)
                return
            current_offset = offset if count % 2 == 0 else 0
            self.shake_container.pack_configure(padx=(current_offset, 0))
            self.after(delay, lambda: do_shake(count - 1))
        do_shake(shakes)
