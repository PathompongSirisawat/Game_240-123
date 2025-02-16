from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
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

class DifficultyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self.update_background, pos=self.update_background)

        title = Label(text="Minesweeper", font_size=30, color=(0, 0, 0, 1),
                      size_hint=(1, None), height=80, pos_hint={"top": 1})
        layout.add_widget(title)

        difficulties = [
            ("Low", 8, 8, 0.6),
            ("Medium", 12, 12, 0.4),
            ("High", 16, 16, 0.2),
        ]

        for text, rows, cols, pos_y in difficulties:
            button = Button(text=text, size_hint=(0.5, None), height=80,
                            pos_hint={"center_x": 0.5, "center_y": pos_y},
                            background_color=(0.5, 0.5, 0.5, 1), background_normal='')
            button.bind(on_press=self.create_start_game_callback(rows, cols))
            layout.add_widget(button)

        self.add_widget(layout)

    def create_start_game_callback(self, rows, cols):
        return lambda btn: self.start_game(rows, cols)

    def update_background(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def start_game(self, rows, cols):
        if "game" not in self.manager.screen_names:
            print("Error: Screen 'game' not found in manager")
            return

        print(f"Switching to game screen with {rows}x{cols}")
        self.manager.get_screen("game").start_game(rows, cols)
        self.manager.current = "game"



class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.bg_rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self.update_background, pos=self.update_background)

        self.title = Label(text="Minesweeper", font_size=30, color=(0, 0, 0, 1),
                           size_hint=(1, None), height=80, pos_hint={"top": 1})
        self.layout.add_widget(self.title)

        self.back_button = Button(text="Back", size_hint=(0.2, None), height=60,
                                  pos_hint={"x": 0.05, "top": 0.9},
                                  background_color=(0.6, 0.6, 0.6, 1), background_normal='')
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        self.rows = 8  
        self.cols = 8

    def update_background(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def on_enter(self):
        self.start_game(self.rows, self.cols)  

    def start_game(self, rows, cols):
        print(f"Starting game with {rows} rows and {cols} cols")
        self.rows = rows
        self.cols = cols

        for widget in self.layout.children[:]:
            if isinstance(widget, MinesweeperGame):
                self.layout.remove_widget(widget)

        game_board = MinesweeperGame(rows=rows, cols=cols, size_hint=(0.8, 0.8),
                                     pos_hint={"center_x": 0.5, "center_y": 0.45})
        self.layout.add_widget(game_board)

    def go_back(self, instance):
        self.manager.current = "difficulty"  


class MinesweeperApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DifficultyScreen(name="difficulty"))
        sm.add_widget(GameScreen(name="game"))

        print("Available Screens:", sm.screen_names)
        sm.current = "difficulty"  
        return sm

MinesweeperApp().run()

