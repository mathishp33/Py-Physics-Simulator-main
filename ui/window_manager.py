import pygame as pg

class WindowManager:
    def __init__(self, window):
        self.click = False
        self.clicked = False
        self.running = True
        self.mouse_pos = (0, 0)
        self.pressed_keys = []
        self.clock = pg.time.Clock()

        self.window = window
        self.window_surf = None
        self.window_rect = None
        self.x, self.y = 0, 0

    def run(self):
        while self.running:
            self.clicked = True if not self.click else False
            self.click = pg.mouse.get_pressed()[0]
            self.mouse_pos = pg.mouse.get_pos()
            self.pressed_keys = pg.key.get_pressed()

            self.running = self.window.running
            self.x, self.y = self.window.x, self.window.y
            self.window_surf = self.window.update(self.mouse_pos, self.click, (self.x, self.y), self.clicked)
            self.window_rect = (self.x, self.y)

            self.clock.tick(180)
        
        return False