from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class MinesweeperGame(GridLayout):
    def __init__(self, rows=8, cols=8, **kwargs):
        super().__init__(**kwargs)
        self.cols = cols
        self.rows = rows
        self.spacing = 2

        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_background, pos=self.update_background)

        for _ in range(self.rows * self.cols):
            btn = Button(background_color=(0.7, 0.7, 0.7, 1), background_normal="")
            btn.bind(on_press=self.reveal_cell)
            self.add_widget(btn)

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def reveal_cell(self, instance):
        instance.text = "X"