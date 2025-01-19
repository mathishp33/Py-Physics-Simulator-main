import pygame as pg
import threading

class Window:
    def __init__(self, RES: tuple = (400, 400), title: str = 'Window'):
        self.WIDTH, self.HEIGHT = self.RES = RES
        self.x, self.y = 0, 0
        self.title = title

        self.last_mouse_pos = (0, 0)
        self.running = True

        pg.font.init()
        self.font30 = pg.font.SysFont('Corbel', 30)

        self.widgets = [] #list like [object(args)]
        self.variables = {} # dict like {'element name': [value, widget_id]}

        self.surface = pg.Surface(self.RES)

    def label(self, text: str = '', x: int = 0, y: int = 0) -> int:
        self.widgets.append(Label(text, x, y))
        return len(self.widgets)-1
    
    def button(self, text: str= '', x: int = 0, y: int = 0, command: tuple = None) -> int:
        self.widgets.append(Button(text, x, y, command))
        return len(self.widgets)-1

    def entry(self, x: int = 0, y: int = 0, var: str= '', width: int = 150) -> int:
        self.widgets.append(Entry(x, y, var, width))
        return len(self.widgets)-1

    def checkbox(self, x: int = 0, y: int = 0, var: bool= False) -> int:
        self.widgets.append(Checkbox(x, y, var))
        return len(self.widgets)-1
    
    def variable(self, name='', var = 0, linked_widget: int = None) -> int:
        self.widgets.append({f'{name}': [var, linked_widget]})
        return len(self.widgets)-1
    
    def get_from_var(self, name: str = ''):
        if not name == '':
            return self.variables[name]
    
    def get_from_widget(self, id: int = 0):
        try:
            return self.widgets[id].content
        except:
            print('widget doesnt have a variable')
    
    def destroy_variable(self, name: str = ''):
        if not name == '':
            try: 
                del self.variables[name]
            except:
                print('variable doesnt exist')
        
    def destroy_widget(self, id: int = 0):
        try:
            del self.widgets[id]
        except:
            print('error occured while deleting object')

    def bar_update(self, mouse_pos, click, clicked):
        bar_rect = pg.draw.rect(self.surface, (100, 100, 100), pg.Rect(0, 0, self.WIDTH, 30))

        if clicked and click and bar_rect.collidepoint(self.surf_mouse_pos):
            self.x, self.y = self.x + (mouse_pos[0]-self.last_mouse_pos[0]), self.y + (mouse_pos[1]-self.last_mouse_pos[1])

        title = self.font30.render(self.title, True, (255, 255, 255), (50 ,50, 50))
        title_rect = title.get_rect(topleft=(0, 0))
        self.surface.blit(title, title_rect)

        close_rect = pg.draw.rect(self.surface, (255, 0, 0), pg.Rect(self.WIDTH-30, 0, 30, 30))
        pg.draw.line(self.surface, (0, 0, 0), (self.WIDTH-25, 5), (self.WIDTH-5, 25), 4)
        pg.draw.line(self.surface, (0, 0, 0), (self.WIDTH-5, 5), (self.WIDTH-25, 25), 4)
        if close_rect.collidepoint(self.surf_mouse_pos) and click:
            self.running = False
    
    def update(self, mouse_pos: tuple, click: bool, pos: tuple, clicked: bool):
        self.surface.fill((25, 25, 25))

        self.surf_mouse_pos = (mouse_pos[0]-pos[0], mouse_pos[1]-pos[1])

        self.bar_update(mouse_pos, click, clicked)

        for i in self.widgets:
            content, rect = i.update((True if i.rect.collidepoint(self.surf_mouse_pos) else False,
                                       click, clicked))
            self.surface.blit(content, rect)

        for i, j in self.variables:
            j[0] = self.widgets[j[1]].get()

        self.last_mouse_pos = mouse_pos

        return self.surface


