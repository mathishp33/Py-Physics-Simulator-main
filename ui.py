import threading

class Parameters:
    def __init__(self, args):
        import integred_ui.window_manager as wm
        import integred_ui.window as window
        self.thread = None
        self.window = window.Window((400, 400), 'window 1')
        self.window.button('hello world', 100, 100)

        self.window_manager = wm.WindowManager(self.window)

    def run(self):
        self.thread = threading.Thread(target=self.window_manager.run)
        self.thread.run()
        print('done')

    def update(self) -> tuple:
        return self.window_manager.window_surf, self.window_manager.window_rect