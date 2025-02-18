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