from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.difficulty_screen import DifficultyScreen
from screens.game_screen import GameScreen

class MinesweeperApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DifficultyScreen(name="difficulty"))
        sm.add_widget(GameScreen(name="game"))

        print("Available Screens:", sm.screen_names)
        sm.current = "difficulty"
        return sm

MinesweeperApp().run()