import numpy as np
import pygame as pg

class RigidBody():
    def __init__(self, x: int, y: int, id: int, args: dict):
        self.x, self.y = x, y #cm, cm
        self.id = id
        self.color = args['color'] #RGB
        self.dry_friction_coeff = args['friction']
        self.drag_coeff = args['drag coeff']
        self.restitution = args['restitution']
        self.shape = args['shape'] if args['shape'] != 'rectangle' else 'polygon'

        if self.shape == 'polygon':
            self.untouched_vertices = args['vertices']

        a = 0
        if self.shape == 'polygon':
            for i in range(len(self.untouched_vertices)):
                j=(i + 1) % len(self.untouched_vertices)
                a += self.untouched_vertices[i][0]*self.untouched_vertices[j][1] - self.untouched_vertices[j][0]*self.untouched_vertices[i][1]
            self.aera = 0.5*abs(a)
        elif self.shape == 'circle':
            self.radius = args['vertices']
            self.width = self.radius*2 #cm
            self.aera = np.pi*self.radius**2*10**-4 #m^2

        self.volume = self.aera*0.01 #m^3
        self.density = args['density'] #g/L

        self.mass = self.volume * self.density #Kg
        self.vertices = []
        self.rect = None

        self.f_x, self.f_y = [], [] #N, N
        self.f = np.array([0, 0]) #N
        self.a = np.array([0, 0]) #m/s^2
        self.v = np.array([0, 0]) #m/s

        self.k_energy = 0 #J
        self.p_energy = 0 #J
        self.energy = 0 #J

        self.inertia = 0 #Kg.m^2
        self.torque = 0 #N.m
        self.angular_a = 0 #°/s^2
        self.angular_v = 0 #°/s
        self.angle = 0 #°

        self.fixed = False

        self.delta_time = 1/120 #s
        self.g = 9.81 #m/s^2
        self.air_density = 1.23 #Kg/m^3
        self.drag = True
        self.gravity = True

    def move(self, x: float, y: float) -> tuple[float, float]:
        self.x = self.x + x
        self.y = self.y + y
        return self.x, self.y
    
    def add_velocity(self, vx: float, vy: float) -> tuple[float, float]:
        self.v = np.array([self.v[0]+vx, self.v[1]+vy])
        return self.v[0], self.v[1]

    def add_force(self, fx: float, fy: float) -> tuple[list, list]:
        self.f_x.append(fx)
        self.f_y.append(fy)
        return self.f_x, self.f_y
    
    def fix(self, is_fixed):
        self.fixed = is_fixed
        self.v = np.array([0, 0])
        self.a = np.array([0, 0])
        self.angular_v = 0
        self.angular_a = 0

    def step(self) -> tuple[str, list, tuple]:
        if self.rect != None:
            self.width, self.height = self.rect.width, self.rect.height

        if not self.fixed:
            if self.drag:
                self.f_y.append(0.5*self.air_density*-self.v[1]*self.drag_coeff)
                self.f_x.append(0.5*self.air_density*-self.v[0]*self.drag_coeff)
            if self.gravity:
                self.f_y.append(self.mass*self.g)

        self.f = np.array([np.sum(self.f_x), np.sum(self.f_y)])
        self.a = self.f/self.mass
        self.v = self.v+self.a*self.delta_time
        self.x, self.y = np.array([self.x, self.y]) + self.v

        if self.shape == 'polygon':
            self.vertices = [] # to do : convert to np.array
            angle_rad = np.radians(self.angle)
            for i, j in self.untouched_vertices:
                x_1 = i * np.cos(angle_rad) - j * np.sin(angle_rad)
                y_1 = i * np.sin(angle_rad) + j * np.cos(angle_rad)

                x_2 = x_1 + self.x
                y_2 = y_1 + self.y

                self.vertices.append((x_2, y_2))

        self.f_x, self.f_y = [], []
        if self.shape == 'polygon':
            return self.vertices, self.color
        elif self.shape == 'circle':
            return (self.x, self.y), self.radius, self.color
        
    def get_parameters(self, delta_time: float, air_density: float, g: float, drag: bool, gravity: bool) -> object:
        self.delta_time = delta_time
        self.air_density = air_density
        self.g = g
        self.gravity = gravity
        self.drag = drag
        return True



class Ground:
    def __init__(self, HEIGHT: int, WIDTH: int):
        self.width, self.height = WIDTH, 10 #cm, cm
        self.x, self.y = WIDTH/2, HEIGHT+self.height/2 #cm, cm
        self.id = -1
        self.shape = 'polygon'
        self.fixed = True
        self.aera = self.width*self.height*10**-4 #m^2
        self.volume = self.aera*0.01 #m^3
        self.density = 2.65*10**3 #Kg/m^3
        self.mass = self.volume * self.density #Kg
        self.restitution = 0.2
        self.v = np.array([0, 0])
        self.vertices = [(0, HEIGHT), (self.width, HEIGHT), (self.width, HEIGHT+self.height), (0, HEIGHT+self.height)]
        self.color = (0, 0, 0)
        self.rect = pg.Rect(0, HEIGHT, self.width, self.height)

    def step(self) -> tuple[list, list]:
        return self.vertices, self.color
    
    def add_velocity(self, vx: float, vy: float) -> tuple[float, float]:
        return self.v[0], self.v[1]

    def get_parameters(self, delta_time: float, air_density: float, g: float, drag: bool, gravity: bool) -> object:
        return True
