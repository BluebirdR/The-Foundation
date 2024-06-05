# -*- coding: utf-8 -*-

from vecteur3D import Vecteur3D
from math import pi, tan, sin, cos
import pygame  # type: ignore
import sys
from pygame.locals import *  # type: ignore
from time import time
from random import random
from Run_moteurCC import MoteurCC

angle_visu = 60  # Angle de visualisation entre l'axe horizontal et l'axe visuelle qu'on veut rajouter dans ce cas l'axe rajouté pointe vers l'ecran
angle_visu = angle_visu * pi / 180


class Particule(object):

    def __init__(self, mass=0.1, p0=Vecteur3D(), v0=Vecteur3D(), a0=Vecteur3D(), fix=False, name="paf", color='red',
                 test=False):
        self.mass = mass
        self.position = [p0]
        self.speed = [v0]
        self.acceleration = [a0]
        self.name = name
        self.color = color
        self.forces = Vecteur3D()
        self.fix = fix
        self.test = test


    def __str__(self):
        msg = 'Particule (' + str(self.mass) + ', ' + str(self.position[-1]) + ', ' + str(self.speed[-1]) + ', ' + str(
            self.acceleration[-1]) + ', "' + self.name + '", "' + str(self.color) + '" )'
        return msg


    def __repr__(self):
        return str(self)


    def getPosition(self):
        return self.position[-1]


    def getSpeed(self):
        return self.speed[-1]
    

    def pfd(self, step):

        if not self.fix:
            a = self.forces * (1 / self.mass)
            v = self.speed[-1] + a * step
        else:
            a = Vecteur3D()
            v = Vecteur3D()

        p = self.position[-1] + 0.5 * a * step ** 2 + self.speed[-1] * step

        self.acceleration.append(a)
        self.speed.append(v)
        self.position.append(p)
        self.forces = Vecteur3D()


    def applyForce(self, *args):
        for f in args:
            self.forces += f


    def plot(self):
        from pylab import plot  # type: ignore
        X = []
        Y = []
        for p in self.position:
            X.append(p.x)
            Y.append(p.y)

        return plot(X, Y, color=self.color, label=self.name) + plot(X[-1], Y[-1], 'o', color=self.color)


    def gameDraw(self, scale, screen):

        _, H = screen.get_size()
        
        # Coordonnées réelles
        X = int(scale * self.getPosition().x)
        Y = int(scale * self.getPosition().y)
        Z = int(scale * self.getPosition().z)
        
        # Coordonnées visualisées
        X = X - Z * cos(angle_visu)
        Y = Y - Z * sin(angle_visu)

        # Vitesses réelles
        vit = self.getSpeed()
        VX = int(scale * vit.x)
        VY = int(scale * vit.y)
        VZ = int(scale * vit.z)

        # Vitesses Visualisées
        VX = VX - VZ * cos(angle_visu)
        VY = VY - VZ * sin(angle_visu)

        size = 2

        if type(self.color) is tuple:
            color = (self.color[0] * 255, self.color[1] * 255, self.color[2] * 255)
        else:
            color = self.color

        # Affichage de la particule
        pygame.draw.circle(screen, color, (X, H - Y), size * 2, size)
        pygame.draw.line(screen, color, (X, H - Y), (X + VX, H - (Y + VY)))
        
        """
        # Attempt to make the particule disapear if it's going farther
        alpha = (255/abs(Z)) if Z<0 else 255
        if type(self.color) is tuple:
            color = (self.color[0] * 255, self.color[1] * 255, self.color[2] * 255, alpha)
        else:
            color = pygame.Color(self.color)
            color = color[:3] + (alpha,)

        if self.test:
            # Create a color with the desired alpha transparency
            transparent_color = pygame.Color(255, 255, 0,255)
            transparent_color.a=(100)  # Set alpha to 100 for semi-transparency
            print(transparent_color.a)

            pygame.draw.circle(screen, transparent_color, (W//4, H//4), 20)
            print(int(scale * self.getPosition().z))
        """



