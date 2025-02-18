from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class HoverBehavior(object):
    def __init__(self, **kwargs):
        super(HoverBehavior, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        if self.collide_point(*self.to_widget(*pos)):
            self.on_enter()
        else:
            self.on_leave()

    def on_enter(self):
        pass

    def on_leave(self):
        pass

class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)

    def on_enter(self):
        if self.background_color != [0.3, 0.3, 0.3, 1]:  # ถ้าปุ่มยังไม่ได้ถูกเลือก
            self.background_color = [0.4, 0.4, 0.4, 1]

    def on_leave(self):
        if self.background_color != [0.3, 0.3, 0.3, 1]:  # ถ้าปุ่มยังไม่ได้ถูกเลือก
            self.background_color = [0.5, 0.5, 0.5, 1]

    def on_press(self):
        self.background_color = [0.3, 0.3, 0.3, 1]  # เปลี่ยนสีปุ่มเมื่อกด

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
        self.selected_difficulty = None
        self.difficulty_buttons = []
        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self.update_background, pos=self.update_background)

        title = Label(text="Minesweeper", font_size=30, color=(0, 0, 0, 1),
                      size_hint=(1, None), height=80, pos_hint={"center_x": 0.5, "center_y": 0.9})
        layout.add_widget(title)

        difficulties = [
            ("Low", 8, 8, 0.7),
            ("Medium", 12, 12, 0.55),
            ("High", 16, 16, 0.4),
        ]

        for text, rows, cols, pos_y in difficulties:
            button = HoverButton(text=text, size_hint=(0.5, None), height=80,
                                 pos_hint={"center_x": 0.5, "center_y": pos_y},
                                 background_color=(0.5, 0.5, 0.5, 1), background_normal='')
            button.bind(on_press=self.create_select_difficulty_callback(button, text, rows, cols))
            self.difficulty_buttons.append(button)
            layout.add_widget(button)

        start_button = Button(text="Start", size_hint=(0.3, None), height=80,
                              pos_hint={"center_x": 0.5, "center_y": 0.25},
                              background_color=(0.5, 0.5, 0.5, 1), background_normal='')
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def create_select_difficulty_callback(self, button, text, rows, cols):
        def select_difficulty(instance):
            self.selected_difficulty = (text, rows, cols)
            self.update_button_colors(button)
            print(f"Selected difficulty: {text}")

        return select_difficulty

    def update_button_colors(self, selected_button):
        for button in self.difficulty_buttons:
            if button == selected_button:
                button.background_color = (0.3, 0.3, 0.3, 1)  # เปลี่ยนสีปุ่มที่เลือก
            else:
                button.background_color = (0.5, 0.5, 0.5, 1)  # สีปุ่มที่ไม่ถูกเลือก

    def update_background(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def start_game(self, instance):
        if not self.selected_difficulty:
            print("Error: No difficulty selected")
            return

        rows, cols = self.selected_difficulty[1], self.selected_difficulty[2]
        if "game" not in self.manager.screen_names:
            print("Error: Screen 'game' not found in manager")
            return

        print(f"Switching to game screen with {rows}x{cols}")
        self.manager.get_screen("game").start_game(rows, cols)
        self.manager.current = "game"

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

        self.main_layout.add_widget(self.top_bar)

        self.board_container = FloatLayout()
        with self.board_container.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.bg_rect = Rectangle(size=self.board_container.size, pos=self.board_container.pos)

        self.board_container.bind(size=self.update_background, pos=self.update_background)
        self.main_layout.add_widget(self.board_container)

        self.add_widget(self.main_layout)

    def update_top_background(self, *args):
        self.top_bg.size = self.top_bar.size
        self.top_bg.pos = self.top_bar.pos

    def update_background(self, *args):
        self.bg_rect.size = self.board_container.size
        self.bg_rect.pos = self.board_container.pos

    def start_game(self, rows, cols):
        print(f"Starting game with {rows} rows and {cols} cols")

        self.board_container.clear_widgets()

        game_board = MinesweeperGame(rows=rows, cols=cols, size_hint=(0.9, 0.9),
                                     pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.board_container.add_widget(game_board)

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
