from kivy.uix.gridlayout import GridLayout  
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import random

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
                    btn.background_color = (0.8, 0, 0, 1)
                    self.reveal_all()
                    self.game_over = True
                else:
                    btn.text = "X"
                    btn.background_color = (0.6, 0.6, 0.6, 1)
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