class Univers(object):

    def __init__(self, t0=0, step=0.01, name="plage", population=[], dimensions=(1024, 512), springOn= True):

        self.name = name
        self.time = [t0]
        self.population = population
        self.step = step
        self.dimensions = dimensions

        self.mouseControlled = []
        self.keyControlled = []
        self.generators = []

        self.springOn = springOn # condition to show the Springs or not 


    def __str__(self):
        ret = "Univers (" + str(self.time[-1]) + "," + str(self.step) + ", " + self.name + ", " + str(
            self.population) + ")"
        return ret


    def __repr__(self):
        return str(self)


    def addAgent(self, *args):

        for agent in args:
            self.population.append(agent)

        return len(self.population)


    def addGenerators(self, *args):

        for g in args:
            self.generators.append(g)


    def gameInit(self, scale=1, fps=60, background=(0, 200, 0)):

        """
            - Initializes pygame
            - creates the window
        """

        pygame.init()
        self.t0 = time()

        self.clock = pygame.time.Clock()
        self.background = background
        self.fps = fps
        self.scale = scale
        self.running = True

        self.W = self.dimensions[0] * self.scale
        self.H = self.dimensions[1] * self.scale

        self.targetX = 0
        self.targetY = 0

        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption(self.name)


    def gameInteraction(self):

        # Inputs
        self.gameKeys = pygame.key.get_pressed()  # It gets the states of all keyboard keys.


        # Ends the simulation if escape or the red cross button is clicked on
        for event in pygame.event.get():
            if event.type == QUIT: # type: ignore
                self.running = False

        if self.now > self.gameEndTime or self.gameKeys[K_ESCAPE]:  # type: ignore
            self.running = False


        for generator in self.keyControlled:
            generator.active = False
            if self.gameKeys[ord('p')] :  # And if the key is K_DOWN:
                generator.active = not generator.active
                print("Key pressed")


            
    def gameUpdate(self):
        """
            This function is used for three things:
                - Checking the user Interactions with the game
                - simulating the universe
                - display all the necessary information
        """
        # Updating the time
        self.now = time() - self.t0

        # Checking if there's any interaction with the universe
        self.gameInteraction()

        # Aplying the existant forces and simulate the environement
        while self.time[-1] < self.now :
            for p in self.population:
                for generator in self.generators:
                    generator.setForce(p)
            self.simulate()
        

        ## Display part of the game

        # Creating the background and some data to be always displayed such as the time 
        self.screen.fill(self.background)
        font_obj = pygame.font.Font('freesansbold.ttf', 12)
        text_surface_obj = font_obj.render(('time: %.2f' % self.now), True, 'green', self.background)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.topleft = (0, 0)
        self.screen.blit(text_surface_obj, text_rect_obj)

        # Displaying the reference axis
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.H / 2), (self.W, self.H / 2))  # Axe x
        pygame.draw.line(self.screen, (255, 255, 255), (self.W / 2, 0), (self.W / 2, self.H))  # Axe y
        pygame.draw.line(self.screen, (255, 255, 255), (self.W / 2 + self.H / (2 * tan(angle_visu)), 0),
                         (self.W / 2 - self.H / (2 * tan(angle_visu)), self.H))  # Axe z

        # Displaying the population
        for agent in self.population:
            agent.gameDraw(self.scale, self.screen)

        # Displaying the Spring/Pendulum/Link unless we decide to set it off
        if self.springOn : 
            for generator in self.generators:
                if isinstance(generator,SpringDamper):

                    p0Pos = generator.particules[0].getPosition()
                    # Coordonnées réelles
                    X0 = int(self.scale * p0Pos.x)
                    Y0 = int(self.scale * p0Pos.y)
                    Z0 = int(self.scale * p0Pos.z)
                    # Coordonnées visualisées
                    X0 = X0 - Z0 * cos(angle_visu)
                    Y0 = Y0 - Z0 * sin(angle_visu)
                    
                    p1Pos = generator.particules[1].getPosition()
                    # Coordonnées réelles
                    X1 = int(self.scale * p1Pos.x)
                    Y1 = int(self.scale * p1Pos.y)
                    Z1 = int(self.scale * p1Pos.z)
                    # Coordonnées visualisées
                    X1 = X1 - Z1 * cos(angle_visu)
                    Y1 = Y1 - Z1 * sin(angle_visu)
                    
                    pygame.draw.line(self.screen, (random()*255,random()*255,random()*255), (X0, self.H - Y0), (X1, self.H - Y1),width=5) # Discooo

        # Making what we displayed visible
        pygame.display.update()
        self.clock.tick(self.fps)



    def simulateRealTime(self, scale=1, fps=60, background=(3, 34, 76), tfin=50000000):
        """
            Simulation based on the real time

        Args:
            scale (float): of the display. Defaults to 1.
            fps (int): frame per seconds. Defaults to 60.
            background (tuple, optional): [description]. Defaults to (3, 34, 76).
            tfin (float): time limit of the simulation. Defaults to 50000000 seconds.
        """
        # Setting the time limit
        self.gameEndTime = tfin

        # Starting the game
        self.gameInit(scale, fps, background)

        # Time to play
        while self.running:
            self.gameUpdate()

        # either the time limit is reached or the user wants to stop it
        pygame.quit()


    def simulate(self):

        # Updating the position, speed and acceleration of each element
        for agent in self.population:
            if isinstance(agent,Particule):
                agent.pfd(self.step)

        self.time.append(self.time[-1] + self.step)


    def simulateTo(self, tFin):
        # It was used before the "simulateRealTime" methode
        while self.time[-1] < tFin:
            self.simulate()
    

    def plot(self):
        # A plot to show each agent of the population and it's trajectory
        from pylab import figure, legend, show, xlabel, ylabel,title  # type: ignore

        figure(self.name)

        for agent in self.population:
            agent.plot()
        
        title("Trajectoire des Particules dans l'Univers ''"+self.name+"''")
        xlabel("Position en x[m]")
        ylabel("Position en y[m]")
        legend()
        show()