class Button:
    def __init__(self, text, x, y, command):
        self.text = text
        self.x, self.y = x, y
        self.command = command
        self.font = pg.font.SysFont('Corbel', 16)

        self.Text = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.Text.get_rect(topleft=(self.x, self.y))

        self.state = False

    def get(self):
        return self.text
    
    def update(self, args):
        self.Text = self.font.render(self.text, True, (255, 255, 255), (100, 100, 100) if args[0] else None)
        self.rect = self.Text.get_rect(topleft=(self.x, self.y))

        self.state = False
        try:
            if args[0] and args[1] and not args[2]:
                self.state = True
                if self.command != None:
                    func = getattr(self.command[0], self.command[1])
                    return func(self.command[2]) 
        except:
            print('error occured while calling a function')

        return self.Text, self.rect


class Label:
    def __init__(self, text, x, y):
        self.text = text
        self.x, self.y = x, y
        self.font = pg.font.SysFont('Corbel', 16)

        self.Text = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.Text.get_rect(topleft=(self.x, self.y))

    def get(self):
        return self.text
    
    def update(self, args):
        return self.Text, self.rect


class Entry:
    def __init__(self, x, y, var, width):
        self.x, self.y = x, y
        self.content = var
        self.width = width
        
        self.focus_counter = 0
        self.focus = False
        self.thread0 = None
        self.new_content = self.content
        self.font = pg.font.SysFont('Corbel', 16)
        self.rect = pg.Rect(self.x, self.y, self.width, 20)

        self.surf = pg.Surface((self.width, 20))
        self.surf.fill((100, 100, 100))
        self.text = self.font.render(self.new_content, True, (255, 255, 255), (100, 100, 100))
        self.text_rect = self.text.get_rect(topleft=(0, 0))
        self.surf.blit(self.text, self.text_rect)

    def get(self):
        return self.content

    def update(self, args):
        if args[0] and args[1] and not args[2]:
            self.focus = True
        elif args[1] and not args[2]:
            self.focus = False

        self.new_content = self.content
        if self.focus:
            if self.thread0 == None:
                self.thread0 = threading.Thread(target=self.get_intput)
                self.thread0.start()

            self.focus_counter += 0.005
            self.new_content += '|' if int(self.focus_counter)%2 == 0 else ''

        else:
            self.thread0 = None

        self.surf.fill((100, 100, 100))
        self.text = self.font.render(self.new_content, True, (255, 255, 255), (100, 100, 100))
        self.text_rect = self.text.get_rect(topleft=(0, 0))
        self.surf.blit(self.text, self.text_rect)

        return self.surf, (self.x, self.y)

    def get_intput(self):
        while self.focus:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if not event.type == pg.K_RETURN:
                        try:
                            self.content = self.content + event.unicode
                        except:
                            print('error occured while adding letter to an entry')
                    if event.type == pg.K_BACKSPACE:
                        self.content = self.content[:-1]


class Checkbox:
    def __init__(self, x, y, var):
        self.x, self.y = x, y
        self.content = var

        self.surf = pg.Surface((20, 20))
        self.surf.fill((255 , 255, 255))
        self.rect = pg.Rect(self.x, self.x, 20, 20)

        if self.content:
            pg.draw.line(self.surf, (0, 0, 0), (0, 0), (20, 20), 3)
            pg.draw.line(self.surf, (0, 0, 0), (20, 0), (0, 20), 3)

    def get(self):
        return self.content
    
    def update(self, args):

        self.surf.fill((255 , 255, 255))
        self.rect = pg.Rect(self.x, self.x, 20, 20)

        if args[0] and args[1] and not args[2]:
            self.content = True if not self.content else False

        if self.content:
            pg.draw.line(self.surf, (0, 0, 0), (0, 0), (20, 20), 3)
            pg.draw.line(self.surf, (0, 0, 0), (20, 0), (0, 20), 3)

        return self.surf, self.rect
        
    
if __name__ == '__main__':
    screen = pg.display.set_mode((1000, 500))

    window = Window()
    window.button('hello world', 100, 100)
    window.checkbox(200, 200)
    window.entry(200, 350)

    clock = pg.time.Clock()
    click = False
    running = True
    while running:
        screen.fill((200, 0, 0))
        mouse_pos = pg.mouse.get_pos()
        clicked = True if click else False
        click = pg.mouse.get_pressed()[0]

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if window.running == False:
            running = False

        x, y = window.x, window.y
        screen.blit(window.update(mouse_pos, click, (x, y), clicked), (x, y))
        pg.display.flip()
        clock.tick(180)