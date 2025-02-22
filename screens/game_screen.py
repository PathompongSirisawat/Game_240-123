from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from component.minesweeper_game import MinesweeperGame

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_layout = BoxLayout(orientation="vertical")

        self.top_bar = BoxLayout(size_hint_y=None, height=80, padding=[10, 10], spacing=10)

        with self.top_bar.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.top_bg = Rectangle(size=self.top_bar.size, pos=self.top_bar.pos)
        self.top_bar.bind(size=self.update_top_background, pos=self.update_top_background)

        self.back_button = Button(text="Back", size_hint=(None, None), size=(100, 50),
                                  background_color=(0.6, 0.6, 0.6, 1), background_normal='')
        self.back_button.bind(on_press=self.go_back)
        self.top_bar.add_widget(self.back_button)

        self.title_label = Label(text="Minesweeper", font_size=30, color=(0, 0, 0, 1))
        self.top_bar.add_widget(self.title_label)
        
        self.remaining_flags_label = Label(text="Remaining flags: 0", font_size=20, color=(0, 0, 0, 1))
        self.top_bar.add_widget(self.remaining_flags_label)

        self.flag_mode_button = Button(text="Bomb Mode", size_hint=(None, None), size=(100, 50),
                                       background_color=(0.6, 0.6, 0.6, 1), background_normal='')
        self.flag_mode_button.bind(on_press=self.toggle_flag_mode)
        self.top_bar.add_widget(self.flag_mode_button)

        self.main_layout.add_widget(self.top_bar)

        self.board_container = FloatLayout()
        with self.board_container.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.bg_rect = Rectangle(size=self.board_container.size, pos=self.board_container.pos)

        self.board_container.bind(size=self.update_background, pos=self.update_background)
        self.main_layout.add_widget(self.board_container)

        self.add_widget(self.main_layout)

        self.flag_mode = False

    def update_top_background(self, *args):
        self.top_bg.size = self.top_bar.size
        self.top_bg.pos = self.top_bar.pos

    def update_background(self, *args):
        self.bg_rect.size = self.board_container.size
        self.bg_rect.pos = self.board_container.pos

    def start_game(self, rows, cols):
        print(f"Starting game with {rows} rows and {cols} cols")

        self.board_container.clear_widgets()

        self.game_board = MinesweeperGame(rows=rows, cols=cols, size_hint=(0.9, 0.9),
                                          pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.board_container.add_widget(self.game_board)
        
        self.game_board.flag_update_callback = self.update_flag_count
        self.update_flag_count(self.game_board.remaining_flags)

    def update_flag_count(self, remaining_flags):
        self.remaining_flags_label.text = f"Remaining flags: {remaining_flags}"

    def go_back(self, instance):
        self.manager.current = "difficulty"

    def toggle_flag_mode(self, instance):
        self.flag_mode = not self.flag_mode
        self.flag_mode_button.text = "Flag Mode" if self.flag_mode else "Bomb Mode"
        if hasattr(self, 'game_board'):
            self.game_board.flag_mode = self.flag_mode
