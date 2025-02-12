from kivy.app import App
from kivy.uix.label import Label

class MinesweeperApp(App):
    def build(self):
        label = Label(text="Minesweeper",
            size_hint=(1, None), 
            height=80, 
            font_size=30,
            pos_hint={"top": 1}  
        )
        return label

MinesweeperApp().run()
