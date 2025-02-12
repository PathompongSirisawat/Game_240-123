from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

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
        return layout

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

MinesweeperApp().run()
