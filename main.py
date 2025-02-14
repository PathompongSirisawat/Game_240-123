from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button

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
        layout.add_widget(label)

        button_low = Button(
            text="Low",
            size_hint=(0.5, None),
            height=80,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            background_color=(0.5, 0.5, 0.5, 1),  # Gray color
            background_normal=''  # Remove default background
        )
        button_low.bind(on_press=self.on_button_press, on_release=self.on_button_release)

        button_medium = Button(
            text="Medium",
            size_hint=(0.5, None),
            height=80,
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            background_color=(0.5, 0.5, 0.5, 1),  # Gray color
            background_normal=''  # Remove default background
        )
        button_medium.bind(on_press=self.on_button_press, on_release=self.on_button_release)

        button_high = Button(
            text="High",
            size_hint=(0.5, None),
            height=80,
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            background_color=(0.5, 0.5, 0.5, 1),  # Gray color
            background_normal=''  # Remove default background
        )
        button_high.bind(on_press=self.on_button_press, on_release=self.on_button_release)

        layout.add_widget(button_low)
        layout.add_widget(button_medium)
        layout.add_widget(button_high)

        return layout

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def on_button_press(self, instance):
        instance.background_color = (0.2, 0.2, 0.2, 0.2)  # Darker gray for shadow effect

    def on_button_release(self, instance):
        instance.background_color = (0.5, 0.5, 0.5, 1)  # Original gray color

MinesweeperApp().run()