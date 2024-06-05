# -*- coding: utf-8 -*-

from math import exp,cos,sin,pi
from pylab import figure,legend,show,plot,grid,title,xlabel,ylabel # type: ignore
from vecteur3D import Vecteur3D
import pygame  # type: ignore

angle_visu = 60  # Angle de visualisation entre l'axe horizontal et l'axe visuelle qu'on veut rajouter dans ce cas l'axe rajouté pointe vers l'ecran
angle_visu = angle_visu * pi / 180

class MoteurCC():
    """     class representing a direct current motor   """

    def __init__(self, pos = Vecteur3D(),color = "cyan",name="DC motor", R=0, Kc=0.1, Ke=0.01, J=0.01, f=0.1, L=0):
        """
        Args:
            name (str, optional): type of the motor. Defaults to "DC motor".
            R (float): induced resistance. Defaults to 0.
            Kc (float): torque constant. Defaults to 0.1.
            Ke (float): counter electromotive constant. Defaults to 0.01.
            J (float): rotor's inertia. Defaults to 0.01.
            f (float): fluid friction. Defaults to 0.1.
            L (float): self inductance of the motor. Defaults to 0.
        """
        self.name = name
        self.r = R
        self.kc = Kc
        self.ke = Ke
        self.j = J
        self.f = f
        self.l = L # self inductance (not used for now)
        self.v = 0  # Voltage
        self.cr = 0 # Resistif torque
        self.viscosity = 0  # the environement's viscosity
        self.i = [0] # Intensity
        self.torque = [0]
        self.speed = [0] # Angular velocity
        self.positionAng = [0] # Angular position
        self.speed_theoritical = [0] # Theoritical angular velocity
        self.t = [0]  # time of simulation 
        self.position = pos
        self.color = color

    
    def __str__(self):
        """
        Returns:
            string: gives us information about the motor
        """
        return f"DC motor ( R = {self.r} ohm, Kc = {self.kc} N.m/A, Ke = {self.ke} V.S, J = {self.j} kg.m^2, f = {self.f} N.m.S, L = {self.l} H)"
    
    
    def __repr__(self):
        return str(self)
    
    
    def setVoltage(self,voltage):
        self.v = voltage
    

    def getpositionAng(self):
        return self.positionAng[-1]
    

    def getSpeed(self):
        return self.speed[-1]
    

    def getTorque(self):
        return self.torque[-1]
    

    def getIntensity(self):
        return self.i[-1]
    

    def getTime(self):
        # Returns the simulation's time
        return self.t[-1]


    def addInertia(self, IAdded):
        # The user adds The load's Inertia if he wants, or it could be used in the 2nd part of the project
        self.j += IAdded
    

    def environementSViscosity(self, viscosity):
        # If there's an environement viscosity, it's gonna be add-up and be taken into account
        self.f += viscosity


    def addTorque(self, TorqueAdded):
        # external Torque, stored in the attribut cr and is gonna be used in addedTorque in each step of the simulation
        self.cr += TorqueAdded


    def addedTorque(self):
        # This updates the torque each time with external Torque in consideration
        self.torque[-1] += self.cr     

    
    def simule(self,step=0.1):
        # Simulate the motor for one step of times
        self.UpdateParameters(step)


    def UpdateParameters(self,step):
        # Time update
        self.t.append(self.getTime() + step) 

        # Intensity update
        E = self.getSpeed()*self.ke # Fem 
        self.i.append((self.v - E )/self.r)  # intensity update with L = 0 
        # In case L !=0 , please comment the two lines above and uncomment the following line  
        # self.i.append(self.rungeKutta (self.funcI,self.getTime(),step,self.getIntensity())) 
       
        # Torque update
        self.torque.append(self.kc * self.getIntensity())  
        self.addedTorque()

        # Speed calculation numérical value
        speed = self.rungeKutta (self.funcspeed, self.getTime(),step,self.getSpeed()) # Using Runge-Kutta 4th order
        self.speed.append(speed) # rad/s

        # Angular Position calculation rad
        self.positionAng.append(self.getSpeed()*step + self.getpositionAng())  
        
        # Speed calculation Theorical value
        tau = self.r * self.j / (self.ke * self.kc + self.r * self.f)
        k = self.kc / (self.ke * self.kc + self.r * self.f)
        self.speed_theoritical.append(k * self.v * (1 - exp(-self.getTime() / tau) ))

        """
        # Theorithical calculation of speed if L != 0
        xsi = 0.5 * (self.f * self.l + self.r * self.j)/(sqrt(self.j * self.l * (self.ke * self.kc + self.r * self.f)))
        wn = sqrt((self.ke * self.kc + self.r * self.f)/(self.j * self.l))
        ks = self.kc / (self.ke * self.kc + self.r * self.f)
        if xsi > 1 : 
            p1 = -xsi *wn + wn *sqrt(xsi**2 - 1)
            p2 = -xsi *wn - wn *sqrt(xsi**2 - 1)
            speed = ks * self.v * (1 - (p2*exp(p1 * self.getTime())/(p2-p1)) + (p1 *exp(p2 * self.getTime())/(p2-p1) ))
        else : 
            phi = atan(sqrt(1-xsi**2)/xsi)
            speed = ks * self.v * (1 - exp(-xsi*wn*self.getTime()/sqrt(1-xsi**2))*sin(wn*sqrt(1-xsi**2)*self.getTime() + phi))
        self.speed.append(speed)
        """
        # Three other methodes to calculate the speed
        # speed = self.getSpeed()+step*(self.getTorque()-self.f*self.getSpeed())/self.j # Using euler explicit 
        # speed = (step * self.getTorque() + self.j * self.getSpeed())/(self.j + self.f * step ) # less accurate
        # speed = self.getTorque() * (1 - exp(-self.f * self.getTime()/self.j)) / self.f # less*2 accurate


    def rungeKutta (self, func, time, step, var): 
        """
            func : is the function that's gonna be used, depends on what variable we want to determine
            time : isn't really necessary here but just to make it look like the runge kutta methode
            step : is the step that determines the periode between each calculation
            var : is the variable to be determined via the Runge-Kutta methode
        """ 
        k1 = step * func(time, var)
        k2 = step * func(time + step / 2, var + k1 * step / 2)
        k3 = step * func(time + step / 2, var + k2 * step / 2)
        k4 = step * func(time + step, var + step * k3)
        speedn = var + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        return speedn


    def funcspeed(self, t, speed):
        # This function is used in the runge kutta methode for speed calculation
        return (self.getTorque() - self.f * speed) / self.j


    def funcI(self,t,intensity):
        # This function is used in the runge kutta methode for Intensity calculation
        E = self.getSpeed()*self.ke # Fem 
        return (self.v-E-self.r*intensity) / self.l
    

    def plotVel(self,label="omega_L(t)"):

        plot(self.t, self.speed,label=label)
        #plot(self.t, m.speed_theoritical, label="omega_no_L(t)")

    def plotPos(self,label="omega_L(t)"):

        plot(self.t, self.positionAng,label=label)

    def gameDraw(self, scale, screen):

        _, H = screen.get_size()
        
        # Coordonnées réelles
        X = int(scale * self.position.x)
        Y = int(scale * self.position.y)
        Z = int(scale * self.position.z)
        
        # Coordonnées visualisées
        X = X - Z * cos(angle_visu)
        Y = Y - Z * sin(angle_visu)

        size = 2

        if type(self.color) is tuple:
            color = (self.color[0] * 255, self.color[1] * 255, self.color[2] * 255)
        else:
            color = self.color

        # Affichage du moteur
        pygame.draw.circle(screen, color, (X, H - Y), size * 2, size)
    
    def plot(self):
        pass


        
    
    


    


#Main###Main###Main###Main###Main###Main###Main###Main###Main###Main###Main
####Main###Main###Main###Main###Main###Main###Main###Main###Main###Main####
if __name__ == '__main__':

    # Behaviour in an Open Loop
    m = MoteurCC(R=1, Kc=0.1, Ke= 0.01, J=0.01, f= 0.1, L=0.1)  # If you want to use L != 0 then go to the function UpdateParameters 
                                                                # And follow the instructions
    
    print(m)

    t = 0
    step = 0.001
    temps = [t]

    while t<2 :

        t = m.getTime()

        m.setVoltage(1)
        m.simule(step)

    figure()
    m.plotVel()
    title("Réponse indicielle de la vitesse ")
    xlabel("temps[s]")
    ylabel("Omega[rad/s]")
    legend()
    grid()
    show()
