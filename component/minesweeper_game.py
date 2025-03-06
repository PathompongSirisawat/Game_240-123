from kivy.uix.gridlayout import GridLayout  
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import random
from collections import deque
from kivy.animation import Animation


class MinesweeperGame(GridLayout):
    def __init__(self, rows=8, cols=8, **kwargs):
        super().__init__(**kwargs)
        self.cols = cols
        self.rows = rows
        self.spacing = 2
        self.mines = set(random.sample(range(rows * cols), int(0.1 * rows * cols)))
        self.flag_mode = False
        self.max_flags = int(0.1 * rows * cols)
        self.remaining_flags = self.max_flags
        self.flag_update_callback = None
        self.stop_timer_callback = None  
        self.game_over = False
        self.hint_button = Button(text="Hint")      
        self.mine_numbers = self.calculate_mine_numbers()
        self.score = 0 
        self.score_update_callback = None  


        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_background, pos=self.update_background)
        
        self.buttons = []
        for i in range(self.rows * self.cols):
            btn = Button(background_color=(0.54, 0.79, 0.22, 1), background_normal="", disabled=False)
            btn.bind(on_press=self.handle_click)
            self.add_widget(btn)
            self.buttons.append((btn, i))
                
    def calculate_mine_numbers(self):
        mine_numbers = {}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for i in range(self.rows * self.cols):
            if i in self.mines:
                mine_numbers[i] = -1
                continue

            count = 0
            row, col = divmod(i, self.cols)
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbor_index = nr * self.cols + nc
                    if neighbor_index in self.mines:
                        count += 1

            mine_numbers[i] = count

        return mine_numbers

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def handle_click(self, instance):
        if self.game_over:
            return
        
        if self.flag_mode:
            self.toggle_flag(instance)
        else:
            self.reveal_cell(instance)
    
    def toggle_flag(self, instance):
        if self.game_over:
            return

        if not instance.text and self.remaining_flags > 0:
            instance.text = "Flag"
            self.remaining_flags -= 1
        elif instance.text == "Flag":
            instance.text = ""
            self.remaining_flags += 1
        
        if self.flag_update_callback:
            self.flag_update_callback(self.remaining_flags)
    
    def reveal_cell(self, instance):
        if self.game_over:
            return

        for btn, index in self.buttons:
            if btn == instance and btn.text != "Flag":
                if index in self.mines:
                    btn.text = "B"
                    btn.background_color = (0.8, 0.8, 0.8, 1)
                    btn.disabled = True  
                    self.show_popup("YOU LOSE!", f"Oh No! You pressed the BOMB!\nYour Score: {self.score}")
                    self.reveal_all()
                    self.game_over = True
                    if self.stop_timer_callback:
                        self.stop_timer_callback()  # หยุดเวลา
                    self.hint_button.disabled = True
                else:
                    self.reveal_safe_area(index)
                    self.check_win()
                break
                
    def reveal_all(self):
        self.game_over = True
        for btn, index in self.buttons:
            if btn.text == "Flag":
                if index in self.mines:
                    btn.text = "True"
                    btn.background_color = (0.6, 0.6, 0.6, 1)
                else:
                    btn.text = "False"
                    btn.background_color = (0.7, 0.6, 0.6, 1)
            elif not btn.text:  # ปรับตรงนี้
                if index in self.mines:
                    btn.text = "B"
                    btn.background_color = (0.8, 0, 0, 1)
                else:
                    btn.disabled = True  # เปลี่ยนจากการแสดง "X" เป็นแค่กดไม่ได้
    
    def update_score(self):
        if not self.game_over:
            self.score += 10  # เพิ่ม 10 คะแนนต่อช่องที่เปิดได้
            if self.score_update_callback:
                self.score_update_callback(self.score)

    def give_hint(self):
        if self.game_over:
            return

    # Find all safe cells that are not yet revealed
        safe_cells = [index for index, (btn, _) in enumerate(self.buttons) if btn.text == "" and index not in self.mines]

        if safe_cells:
            hint_index = random.choice(safe_cells)  # Select a random safe cell
            self.reveal_safe_area(hint_index)  # Reveal the safe area
            self.buttons[hint_index][0].disabled = True  # Disable the button to mark it as revealed
            self.check_win()  # Check if the game is won

    def is_adjacent_to_mine(self, index):
        row, col = divmod(index, self.cols)
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if r * self.cols + c in self.mines:
                        return True
        return False

    def reveal_cell_by_index(self, index):
        btn, _ = self.buttons[index]
        if index in self.mines:
            btn.text = "B"
            btn.background_color = (0.8, 0, 0, 1)
        else:
            mine_count = self.mine_numbers[index]
            if mine_count > 0:
                btn.text = str(mine_count)
                btn.markup = True  # เปิดใช้งาน markup
                btn.text = f"[color={self.get_number_hex_color(mine_count)}]{mine_count}[/color]"
            else:
                btn.text = " "
                self.reveal_safe_area(index)  
            
        btn.disabled = True  

    def check_win(self):
        unopened_cells = sum(1 for btn, _ in self.buttons if not btn.disabled)

        if unopened_cells == len(self.mines): 
            self.game_over = True
            self.show_popup("YOU WIN!", f"CONGRATS!\nYour Score: {self.score}")
            if self.stop_timer_callback:
                self.stop_timer_callback()  # หยุดเวลา
            if self.flag_update_callback:
                self.flag_update_callback(0)  # รีเซ็ตจำนวนธง
            self.hint_button.disabled = True

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, font_size=20),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.open()
        
    def reveal_safe_area(self, start_index):
        queue = deque([start_index])
        visited = set()

        while queue:
            index = queue.popleft()
            if index in visited:
                continue
            visited.add(index)

            btn, _ = self.buttons[index]
            if btn.text in ["Flag", "B"]:
                continue

            mine_count = self.mine_numbers[index]
            if mine_count > 0:
                btn.markup = True 
                btn.text = f"[color={self.get_number_hex_color(mine_count)}]{mine_count}[/color]"
            else:
                btn.text = " "
                self.add_neighbors_to_queue(index, queue, visited)

            btn.background_color = (245, 245, 220)
            btn.disabled = True  
            self.update_score()

    def add_neighbors_to_queue(self, index, queue, visited):
        row, col = divmod(index, self.cols)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            neighbor_index = nr * self.cols + nc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and neighbor_index not in visited:
                queue.append(neighbor_index)
    
    def get_number_hex_color(self, mine_count):
        colors = {
            1: "0000FF", 
            2: "008000",  
            3: "FF0000",  
    }
        return colors.get(mine_count, "000000")
    
    def handle_click(self, instance):
        if self.game_over:
            return
    
        if self.flag_mode:
            self.toggle_flag(instance)
        else:
            anim = Animation(background_color=(1, 1, 1, 1), duration=0.1) + \
               Animation(background_color=(0.7, 0.7, 0.7, 1), duration=0.1)
            anim.start(instance)  
        
        self.reveal_cell(instance)  

