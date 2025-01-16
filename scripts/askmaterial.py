import customtkinter as ctk

class AskMaterial():
    def __init__(self):
        self.density = 1200
        self.restitution = 0.3
        self.friction = 0.5

        self.obj = []

    def custom_material(self):
        self.root = ctk.CTk()
        self.root.title('Choose Material')
        self.root.resizable(False, False)
        ctk.set_appearance_mode('dark')

        self.obj.append(ctk.CTkLabel(self.root, text='Density:', font=('Arial', 20), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=0, column=0, pady=20, padx=20)
        self.obj.append(ctk.CTkLabel(self.root, text='Restitution:', font=('Arial', 20), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=1, column=0, pady=20, padx=20)
        self.obj.append(ctk.CTkLabel(self.root, text='Friction Coeff:', font=('Arial', 20), corner_radius=16, fg_color='white', text_color='black'))
        self.obj[-1].grid(row=2, column=0, pady=20, padx=20)

        self.obj.append(ctk.CTkEntry(self.root, font=('Arial', 20), corner_radius=16, border_width=5))
        self.obj[-1].grid(row=0, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkEntry(self.root, font=('Arial', 20), corner_radius=16, border_width=5))
        self.obj[-1].grid(row=1, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkEntry(self.root, font=('Arial', 20), corner_radius=16, border_width=5))
        self.obj[-1].grid(row=2, column=1, pady=20, padx=20)

        self.obj.append(ctk.CTkButton(self.root, text='Submit', font=('Arial', 20), corner_radius=16, command=self.custom_meterial_end))
        self.obj[-1].grid(row=3, column=1, pady=20, padx=20)
        self.obj.append(ctk.CTkButton(self.root, text='Cancel', font=('Arial', 20), corner_radius=16, command=self.stop))
        self.obj[-1].grid(row=3, column=0, pady=20, padx=20)

        self.root.mainloop()

    def custom_meterial_end(self):
        try:
            self.density = float(self.obj[3].get())
            self.restitution = float(self.obj[4].get())
            self.friction = float(self.obj[5].get())

            self.stop()
        except:
            print('error occured, wrong informations, try again')
        
    def stop(self):
        self.root.quit()
        self.root.after(100, self.root.destroy)
