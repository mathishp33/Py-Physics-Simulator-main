import customtkinter as ctk
import numpy as np

class AskShape():
    def __init__(self, shape):
        self.obj = []
        self.vertices = []
        self.next_vertice = None
        self.interacting = False
        self.width, self.height = 1200, 700
        self.is_submitted = False
        self.shape = shape

    def add_vertice_manually(self):
        self.interacting = True
        dialog = ctk.CTkInputDialog(title='Add Vertice', text='Enter vertice coordinates (x, y):')
        try:
            input_ = dialog.get_input()
            input_ = input_.replace('(', '').replace(')', '')
            pos = tuple(map(int, input_.split(',')))
            x, y = pos[0]+self.width//2, self.height//2-pos[1]
            self.vertices.append((x, y))
            self.update_vertices()
        except:
            print('Invalid input')
        self.interacting = False

    def add_vertice(self, event=None):
        if not self.interacting:
            if event != None:
                x, y = event.x, event.y
            if not self.is_finished():
                self.vertices.append((x, y))
                self.update_vertices()
        else:
            return None
        
    def draw_missing_vertice(self, event):
        if not self.interacting and ((len(self.vertices) > 0 and self.shape == 'polygon') or (len(self.vertices) == 0 and self.shape == 'circle') or (len(self.vertices) == 1 and self.shape == 'rectangle')):
            self.next_vertice = (event.x, event.y)
            self.update_vertices()
    def complete_shape(self):
        if len(self.vertices) > 2 and self.shape == 'polygon':
            self.canvas.create_line(self.next_vertice[0], self.next_vertice[1], self.vertices[0][0], self.vertices[0][1], fill='red')
        
    def is_finished(self):
        if self.shape == 'circle':
            if len(self.vertices) == 1:
                return True
        elif self.shape == 'rectangle':
            if len(self.vertices) == 2:
                return True
        elif self.shape == 'polygon':
            if len(self.vertices) > 20:
                return True
        return False

    def update_vertices(self):
        self.canvas.delete('all')

        self.canvas.create_text(150, 20, text='Draw the shape by clicking on the canvas', font=('Arial', 12), fill='black')
        self.canvas.create_text(150, 50, text='Here is the scale : 100 pixel = 1 m', font=('Arial', 12), fill='black')
        self.canvas.create_text(150, 80, text='The origin (0, 0) is at the center', font=('Arial', 12), fill='black')

        self.canvas.create_line(self.width/2-20, self.height/2, self.width/2+20, self.height/2, fill='black')
        self.canvas.create_line(self.width/2, self.height/2+20, self.width/2, self.height/2-20, fill='black')

        if self.shape == 'polygon':
            for j, i in enumerate(self.vertices):
                self.canvas.create_oval(i[0]-5, i[1]-5, i[0]+5, i[1]+5, fill='black')
                if j != 0:
                    self.canvas.create_line(self.vertices[j-1][0], self.vertices[j-1][1], i[0], i[1], fill='black')
        elif self.shape == 'circle':
            if len(self.vertices) > 0:
                self.canvas.create_aa_circle(self.width/2, self.height/2, int(np.hypot(self.vertices[0][0]-self.width/2, self.vertices[0][1]-self.height/2)), fill='black')
        elif self.shape == 'rectangle':
            if len(self.vertices) > 1:
                self.canvas.create_rectangle(self.vertices[0][0], self.vertices[0][1], self.vertices[1][0], self.vertices[1][1], outline='black')

        if not self.is_finished():
            if self.shape == 'polygon':
                if self.next_vertice != None and len(self.vertices) > 0:
                    self.canvas.create_oval(self.next_vertice[0]-5, self.next_vertice[1]-5, self.next_vertice[0]+5, self.next_vertice[1]+5, fill='blue')
                    self.canvas.create_line(self.vertices[-1][0], self.vertices[-1][1], self.next_vertice[0], self.next_vertice[1], fill='blue')
            elif self.shape == 'circle':
                if self.next_vertice != None and len(self.vertices) == 0:
                    self.canvas.create_aa_circle(self.width/2, self.height/2, int(np.hypot(self.next_vertice[0]-self.width/2, self.next_vertice[1]-self.height/2)), fill='blue')
            elif self.shape == 'rectangle':
                if self.next_vertice != None and len(self.vertices) == 1:
                    self.canvas.create_rectangle(self.vertices[0][0], self.vertices[0][1], self.next_vertice[0], self.next_vertice[1], outline='blue')

        self.complete_shape()

    def undo(self):
        if len(self.vertices) > 0:
            self.canvas.delete('all')
            self.vertices.pop()
            self.update_vertices()
            self.complete_shape()

    def on_start(self, event):
        self.update_vertices()
        self.root.unbind('<Visibility>', self.root.bind('<Visibility>', self.on_start))

    def submit(self):
        if self.is_finished():
            if self.shape == 'circle':
                radius = np.hypot(self.vertices[0][0]-self.width/2, self.vertices[0][1]-self.height/2)
                self.vertices = radius
            elif self.shape == 'rectangle':
                self.corners = [self.vertices[0], (self.vertices[0][0], self.vertices[1][1]), self.vertices[1], (self.vertices[1][0], self.vertices[0][1])]
                self.vertices = self.corners

        self.is_submitted = True
        self.stop()

    def stop(self):
        self.root.quit()
        self.root.after(100, self.root.destroy)

    def draw_shape(self):
        self.root = ctk.CTk()
        self.root.title('Draw Shape')
        self.root.geometry(f'{self.width}x{self.height+200}')
        self.root.resizable(False, False)
        ctk.set_appearance_mode('dark')

        self.obj.append(ctk.CTkButton(self.root, text='Add Vertice Manually', font=('Arial', 20), corner_radius=16, command=self.add_vertice_manually))
        self.obj[-1].grid(row=0, column=0, pady=20, padx=20)
        self.obj.append(ctk.CTkButton(self.root, text='Undo', font=('Arial', 20), corner_radius=16, command=self.undo))
        self.obj[-1].grid(row=0, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkButton(self.root, text='Submit', font=('Arial', 20), corner_radius=16, command=self.submit))
        self.obj[-1].grid(row=0, column=2, pady=20, padx=20)
        self.obj.append(ctk.CTkButton(self.root, text='Cancel', font=('Arial', 20), corner_radius=16, command=self.stop))
        self.obj[-1].grid(row=0, column=3, pady=20, padx=20)

        self.canvas = ctk.CTkCanvas(self.root, width=self.width, height=self.height, bg='ivory')
        self.canvas.grid(row=1, column=0, columnspan=4, pady=20, padx=20)

        self.canvas.bind('<Button-1>', self.add_vertice)
        self.canvas.bind('<Motion>', self.draw_missing_vertice)

        self.root.bind('<Visibility>', self.on_start)

        self.root.mainloop()