from kivy.uix.button import Button
from .hover_behavior import HoverBehavior

class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)

    def on_enter(self):
        if self.background_color != "#689f38":  
            self.background_color = "#33691e"  

    def on_leave(self):
        if self.background_color != "#689f38":  
            self.background_color = "#33691e"  

    def on_press(self):
        self.background_color = "#689f38"  
