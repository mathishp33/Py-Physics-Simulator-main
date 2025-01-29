import threading

class Parameters:
    def __init__(self, args):
        import ui.window_manager as wm
        import ui.window as w
        self.thread = None
        self.window = w.Window(400, 400)
        self.window.button('hello world', 100, 100)

        self.window_manager = wm.WindowManager(self.window)

    def run(self):
        self.thread = threading.Thread(target=self.window_manager.run)
        self.thread.run()

    def update(self) -> tuple:
        return self.window_manager.window_surf, self.window_manager.window_rect