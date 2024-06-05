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
    TheFoundation = Univers(name='The Foundation',step=0.0005, dimensions=(0.55,0.5) )


    # Question 4
    # To test the modes here i declared an initial speed which will show us the moves here, if we put the same signe for V0 then,
    # they are in the in-phase mode, otherwise, the are in anti phase, as show in my simulation here
    V0 = 0.1

    TheFoundation.springOn = False  # this allow us to see the moves with ivisible springs, (if you want to see the magic springs, 
                                    # just set it "True" )

    L1 = 0.1
    L2 = L1
    L3 = L1

    K1 = 10
    K3 = K1
    K2 = K1/2




    # En phase
    P_fix1 = Particule(p0=Vecteur3D(0.125,0.25,0),fix=True,name="bedRock",color="white")
    P_41 = Particule(p0=calculatePos(P_fix1.getPosition(), l1=L1,angle=90) , v0=Vecteur3D(V0,0,0),mass=5)
    P_42 = Particule(p0=calculatePos(P_41.getPosition(), l1=L2,angle=90) , v0=Vecteur3D(V0,0,0), color="orange",mass=5)
    P_fix2 = Particule(p0=calculatePos(P_42.getPosition(), l1=L3,angle=90),fix=True,name="bedRock",color="white")
    
    # If you want to see the behavior in the opposing phase, please comment the lines above and uncomment the following 5 lines by on #
    # # En opposition de phase  
    # P_fix1 = Particule(p0=Vecteur3D(0.125,0.25,0),fix=True,name="bedRock",color="white")
    # P_41 = Particule(p0=calculatePos(P_fix1.getPosition(), l1=L1,angle=90) , v0=Vecteur3D(V0,0,0),mass=5)
    # P_42 = Particule(p0=calculatePos(P_41.getPosition(), l1=L2,angle=90) , v0=Vecteur3D(-V0,0,0), color="orange",mass=5)
    # P_fix2 = Particule(p0=calculatePos(P_42.getPosition(), l1=L3,angle=90),fix=True,name="bedRock",color="white")


    # I removed the gravity here since the experiment should be done on a surface, and vertically, therefore the gravity would be canceled by the normal 
    # force of the surface
    f_spring1 = SpringDamper(k=K1, c=.1, l0=L1, particules=[P_fix1,P_41])
    f_spring2 = SpringDamper(k=K2, c=.1, l0=L2, particules=[P_41,P_42])
    f_spring3 = SpringDamper(k=K3, c=.1, l0=L3, particules=[P_42,P_fix2])


    TheFoundation.addAgent(P_fix1,P_41,P_42,P_fix2)

    TheFoundation.addGenerators( f_spring1, f_spring2, f_spring3)

    TheFoundation.simulateRealTime(scale=1000,background=(30,30,30))


    N = len(P_41.position)
    t = len(TheFoundation.time)
    posX1 =[]
    posX2 =[]
    for i in range(N) :
        posX1.append(P_41.position[i].x)
        posX2.append(P_42.position[i].x)



    figure()
    plot(TheFoundation.time,posX1, label="m1")
    plot(TheFoundation.time,posX2, label="m2")
    title("Déplacement Horizontal en fonction du temps")
    xlabel("temps[s]")
    ylabel("deplacement Horizontal[m]")
    legend()
    grid()
    show()



    sys.exit()