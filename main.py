from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

class MinesweeperGame(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 8  # สร้างกระดาน 8x8
        self.rows = 8

        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle(size =self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class MinesweeperApp(App):
    def build(self):
        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        
        layout.bind(size=self.update_rect, pos=self.update_rect)

        label = Label(
            text="Minesweeper",
            font_size=30,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=80,
            pos_hint={"top": 1}
        )
        
        grid = MinesweeperGame(size_hint=(1, 0.8), pos_hint={"top": 0.9})

        layout.add_widget(label)
        layout.add_widget(grid)
        return layout

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

MinesweeperApp().run()
