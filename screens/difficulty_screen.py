from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from component.hover_button import HoverButton
from kivy.animation import Animation
from kivy.clock import Clock

class DifficultyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_difficulty = None
        self.difficulty_buttons = []
        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.5, 0.7, 0.4, 1)
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self.update_background, pos=self.update_background)

        self.title_label = Label(text="[b][color=#F7F2C3]Gardensweeper[/color][/b]",markup=True, font_size=30,font_name="fonts/PressStart2P-Regular.ttf",
                    size_hint=(1, None), height=80, pos_hint={"center_x": 0.5, "center_y": 0.92})
        layout.add_widget(self.title_label)

        self.animate_title()

        difficulties = [
            ("Low", 8, 8, 0.75),
            ("Medium", 12, 12, 0.6),
            ("High", 16, 16, 0.45),
        ]

        for text, rows, cols, pos_y in difficulties:
            button = HoverButton(text=text, size_hint=(0.5, None), height=80,
                                pos_hint={"center_x": 0.5, "center_y": pos_y},
                                background_color= "#689f38", background_normal='')
            button.bind(on_press=self.create_select_difficulty_callback(button, text, rows, cols))
            self.difficulty_buttons.append(button)
            layout.add_widget(button)

        box_layout = BoxLayout(orientation='horizontal', size_hint=(0.5, None), height=80,
                               pos_hint={"center_x": 0.5, "center_y": 0.2})

        self.difficulty_label = Label(text="Select Difficulty",font_size=20, color=(0, 0, 0, 1),
                                      size_hint=(0.4, 1))
        box_layout.add_widget(self.difficulty_label)

        start_button = Button(text="Start", size_hint=(0.4, 1),
                              background_color=(0, 0.6, 0.2, 1), background_normal='')
        start_button.bind(on_press=self.start_game)
        box_layout.add_widget(start_button)

        layout.add_widget(box_layout)
        self.add_widget(layout)

    def create_select_difficulty_callback(self, button, text, rows, cols):
        def select_difficulty(instance):
            self.selected_difficulty = (text, rows, cols)
            self.update_button_colors(button)
            self.difficulty_label.text = f"Selected: {text}"
            print(f"Selected difficulty: {text}")

        return select_difficulty

    def update_button_colors(self, selected_button):
        for button in self.difficulty_buttons:
            if button == selected_button:
                button.background_color = (0.3, 0.3, 0.3, 1)
            else:
                button.background_color = (0.5, 0.5, 0.5, 1)

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
    
    def animate_title(self):
        def start_anim(*args):
            anim = Animation(font_size=40, duration=1) + Animation(font_size=30, duration=1)
            anim &= Animation(color=(1, 1, 0, 1), duration=1) + Animation(color=(1, 1, 1, 1), duration=0.5)
            anim.start(self.title_label)

        Clock.schedule_interval(start_anim, 2)
