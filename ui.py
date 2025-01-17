import customtkinter as ctk
from scripts.CTkColorPicker import *

class Create_Object():
    def __init__(self):

        self.obj = []

        self.pad_y = 20
        self.pad_x = 20

        self.densities = {'Caoutchouc': 1500, 'Steel': 7800, 'Glass': 2500, 'Stone': 2400, 'Wood': 600, 'Helium': 0.5, 'Ice': 900, 'Gold': 19300} #g/L
        self.restitutions = {'Caoutchouc': 0.8, 'Steel': 0.8, 'Glass': 0.5, 'Stone': 0.2, 'Wood': 0.4, 'Helium': 0.3, 'Ice': 0.05, 'Gold': 0.1} 
        self.frictions = {'Caoutchouc': 0.8, 'Steel': 0.8, 'Glass': 0.5, 'Stone': 0.2, 'Wood': 0.4, 'Helium': 0.3, 'Ice': 0.05, 'Gold': 0.1}

        self.args = {'material': 'Wood', 'shape': 'circle', 'vertices': 100, 'color': (0, 255, 0)}

    def ask_color(self):
        pick_color = AskColor()
        color = pick_color.get()
        color = (int(color[1:3], base=16), int(color[3:5], base=16), int(color[5:7], base=16))
        self.args['color'] = color

    def ask_material(self, event):
        from scripts.askmaterial import AskMaterial
        self.args['material'] = self.obj[5].get()
        if self.obj[5].get() == 'Cutom Material':
            pick_material = AskMaterial()
            pick_material.custom_material()
            self.args['density'] = pick_material.density
            self.args['restitution'] = pick_material.restitution
            self.args['friction'] = pick_material.friction

    def ask_shape(self, event):
        from scripts.askshape import AskShape
        shape = self.obj[3].get().lower()
        self.args['shape'] = shape
        pick_shape = AskShape(shape=shape)
        pick_shape.draw_shape()
        if pick_shape.is_submitted:
            self.args['vertices'] = pick_shape.vertices
        
    def submit(self):
        try:
            if self.args['material'] != 'Custom Material':
                self.args['density'] = self.densities[self.args['material']]
                self.args['restitution'] = self.restitutions[self.args['material']]
                self.args['friction'] = self.frictions[self.args['material']]
                
            self.drag_coeffs = {'polygon': 0.9, 'rectangle': 1, 'circle': 0.5}
            self.args['drag coeff'] = self.drag_coeffs[self.args['shape']]
        except:
            print('wrong material informations')

        
        if all(i in list(self.args.keys()) for i in ['shape', 'density', 'restitution', 'friction', 'vertices', 'shape', 'color']):
            self.stop()
        else:
            print('error while creating object, maybe you forgot to input arguments')

    def cancel(self):
        self.args = 'cancel'
        self.stop()

    def stop(self):
        self.root.quit()
        self.root.destroy()

    def run(self):

        self.root = ctk.CTk()
        self.root.title('Create an Object')
        self.root.resizable(False, False)
        ctk.set_appearance_mode('dark')

        self.obj.append(ctk.CTkLabel(self.root, text='Object Shape:', font=('Arial', 20), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=0, column=0, pady=self.pad_y, padx=self.pad_x)
        self.obj.append(ctk.CTkLabel(self.root, text='Object Color:', font=('Arial', 20), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=1, column=0, pady=self.pad_y, padx=self.pad_x)
        self.obj.append(ctk.CTkLabel(self.root, text='Object Material:', font=('Arial', 20), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=2, column=0, pady=self.pad_y, padx=self.pad_x)

        self.obj.append(ctk.CTkComboBox(self.root, font=('Arial', 20), values=["Circle", "Rectangle", "Polygon"], corner_radius=16, border_width=5, command=self.ask_shape, hover=True))
        self.obj[-1].grid(row=0, column=1, pady=self.pad_y, padx=self.pad_x)
        self.obj.append(ctk.CTkButton(self.root, text='Choose Color', font=('Arial', 20), corner_radius=16, command=self.ask_color))
        self.obj[-1].grid(row=1, column=1, pady=self.pad_y, padx=self.pad_x)
        self.obj.append(ctk.CTkComboBox(self.root, font=('Arial', 20), values=["Caoutchouc", "Steel", "Glass", "Stone", "Wood", "Helium", "Ice", "Gold", "Cutom Material"], 
                                        corner_radius=16, border_width=5, hover=True, command=self.ask_material))
        self.obj[-1].grid(row=2, column=1, pady=self.pad_y, padx=self.pad_x)

        self.obj.append(ctk.CTkButton(self.root, text='Submit', font=('Arial', 20), corner_radius=16, command=self.submit))
        self.obj[-1].grid(row=5, column=1, pady=self.pad_y, padx=self.pad_x)
        self.obj.append(ctk.CTkButton(self.root, text='Cancel', font=('Arial', 20), corner_radius=16, command=self.cancel))
        self.obj[-1].grid(row=5, column=0, pady=self.pad_y, padx=self.pad_x)

        self.root.mainloop()


class App_parameters:
    def __init__(self, args):
        self.background_color = args['bg']
        self.FPS = args['fps']
        self.air_density = args['air_density']
        self.drag = args['drag']
        self.collision = args['collision']
        self.g = args['g']
        self.gravity = args['gravity']

        self.submitted = False
        self.obj = []

    def submit(self):
        self.submitted = True

        self.stop()

    def stop(self):
        self.root.quit()
        self.root.destroy()

    def ask_color(self):
        pick_color = AskColor()
        color = pick_color.get()
        color = (int(color[1:3], base=16), int(color[3:5], base=16), int(color[5:7], base=16))
        self.background_color = color
    
    def run(self):
        self.root = ctk.CTk()
        self.root.title('Modify Simulation Parameters')
        self.root.resizable(False, False)
        ctk.set_appearance_mode('dark')

        self.obj.append(ctk.CTkLabel(self.root, text='Background Color:', font=('Arial, 20'), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=0, column=0, padx=20, pady=20)
        self.obj.append(ctk.CTkLabel(self.root, text='Images per sec. :', font=('Arial, 20'), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=1, column=0, padx=20, pady=20)
        self.obj.append(ctk.CTkLabel(self.root, text='Air Density:', font=('Arial, 20'), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=2, column=0, padx=20, pady=20)
        self.obj.append(ctk.CTkLabel(self.root, text='Allow Dragging:', font=('Arial, 20'), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=3, column=0, padx=20, pady=20)
        self.obj.append(ctk.CTkLabel(self.root, text='Allow Collisions:', font=('Arial, 20'), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=4, column=0, padx=20, pady=20)
        self.obj.append(ctk.CTkLabel(self.root, text='Allow Gravity:', font=('Arial, 20'), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=5, column=0, padx=20, pady=20)
        self.obj.append(ctk.CTkLabel(self.root, text='Gravity Acceleration:', font=('Arial, 20'), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=6, column=0, padx=20, pady=20)

        self.obj.append(ctk.CTkButton(self.root, text='Choose Background Color', font=('Arial', 20), corner_radius=16, command=self.ask_color))
        self.obj[-1].grid(row=0, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkEntry(self.root, font=('Arial', 20), corner_radius=16, border_width=5))
        self.obj[-1].grid(row=1, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkEntry(self.root, font=('Arial', 20), corner_radius=16, border_width=5))
        self.obj[-1].grid(row=2, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkCheckBox(self.root, corner_radius=16, border_color=5))
        self.obj[-1].grid(row=3, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkCheckBox(self.root, corner_radius=16, border_color=5))
        self.obj[-1].grid(row=4, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkCheckBox(self.root, corner_radius=16, border_color=5))
        self.obj[-1].grid(row=5, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkEntry(self.root, font=('Arial', 20), corner_radius=16, border_width=5))
        self.obj[-1].grid(row=6, column=1, pady=20, padx=20)

        self.obj.append(ctk.CTkLabel(self.root, text='s^-1', font=('Arial', 20), corner_radius=16))
        self.obj[-1].grid(row=1, column=2, pady=20, padx=20)
        self.obj.append(ctk.CTkLabel(self.root, text='g/L', font=('Arial', 20), corner_radius=16))
        self.obj[-1].grid(row=2, column=2, pady=20, padx=20)
        self.obj.append(ctk.CTkLabel(self.root, text='m/s^2', font=('Arial', 20), corner_radius=16))
        self.obj[-1].grid(row=6, column=2, pady=20, padx=20)

        self.obj.append(ctk.CTkButton(self.root, text='Submit', font=('Arial', 20), corner_radius=16, command=self.submit))
        self.obj[-1].grid(row=3, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkButton(self.root, text='Cancel', font=('Arial', 20), corner_radius=16, command=self.cancel))
        self.obj[-1].grid(row=3, column=0, pady=20, padx=20)

        self.root.mainloop()
    

if __name__ == '__main__':
    window = None