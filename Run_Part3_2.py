# -*- coding: utf-8 -*-

from Run_particuleM import *
from math import sin,cos,pi
from pylab import figure,legend,show,plot,grid,title,xlabel,ylabel # type: ignore


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


    L1 = 0.1
    L2 = 0.2 
    L3 = 0.3 

    angle = 10

    # 1st Pendulum
    P_fix1 = Particule(p0=Vecteur3D(1, 0.5, -0.1),fix=True,name="bedRock",color="white")
    P_21 = Particule(p0=calculatePos(P_fix1.getPosition(), l1=L1,angle=angle) , v0=Vecteur3D(0,0,0),mass=1)

    # 2nd Pendulum
    P_fix2 = Particule(p0=Vecteur3D(1, 0.5, -0.15),fix=True,name="bedRock",color="white")
    P_22 = Particule(p0=calculatePos(P_fix2.getPosition(), l1=L2,angle=angle) , v0=Vecteur3D(0,0,0), color="orange",mass=1)
    
    # 3rd Pendulum
    P_fix3 = Particule(p0=Vecteur3D(1, 0.5, -0.2),fix=True,name="bedRock",color="white")
    P_23 = Particule(p0=calculatePos(P_fix3.getPosition(), l1=L3,angle=angle) , v0=Vecteur3D(0,0,0), color="yellow",mass=1)

    # Creating the Forces
    f_gravity = Gravity(Vecteur3D(0,-9.81,0),active=True)
    f_link1 = Link(P_fix1, P_21)
    f_link2 = Link(P_fix2, P_22)
    f_link3 = Link(P_fix3, P_23)

    # Adding the particules and the forces into TheFoundation
    TheFoundation.addAgent(P_fix1, P_fix2, P_fix3, P_21, P_22, P_23)
    TheFoundation.addGenerators(f_gravity, f_link1, f_link2, f_link3)


    TheFoundation.simulateRealTime(scale=400,background=(30,30,30))


    N = len(P_21.position)
    posX1 =[]
    posX3 =[]
    posX2 =[]

    for i in range(N) :
        posX1.append(P_21.position[i].x)
        posX2.append(P_22.position[i].x)
        posX3.append(P_23.position[i].x)


    figure()
    plot(TheFoundation.time,posX1, label="L = 0.1m")
    plot(TheFoundation.time,posX2, label="L = 0.2m")
    plot(TheFoundation.time,posX3, label="L = 0.3m")
    title("Déplacement Horizontal des 3 Masses Accrochées aux Pendules Associés")
    xlabel("temps[s]")
    ylabel("deplacement Horizontal[m]")
    legend()
    grid()
    show()


    sys.exit()
    
