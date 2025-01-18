import numpy as np
import pygame as pg
import time
import threading
from object import RigidBody, Ground
import collision
from ui import App_parameters, Create_Object

class App:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1600, 900
        self.mouse_pos = (0, 0)
        self.click = False
        self.clicked = False
        self.font16 = pg.font.SysFont('Corbel', 16)
        self.focused = True

        #simulation parameters
        self.background_color = (135, 205, 235)
        self.FPS = 120
        self.air_density = 1.23
        self.drag = True
        self.collision = True
        self.g = 9.81
        self.gravity = False

        self.interacting_ = False
        self.tool = 'dragging'
        self.tools = [[pg.image.load('assets/drag_icon.jpg'), True, 'dragging', 'Click on an object to drag it'], 
                      [pg.image.load('assets/fix_icon.jpg'), True, 'fix', 'Click on an object to fix it'], 
                      [pg.image.load('assets/create_icon.png'), True, 'create', 'Click on the screen where you want to add an object']
                      ]
        self.buttons = [[pg.image.load('assets/param_icon.png')]
                        ]
        
        self.rigid_bodies = []

        for object in self.rigid_bodies:
            if object.shape == 'polygon':
                vertices, color = object.step()
                object.rect = pg.draw.polygon(self.screen, color, vertices)
            elif object.shape == 'circle':
                pos, radius, color = object.step()
                object.rect = pg.draw.circle(self.screen, color, pos, radius)
        
    def run(self):
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()

        self.running = True
        while self.running:
            if self.focused:
                self.mouse_pos = pg.mouse.get_pos()
                self.screen.fill(self.background_color)

                self.clicked = True if self.click else False
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False
                self.click = pg.mouse.get_pressed()[0]

                self.update()
                self.UI()
                self.interact()

                pg.display.flip()
                pg.display.set_caption('Py-Physics Simulator  |  ' + str(round(self.clock.get_fps())))
            self.clock.tick(self.FPS)

    def interact(self):
        if not self.interacting_:
            if self.tool != None:
                if self.click and (not self.clicked) and (not pg.Rect(0, 0, self.WIDTH, 100).collidepoint(self.mouse_pos)):
                    for i, object in enumerate(self.rigid_bodies):
                        if object.rect.collidepoint(self.mouse_pos):
                            if self.tool == 'dragging':
                                if object.fixed == False:
                                    thread0 = threading.Thread(target=self.dragging, args=(i, ))
                                    thread0.start()
                            elif self.tool == 'fix':
                                object.fix(True if not object.fixed else False)
                    if self.tool == 'create':
                        x, y = self.mouse_pos
                        self.external_ui = Create_Object()
                        self.external_ui.run()
                        args = self.external_ui.args
                        if not args == 'cancel':
                            self.rigid_bodies.append(RigidBody(x, y, len(self.rigid_bodies), args))

    def UI(self):
        pg.draw.rect(self.screen, (0, 0, 0), (0, 0, self.WIDTH, 100))

        for i, j in enumerate(self.tools):
            x, y = 25 + (25 + 50)*i, 25
            self.screen.blit(j[0], (x, y))

            if self.click and j[0].get_rect(topleft=(x, y)).collidepoint(self.mouse_pos) and not self.clicked:
                j[1] = True if j[1] == False else False
                self.tool = None if j[1] else self.tool

                if not j[1]:
                    for k in self.tools:
                        if k != j: 
                            k[1] = True

            self.tool = j[2] if not j[1] else self.tool
            if self.tool == j[2]:
                text = self.font16.render(j[3], True, (255, 255, 255), (0, 0, 0))
                self.screen.blit(text, text.get_rect(bottomleft=self.mouse_pos))

            pg.draw.line(self.screen, (0, 0, 0), (x, y), (x + 48, y + 48), 5) if j[1] else 0

        x_offset =  75 + (25 + 50)*(len(self.tools)-1)
        #pg.draw.rect(self.screen, (255, 255, 255), pg.Rect())
        for i, j in enumerate(self.buttons):
            x, y = 25 + x_offset + (25 + 50) * i, 25
            self.screen.blit(j[0], (x, y))

            if self.click and j[0].get_rect(topleft=(x, y)).collidepoint(self.mouse_pos) and not self.clicked:
                if i == 0:
                    args = {'bg': self.background_color, 'fps': self.FPS, 'air_density': self.air_density, 'drag': self.drag, 
                            'collision': self.collision, 'g': self.g, 'gravity': self.gravity}
                    self.external_ui = App_parameters(args)
                    self.external_ui.run()

                    if self.external_ui.submitted:
                        try:
                            self.background_color, self.FPS, self.air_density = self.external_ui.background_color, int(self.external_ui.FPS.get()), float(self.external_ui.air_density.get())
                            self.drag, self.collision, self.g, self.gravity = self.external_ui.drag.get(), self.external_ui.collision.get(), float(self.external_ui.g.get()), self.external_ui.gravity.get()
                        except:
                            print('error while updating parameters')
                    del self.external_ui

    def dragging(self, index: int):
        self.interacting_ = True
        while self.click:
            pos_0 = (self.rigid_bodies[index].x, self.rigid_bodies[index].y)
            pg.draw.line(self.screen, (50, 50, 50), pos_0, self.mouse_pos)
            pg.draw.line(self.screen, (50, 50, 50), pos_0, (self.mouse_pos[0], pos_0[1]))
            pg.draw.line(self.screen, (50, 50, 50), pos_0, (pos_0[0], self.mouse_pos[1]))
            text0 = self.font16.render(str(round(-pos_0[0]+self.mouse_pos[0], 1))+ '  N', True, (200, 200, 200), (0, 0, 0))
            text1 = self.font16.render(str(round(-pos_0[1]+self.mouse_pos[1], 1))+ '  N', True, (200, 200, 200), (0, 0, 0))
            rect0 = text0.get_rect(center=((pos_0[0]+self.mouse_pos[0])/2, pos_0[1]))
            rect1 = text1.get_rect(center=(pos_0[0], (pos_0[1]+self.mouse_pos[1])/2))
            self.screen.blit(text0, rect0)
            self.screen.blit(text1, rect1)
            pg.display.update([rect0, rect1])
            time.sleep(1/self.FPS/2)
        self.rigid_bodies[index].add_force(self.mouse_pos[0]-pos_0[0], self.mouse_pos[1]-pos_0[1])
        self.interacting_ = False

    def update(self):
        for object in self.rigid_bodies: object.get_parameters(1/self.FPS, self.air_density, self.g, self.drag, self.gravity)

        if self.collision:
            for objectA in self.rigid_bodies:
                for objectB in self.rigid_bodies:
                    if objectA.id != objectB.id and not (objectA.fixed == True and objectB.fixed == True):
                            if objectA.shape == 'polygon' and objectB.shape == 'polygon':
                                is_collided, normal, depth = collision.intersect_rect_rect(objectA, objectB)
                            if objectA.shape == 'circle' and objectB.shape == 'circle':
                                is_collided, normal, depth = collision.intersect_circle_circle(objectA, objectB)
                            if objectA.shape == 'polygon' and objectB.shape == 'circle':
                                is_collided, normal, depth = collision.intersect_rect_circle(objectA, objectB)
                            if objectA.shape == 'circle' and objectB.shape == 'polygon':
                                is_collided, normal, depth = collision.intersect_circle_rect(objectA, objectB)

                            if is_collided:
                                if objectA.fixed:
                                    objectB.move(normal[0]*depth, normal[1]*depth)
                                elif objectB.fixed:
                                    objectA.move(-normal[0]*depth, -normal[1]*depth)
                                else:
                                    objectA.move(-normal[0]*depth/2, -normal[1]*depth/2)
                                    objectB.move(normal[0]*depth/2, normal[1]*depth/2)

                                self.resolve_collison(objectA, objectB, normal)

        for object in self.rigid_bodies:
            if object.shape == 'polygon':
                vertices, color = object.step()
                object.rect = pg.draw.polygon(self.screen, color, vertices)
            elif object.shape == 'circle':
                pos, radius, color = object.step()
                object.rect = pg.draw.circle(self.screen, color, pos, radius)

            if object.fixed and object.id != -1:
                pg.draw.circle(self.screen, (0, 0, 0), (object.x, object.y), object.width/2/3, width=3)
                pg.draw.line(self.screen, (0, 0, 0), (object.x-np.cos(np.pi/4)*object.width/2/3, object.y-np.cos(np.pi/4)*object.width/2/3), 
                            (object.x+np.cos(np.pi/4)*object.width/2/3, object.y+np.cos(np.pi/4)*object.width/2/3), width=3)
                pg.draw.line(self.screen, (0, 0, 0), (object.x-np.cos(np.pi/4)*object.width/2/3, object.y+np.cos(np.pi/4)*object.width/2/3), 
                            (object.x+np.cos(np.pi/4)*object.width/2/3, object.y-np.cos(np.pi/4)*object.width/2/3), width=3)

    def resolve_collison(self, objectA: RigidBody, objectB: RigidBody, normal: tuple) -> None:
        v_ab = (objectB.v[0] - objectA.v[0], objectB.v[1] - objectA.v[1])

        if np.dot(v_ab, normal) > 0:
            return False

        j = -(1+min(objectA.restitution, objectB.restitution))*np.dot(v_ab, normal)
        j /= (1/objectA.mass if not objectA.fixed else 0) + (1/objectB.mass if not objectB.fixed else 0) + 0.00001
        
        objectA.add_velocity(-j / objectA.mass * normal[0] * (not objectA.fixed), -j / objectA.mass * normal[1] * (not objectA.fixed))
        objectB.add_velocity(j / objectB.mass * normal[0] * (not objectB.fixed), j / objectB.mass * normal[1] * (not objectB.fixed))

if __name__ == '__main__':
    pg.init()
    pg.display.init()
    pg.font.init()
    app = App()
    app.run()
    pg.quit()
