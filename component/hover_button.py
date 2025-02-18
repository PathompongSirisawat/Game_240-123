from kivy.uix.button import Button
from .hover_behavior import HoverBehavior

class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)

    def on_enter(self):
        if self.background_color != [0.3, 0.3, 0.3, 1]:
            self.background_color = [0.4, 0.4, 0.4, 1]

    def on_leave(self):
        if self.background_color != [0.3, 0.3, 0.3, 1]:
            self.background_color = [0.5, 0.5, 0.5, 1]

    def on_press(self):
        self.background_color = [0.3, 0.3, 0.3, 1]