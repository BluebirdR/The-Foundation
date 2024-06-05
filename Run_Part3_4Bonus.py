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
    TheFoundation = Univers(name='The Foundation',step=0.0005, dimensions=(0.6,0.5) )
    
    # Question 4 (bonus part)
    # this is a système with 4 Masses + 5 Springs we can go for as much masses and springs as we want the phenomenon are just amazing 
    # to see
    V0 = 0.1

    TheFoundation.springOn = False  # this allow us to see the moves with ivisible springs, (if you want to see the magic springs, 
                                    # just set it "True" )

    L1 = 0.1

    K1 = 10
    K3 = K1
    K2 = K1/2

    m = 5

    P_fix1 = Particule(p0=Vecteur3D(0.0625,0.25,0),fix=True,name="bedRock",color="white")
    P_41 = Particule(p0=calculatePos(P_fix1.getPosition(), l1=L1,angle=90) , v0=Vecteur3D(V0,0,0), mass=m)
    P_42 = Particule(p0=calculatePos(P_41.getPosition(), l1=L1,angle=90) , v0=Vecteur3D(-V0,0,0), color="orange", mass=m)
    P_43 = Particule(p0=calculatePos(P_42.getPosition(), l1=L1,angle=90) , v0=Vecteur3D(V0,0,0), color="yellow", mass=m)
    P_44 = Particule(p0=calculatePos(P_43.getPosition(), l1=L1,angle=90) , v0=Vecteur3D(-V0,0,0), color="green", mass=m)
    P_fix2 = Particule(p0=calculatePos(P_44.getPosition(), l1=L1,angle=90),fix=True,name="bedRock",color="white", mass=m)

    # I removed the gravity here since the experiment should be done on a surface, therefore the gravity would be canceled by the normal 
    # force of the surface

    f_spring1 = SpringDamper(k=K1, c=.1, l0=L1, particules=[P_fix1,P_41])
    f_spring2 = SpringDamper(k=K2, c=.1, l0=L1, particules=[P_41,P_42])
    f_spring3 = SpringDamper(k=K2, c=.1, l0=L1, particules=[P_42,P_43])
    f_spring4 = SpringDamper(k=K2, c=.1, l0=L1, particules=[P_43,P_44])
    f_spring5 = SpringDamper(k=K3, c=.1, l0=L1, particules=[P_44,P_fix2])


    TheFoundation.addAgent(P_fix1,P_41,P_42,P_43,P_44,P_fix2)

    TheFoundation.addGenerators( f_spring1, f_spring2, f_spring3 ,f_spring4, f_spring5)

    TheFoundation.simulateRealTime(scale=1000,background=(30,30,30))


    N = len(P_41.position)
    t = len(TheFoundation.time)
    posX1 =[]
    posX2 =[]
    posX3 =[]
    posX4 =[]
    for i in range(N) :
        posX1.append(P_41.position[i].x)
        posX2.append(P_42.position[i].x)
        posX3.append(P_43.position[i].x)
        posX4.append(P_44.position[i].x)



    figure()
    plot(TheFoundation.time,posX1, label="m1")
    plot(TheFoundation.time,posX2, label="m2")
    plot(TheFoundation.time,posX3, label="m3")
    plot(TheFoundation.time,posX4, label="m4")
    title("Déplacement Horizontal en fonction du temps")
    xlabel("temps[s]")
    ylabel("deplacement Horizontal[m]")
    legend()
    grid()
    show()



    sys.exit()