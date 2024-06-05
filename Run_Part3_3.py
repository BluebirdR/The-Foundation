# -*- coding: utf-8 -*-

from Run_particuleM import *
from math import sin,cos,pi


def calculatePos(pos1=Vecteur3D(),l1=0.2,angle=20):
    """
        this function will calculate the coordinate of a particule to create a pendulum based on a fixed particule pos1(or a mobil 
        particule in the case of 2pendulums connected), a length l1 and the angle from the vertical line to l1

    """
    angle = angle*pi/180

    X = pos1.x + l1 * sin(angle)
    Y = pos1.y - l1 * cos(angle)
    Z = pos1.z

    return Vecteur3D(X,Y,Z)


if __name__ == '__main__':

    # Creation of the Universe
    TheFoundation = Univers(name='The Foundation',step=0.0005, dimensions=(2,1) )

    # Question 3
    # This simulation describes the chaotic moves that a double pendulum makes, and we can repeat it in the simulation as much as we want,
    # but if it's the réality, the smallest change of height would change the trajectory taken and this is just mind blowing, we can visualize it here with  details
    L1 = 0.15
    L2 = 0.10


    P_fix = Particule(p0=Vecteur3D(1,0.5,0),fix=True,name="bedRock",color="white")
    P_31 = Particule(p0=calculatePos(P_fix.getPosition(), l1=L1,angle=120) , v0=Vecteur3D(0,0,0), mass=1,name="cat")
    P_32 = Particule(p0=calculatePos(P_31.getPosition(), l1=L2,angle=120) , v0=Vecteur3D(0,0,0), color="orange",mass=0.5, name="ciao")

    f_gravity = Gravity(Vecteur3D(0,-1,0),active=True)
    f_link1 = Link(P_fix, P_31)
    f_link2 = Link(P_31, P_32)


    TheFoundation.addAgent(P_fix,P_31,P_32)

    TheFoundation.addGenerators(f_gravity, f_link1, f_link2)



    TheFoundation.simulateRealTime(scale=400,background=(30,30,30))

    TheFoundation.plot()


    sys.exit()
    
