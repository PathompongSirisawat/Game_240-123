from kivy.app import App
from kivy.uix.label import Label

class GameApp(App):
    def build(self):
        label = Label(text="Hello World")
        return label

GameApp().run()
