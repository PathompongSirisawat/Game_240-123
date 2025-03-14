from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.audio import SoundLoader
from kivy.core.window import Window  # Import the Window module
from component.minesweeper_game import MinesweeperGame

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (800, 600)  
        Window.resizable = False
        self.win_count = 0  
        self.lose_count = 0 
        self.main_layout = BoxLayout(orientation="vertical")

        self.top_bar = BoxLayout(size_hint_y=None, height=80, padding=[10, 10], spacing=10)

        with self.top_bar.canvas.before:
            Color(0.5, 0.7, 0.4, 1)
            self.top_bg = Rectangle(size=self.top_bar.size, pos=self.top_bar.pos)
        self.top_bar.bind(size=self.update_top_background, pos=self.update_top_background)

        left_layout = BoxLayout(size_hint_x=0.2, spacing=10, padding=[10, 0])

        back_layout = RelativeLayout(size_hint=(None, None), size=(50, 50))
        back_icon = Image(source="image/back_icon.png", size_hint=(None, None), size=(50, 50))
        back_layout.add_widget(back_icon)

        self.back_button = Button(size_hint=(None, None), size=(50, 50),
                          background_color=(0, 0, 0, 0),
                          background_normal='')
        back_layout.add_widget(self.back_button)
        self.back_button.bind(on_press=self.go_back)

        reset_layout = RelativeLayout(size_hint=(None, None), size=(50, 50))
        reset_icon = Image(source="image/reset_icon.png", size_hint=(None, None), size=(50, 50))
        reset_layout.add_widget(reset_icon)

        self.reset_button = Button(size_hint=(None, None), size=(50, 50),
                           background_color=(0, 0, 0, 0),
                           background_normal='')
        reset_layout.add_widget(self.reset_button)
        self.reset_button.bind(on_press=self.reset_game)

        left_layout.add_widget(back_layout)
        left_layout.add_widget(reset_layout)

        center_layout = BoxLayout(size_hint_x=0.6, spacing=10, padding=[120, 0, 0, 0])
        self.title_label = Label(text="[b][color=#F7F2C3]Gardensweeper[/color][/b]",  
                                    markup=True,  
                                    font_size=35,
                                    font_name="fonts/PressStart2P-Regular.ttf")
        center_layout.add_widget(self.title_label)

        right_layout = BoxLayout(size_hint_x=0.4, spacing=5, padding=[5, 0])

        self.timer_label = Label(text="Time: 00:00", font_size=20, color=(0, 0, 0, 1), size_hint_x=None, width=150)
        self.remaining_flags_label = Label(text="flags: 0", font_size=20, color=(0, 0, 0, 1), size_hint_x=None, width=200)
        self.stats_label = Label(text="Wins: 0 | Losses: 0", font_size=20, color=(0, 0, 0, 1), size_hint_x=None, width=200)

        right_layout.add_widget(self.timer_label)
        right_layout.add_widget(self.remaining_flags_label)
        right_layout.add_widget(self.stats_label)

        self.top_bar.add_widget(left_layout)
        self.top_bar.add_widget(center_layout)
        self.top_bar.add_widget(right_layout)

        self.main_layout.add_widget(self.top_bar)

        self.board_container = FloatLayout()
        with self.board_container.canvas.before:
            Color(0.5, 0.7, 0.4, 1)
            self.bg_rect = Rectangle(size=self.board_container.size, pos=self.board_container.pos)

        self.board_container.bind(size=self.update_background, pos=self.update_background)
        self.main_layout.add_widget(self.board_container)

        self.add_widget(self.main_layout)

        # Create a layout for the hint, flag mode, and pause buttons
        bottom_layout = BoxLayout(size_hint=(1, 0.1), padding=[10, 10], spacing=10, pos_hint={"center_x": 0.5, "center_y": 0.1})

        hint_button = Button(text="Hint (10)", size_hint=(0.2, 1))
        hint_button.bind(on_press=self.show_hint)
        self.hint_counter = 0  # ตัวนับการใช้ Hint
        self.max_hints = 10    # กำหนดจำนวนครั้งสูงสุด
        self.hint_button = hint_button  # เก็บ reference ปุ่มไว้
        bottom_layout.add_widget(self.hint_button)

        self.flag_mode_button = Button(text="Bomb Mode", size_hint=(0.2, 1),
                                       background_color=(0.6, 0.2, 0.2, 1), background_normal='')
        self.flag_mode_button.bind(on_press=self.toggle_flag_mode)
        bottom_layout.add_widget(self.flag_mode_button)

        self.pause_button = Button(text="Pause", size_hint=(0.2, 1))
        self.pause_button.bind(on_press=self.toggle_pause)
        bottom_layout.add_widget(self.pause_button)

        self.main_layout.add_widget(bottom_layout)

        self.flag_mode = False
        self.timer = 0
        self.timer_event = None
        
        #อันนี้เพลงตอนเล่นนะจ้ะ
        self.bg_music = SoundLoader.load("soundeffect/song.mp3")
        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.volume = 0.5
            self.bg_music.play() 

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
        self.game_board.stop_timer_callback = self.stop_timer  # Set the stop timer callback

        self.update_flag_count(self.game_board.remaining_flags)

        self.reset_timer()

    def update_flag_count(self, remaining_flags):
        self.remaining_flags_label.text = f"flags: {remaining_flags}"

    def go_back(self, instance):
        self.manager.current = "difficulty"
        self.stop_timer()
        
        self.hint_counter = 0
        self.hint_button.text = f"Hint ({self.max_hints})"
        self.hint_button.disabled = False
        
        if self.bg_music:
            self.bg_music.stop()

        self.bg_music = SoundLoader.load("soundeffect/song.mp3")
        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.volume = 0.5
            self.bg_music.play()
        

    def toggle_flag_mode(self, instance):
        if self.game_board.game_over:  
            return
        
        self.flag_mode = not self.flag_mode
        if self.flag_mode:
            self.flag_mode_button.text = "Flag Mode"
            self.flag_mode_button.background_color = (0.2, 0.6, 0.2, 1)
        else:
            self.flag_mode_button.text = "Bomb Mode"
            self.flag_mode_button.background_color = (0.6, 0.2, 0.2, 1)
        if hasattr(self, 'game_board'):
            self.game_board.flag_mode = self.flag_mode


    def update_timer(self, dt):
        self.timer += 1
        minutes, seconds = divmod(self.timer, 60)
        self.timer_label.text = f"Time: {minutes:02}:{seconds:02}"

    def reset_timer(self):
        self.timer = 0
        self.timer_label.text = "Time: 00:00"
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

            if self.bg_music:
                self.bg_music.stop()

            self.bg_music = SoundLoader.load("soundeffect/song.mp3")
            if self.bg_music:
                self.bg_music.loop = True
                self.bg_music.volume = 0.5
                self.bg_music.play()

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
        if hasattr(self, "game_board") and self.game_board.game_over:  
            self.play_end_game_sound()
            self.calculate_game_stat()

    def show_hint(self, instance):
        if self.game_board.game_over:  # ถ้าเกมจบ ห้ามใช้ Hint
            return 
        
        if self.hint_counter < self.max_hints:
            self.game_board.give_hint()
            self.hint_counter += 1
            remaining_hints = self.max_hints - self.hint_counter
            self.hint_button.text = f"Hint ({remaining_hints})"

            if self.hint_counter >= self.max_hints:
                self.hint_button.text = "No hints available!"
                self.hint_button.disabled = True
                
    def play_end_game_sound(self):
        if self.bg_music:  
            self.bg_music.stop()
        
        if self.game_board.win == True:
            self.bg_music = SoundLoader.load("soundeffect/win.mp3")
            if self.bg_music:
                self.bg_music.volume = 0.6
                self.bg_music.play()  
        else:
            self.bg_music = SoundLoader.load("soundeffect/OOF.mp3")
            if self.bg_music:
                self.bg_music.volume = 1
                self.bg_music.play()  
                
                
    def calculate_game_stat(self):
        if self.game_board.win == True:
            self.win_count += 1  
        else:
            self.lose_count += 1
        self.update_stats_label()
        self.game_board.win = False
        

    def toggle_pause(self, instance):
        if self.game_board.game_over:  
            return
        
        if self.timer_event:  
            if self.timer_event.is_triggered:  
                self.timer_event.cancel()  
                self.pause_button.text = "Resume"
            else:
                self.timer_event = Clock.schedule_interval(self.update_timer, 1)  
                self.pause_button.text = "Pause"
    
    def update_stats_label(self):
         new_text = f"Wins: {self.win_count} | Losses: {self.lose_count}"
         if self.stats_label.text != new_text:  
            self.stats_label.text = new_text
 
            Clock.schedule_once(lambda dt: setattr(self.stats_label, 'text', new_text))
