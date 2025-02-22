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

        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_background, pos=self.update_background)

        self.buttons = []
        for i in range(self.rows * self.cols):
            btn = Button(background_color=(0.7, 0.7, 0.7, 1), background_normal="")
            btn.bind(on_press=self.reveal_cell)
            self.add_widget(btn)
            self.buttons.append((btn, i))

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def reveal_cell(self, instance):
        for btn, index in self.buttons:
            if btn == instance:
                if index in self.mines:
                    btn.text = "B"
                    btn.background_color = (0.8, 0, 0, 1)
                else:
                    btn.text = "X"
                    btn.background_color = (0.6, 0.6, 0.6, 1)
                break