## Generators

class Force(object):

    def __init__(self, force=Vecteur3D(), name='force', active=True):
        self.force = force
        self.name = name
        self.active = active


    def __str__(self):
        return "Force (" + str(self.force) + ', ' + self.name + ")"


    def __repr__(self):
        return str(self)


    def setForce(self, particule):
        if self.active and isinstance(particule,Particule):
            particule.applyForce(self.force)




class ForceSelect(Force):
    # A force that applies only to the selected particules
    def __init__(self, force=Vecteur3D(), name='force', particules=[], active=True):
        Force.__init__(self, force, name, active)
        self.particules = particules


    def setForce(self, particule):
        if self.active and particule in self.particules and isinstance(particule,Particule):
            particule.applyForce(self.force)




class Gravity(Force):
    # Applies the gravity on each particule 
    def __init__(self, force=Vecteur3D(0, -9.81, 0), name='gravity', active=True):
        Force.__init__(self, force, name, active)


    def setForce(self, particule):
        if self.active and isinstance(particule,Particule):
            particule.applyForce(self.force * particule.mass)




class SpringDamper(Force):

    def __init__(self, force=Vecteur3D(), name='SpringDamper', active=True, k=1000, c=100, l0=5, particules=[]):
        Force.__init__(self, force, name, active)
        self.k = k
        self.c = c
        self.l0 = l0
        self.particules = particules  # ne doit contenir que deux elements


    def setForce(self, particule):
        
        if self.active and particule in self.particules and isinstance(particule,Particule):
            
            deformation = self.particules[1].getPosition() - self.particules[0].getPosition()
            dx = deformation.mod()-self.l0

            vitesse_diff = self.particules[1].getSpeed() - self.particules[0].getSpeed()
            vect_vit = vitesse_diff ** deformation.norm() # Projection suivant l'axe de la deformation

            resultante = (self.c * vect_vit + self.k * dx )* deformation.norm()
            
            if particule == self.particules[0]:
                self.particules[0].applyForce(resultante)
            else:
                self.particules[1].applyForce(-resultante)




class Viscosity(Force):

    def __init__(self, force=Vecteur3D(0, -9.81, 0), name='viscosity', active=True,viscosity=1e-6):
        Force.__init__(self, force, name, active)
        self.viscosity = viscosity


    def setForce(self, particule):
        if self.active and isinstance(particule,Particule):
            particule.applyForce(-particule.getSpeed()*self.viscosity)




class Link(SpringDamper):
    # A rigide spring used as rods or threads
    def __init__(self, P0, P1):
        l0 = (P0.getPosition()-P1.getPosition()).mod()
        SpringDamper.__init__(self,k=1000,c=100,l0=l0,active=True,name="Link",particules=[P0,P1])
    



class Prismatic(SpringDamper):

    def __init__(self,P0, P1, axis=Vecteur3D(1,0,0)):
        self.P0 = P0
        self.P1 = P1
        self.axis = axis.norm()
        l = self.P1.getPosition() - self.P0.getPosition()
        l0 = (l ** self.axis)*self.axis
        SpringDamper.__init__(self,particules=[self.P0, self.P1],l0=l0.mod())


    def setForce(self, particule):
    
        if self.active and particule in self.particules and isinstance(particule,Particule):
            deformation = self.particules[1].getPosition() - self.particules[0].getPosition()
            deformation_proj = deformation - deformation**self.axis *self.axis
            dx = deformation_proj.mod() - self.l0

            vitesse_diff = self.particules[1].getSpeed() - self.particules[0].getSpeed()
            vect_vit = vitesse_diff ** deformation_proj.norm() # Projection suivant l'axe de la deformation
    
 
            resultante = (self.c * vect_vit + self.k * dx )* deformation_proj.norm()
        
            if particule == self.P0:
                particule.applyForce(resultante)
            else:
                particule.applyForce(-resultante)
    




## Main
if __name__ == '__main__':
    from pylab import figure, show, legend  # type: ignore

    P0 = Particule(v0=Vecteur3D(10, 10, 0))
    print(P0)

    while P0.getPosition().y >= 0.:
        P0.applyForce(Vecteur3D(0, -9.81, 0))
        P0.pfd(0.001)

    figure()                
    P0.plot()
    legend()
    show()
