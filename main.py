from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line


class MinesweeperGame(GridLayout):
    def __init__(self, rows=8, cols=8, **kwargs):
        super().__init__(**kwargs)
        self.cols = cols
        self.rows = rows

        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_grid, pos=self.update_grid)

        for _ in range(self.rows * self.cols):
            btn = Button(background_color=(0.7, 0.7, 0.7, 1), background_normal="")
            btn.bind(on_press=self.reveal_cell)
            self.add_widget(btn)

    def update_grid(self, *args):
        self.canvas.after.clear()  

        with self.canvas.after:
            Color(0, 0, 0, 1)  
            cell_width = self.width / self.cols
            cell_height = self.height / self.rows

            for i in range(1, self.cols):
                x = self.pos[0] + i * cell_width
                Line(points=[x, self.pos[1], x, self.pos[1] + self.size[1]], width=1)  

            for i in range(1, self.rows):
                y = self.pos[1] + i * cell_height
                Line(points=[self.pos[0], y, self.pos[0] + self.size[0], y], width=1)  

    def reveal_cell(self, instance):
        instance.text = "X"


class MinesweeperApp(App):
    def build(self):
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.bg_rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        self.label = Label(
            text="Minesweeper",
            font_size=30,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=80,
            pos_hint={"top": 1}
        )
        self.layout.add_widget(self.label)

        self.create_buttons()

        return self.layout

    def create_buttons(self):
        difficulties = [
            ("Low", 8, 8, 0.6),
            ("Medium", 12, 12, 0.4),
            ("High", 16, 16, 0.2),
        ]

        for text, rows, cols, pos_y in difficulties:
            button = Button(
                text=text,
                size_hint=(0.5, None),
                height=80,
                pos_hint={"center_x": 0.5, "center_y": pos_y},
                background_color=(0.5, 0.5, 0.5, 1),
                background_normal=''
            )
            button.bind(on_press=lambda btn, r=rows, c=cols: self.start_game(r, c))
            self.layout.add_widget(button)

    def update_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def start_game(self, rows, cols):
        existing_game = next((w for w in self.layout.children if isinstance(w, MinesweeperGame)), None)
        if existing_game:
            self.layout.remove_widget(existing_game)

        game_grid = MinesweeperGame(rows=rows, cols=cols, size_hint=(1, 0.7), pos_hint={"center_x": 0.5, "y": 0.05})
        self.layout.add_widget(game_grid)


MinesweeperApp().run()
