from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
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

        back_layout = RelativeLayout(size_hint=(None, None), size=(50, 50))
        back_icon = Image(source="image/back_icon.png", size_hint=(None, None), size=(50, 50))
        back_layout.add_widget(back_icon)

        self.back_button = Button(size_hint=(None, None), size=(50, 50),
                                  background_color=(0, 0, 0, 0),  # ทำให้ปุ่มโปร่งใส
                                  background_normal='')
        back_layout.add_widget(self.back_button)
        self.back_button.bind(on_press=self.go_back)

        self.top_bar.add_widget(back_layout)

        # Create the reset button with an image
        reset_layout = RelativeLayout(size_hint=(None, None), size=(50, 50))
        reset_icon = Image(source="image/reset_icon.png", size_hint=(None, None), size=(50, 50))
        reset_layout.add_widget(reset_icon)

        self.reset_button = Button(size_hint=(None, None), size=(50, 50),
                                   background_color=(0, 0, 0, 0),  # ทำให้ปุ่มโปร่งใส
                                   background_normal='')
        reset_layout.add_widget(self.reset_button)
        self.reset_button.bind(on_press=self.reset_game)

        self.top_bar.add_widget(reset_layout)

        self.title_label = Label(text="Minesweeper", font_size=30, color=(0, 0, 0, 1), size_hint_x=2)
        self.top_bar.add_widget(self.title_label)
        
        self.timer_label = Label(text="Time: 00:00:00", font_size=20, color=(0, 0, 0, 1), size_hint_x=None, width=150)
        
        self.remaining_flags_label = Label(text="Remaining flags: 0", font_size=20, color=(0, 0, 0, 1), size_hint_x=None, width=200)
        
        self.flag_mode_button = Button(text="Bomb Mode", size_hint=(None, None), size=(100, 50),
                                       background_color=(0.6, 0.6, 0.6, 1), background_normal='')
        self.flag_mode_button.bind(on_press=self.toggle_flag_mode)
        
        right_layout = BoxLayout(size_hint_x=None, width=460)
        right_layout.add_widget(self.timer_label)
        right_layout.add_widget(self.remaining_flags_label)
        right_layout.add_widget(self.flag_mode_button)
        
        self.top_bar.add_widget(right_layout)

        self.main_layout.add_widget(self.top_bar)

        self.board_container = FloatLayout()
        with self.board_container.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.bg_rect = Rectangle(size=self.board_container.size, pos=self.board_container.pos)

        self.board_container.bind(size=self.update_background, pos=self.update_background)
        self.main_layout.add_widget(self.board_container)

        self.add_widget(self.main_layout)

        hint_button = Button(text="Hint (10)", size_hint=(0.2, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.1})
        hint_button.bind(on_press=self.show_hint)
        self.hint_counter = 0  # ตัวนับการใช้ Hint
        self.max_hints = 10    # กำหนดจำนวนครั้งสูงสุด
        self.hint_button = hint_button  # เก็บ reference ปุ่มไว้
        self.main_layout.add_widget(self.hint_button)

        self.flag_mode = False
        self.timer = 0
        self.timer_event = None
        
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

        self.reset_timer()

    def update_flag_count(self, remaining_flags):
        self.remaining_flags_label.text = f"Remaining flags: {remaining_flags}"

    def go_back(self, instance):
        self.manager.current = "difficulty"
        self.stop_timer()

    def toggle_flag_mode(self, instance):
        self.flag_mode = not self.flag_mode
        self.flag_mode_button.text = "Flag Mode" if self.flag_mode else "Bomb Mode"
        if hasattr(self, 'game_board'):
            self.game_board.flag_mode = self.flag_mode

    def update_timer(self, dt):
        self.timer += 1
        hours, remainder = divmod(self.timer, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timer_label.text = f"Time: {hours:02}:{minutes:02}:{seconds:02}"

    def reset_timer(self):
        self.timer = 0
        self.timer_label.text = "Time: 00:00:00"
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def reset_game(self, instance):
        if hasattr(self, "game_board"):
            self.start_game(self.game_board.rows, self.game_board.cols)
            # Reset the hint counter and update the hint button text
            self.hint_counter = 0
            self.hint_button.text = f"Hint ({self.max_hints})"
            self.hint_button.disabled = False

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()

    def show_hint(self, instance):
        if self.hint_counter < self.max_hints:
            self.game_board.give_hint()
            self.hint_counter += 1
            remaining_hints = self.max_hints - self.hint_counter
            self.hint_button.text = f"Hint ({remaining_hints})"

            if self.hint_counter >= self.max_hints:
                self.hint_button.disabled = True