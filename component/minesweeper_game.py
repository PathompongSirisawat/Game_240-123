from kivy.uix.gridlayout import GridLayout  
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import random
from collections import deque

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
        self.game_over = False
        

        self.mine_numbers = self.calculate_mine_numbers()

        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_background, pos=self.update_background)

        self.buttons = []
        for i in range(self.rows * self.cols):
            btn = Button(background_color=(0.7, 0.7, 0.7, 1), background_normal="", disabled=False)
            btn.bind(on_press=self.handle_click)
            self.add_widget(btn)
            self.buttons.append((btn, i))
    
    def calculate_mine_numbers(self):
        mine_numbers = {}
        directions = [-1, 1, -self.cols, self.cols, -self.cols-1, -self.cols+1, self.cols-1, self.cols+1]

        for i in range(self.rows * self.cols):
            if i in self.mines:
                mine_numbers[i] = -1  
                continue

            count = 0
            for d in directions:
                neighbor = i + d
                if 0 <= neighbor < self.rows * self.cols and neighbor in self.mines:
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
                    self.show_popup("YOU LOSE!", "Oh No! You pressed the BOMB!")
                    self.reveal_all()
                    self.game_over = True
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
            elif not btn.text:
                if index in self.mines:
                    btn.text = "B"
                    btn.background_color = (0.8, 0, 0, 1)
                else:
                    btn.text = "X"
                    btn.background_color = (0.6, 0.6, 0.6, 1)

    def give_hint(self):
        if self.game_over:
            return
        
        for btn, index in self.buttons:
            if btn.text == "" and self.mine_numbers[index] == 0:
                self.reveal_safe_area(index)
                break

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
            btn.text = "X"
            btn.background_color = (0.6, 0.6, 0.6, 1)

    def check_win(self):
        opened_cells = sum(1 for btn, index in self.buttons if btn.text and btn.text not in ["Flag", "B"])
        total_safe_cells = (self.rows * self.cols) - len(self.mines)

        if opened_cells == total_safe_cells:
            self.game_over = True
            self.show_popup("🎉 YOU WIN!", "CONGRATS!🎉")
    
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
                btn.text = str(mine_count)
            else:
                btn.text = " "
                self.add_neighbors_to_queue(index, queue, visited)
            
            btn.background_color = (0.6, 0.6, 0.6, 1)

    def add_neighbors_to_queue(self, index, queue, visited):
        row, col = divmod(index, self.cols)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            neighbor_index = nr * self.cols + nc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and neighbor_index not in visited:
                queue.append(neighbor_index)