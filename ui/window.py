import pygame as pg


class Window:
    def __init__(self, RES: tuple = (400, 400), title: str = 'Window'):
        self.WIDTH, self.HEIGHT = self.RES = RES
        self.x, self.y = 0, 0
        self.title = title

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

    def checkbox(self, x: int = 0, y: int = 0, var: bool= '') -> int:
        self.widgets.append({'x': x, 'y': y, 'var': var})
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
    
    def update(self, mouse_pos, click, pos):
        self.surface.fill((25, 25, 25))

        title = self.font30.render(self.title, True, (255, 255, 255), (50 ,50, 50))
        title_rect = title.get_rect(topleft=(0, 0))
        self.surface.blit(title, title_rect)

        for i in self.widgets:
            content, rect = i.update((True if i.rect.collidepoint((mouse_pos[0]-pos[0], mouse_pos[1]-pos[1])) else False, click))
            self.surface.blit(content, rect)

        for i, j in self.variables:
            j[0] = self.widgets[j[1]].get()

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
            if args[0] and args[1]:
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

    def get(self):
        return self.content


class Checkbox:
    def __init__(self, x, y, var):
        self.x, self.y = x, y
        self.content = var

    def get(self):
        return self.content
    
    def update(self):
        
    
if __name__ == '__main__':
    screen = pg.display.set_mode((1000, 500))

    window = Window()
    window.button('hello world', 100, 100)
    running = True
    while running:
        screen.fill((200, 0, 0))
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.blit(window.update(mouse_pos, 0, (10, 10)), (10, 10))
        pg.display.flip()