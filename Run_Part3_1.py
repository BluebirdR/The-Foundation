# -*- coding: utf-8 -*-

from Run_particuleM import *
from pylab import figure, show, legend, plot, title, xlabel, ylabel, grid  # type: ignore


if __name__ == '__main__':

    # Creation of the Universe
    TheFoundation = Univers(name='The Foundation',step=0.0005, dimensions=(10,5) )


    #############################################################################################
    # Question 1
    #
    # If you want to activate the force presse on the letter "p" on your keyboard

    P_fix = Particule(p0=Vecteur3D(5,3,0),fix=True,name="bedRock",color="white")
    P_test = Particule(p0=Vecteur3D(5,2.5,0),v0=Vecteur3D(0,0,0),mass=1)

    l0 = (P_fix.getPosition()-P_test.getPosition()).mod()   # Calculate the initial length of the spring considering the mass 
                                                            # will be in equilibrium

    # Creating the forces to be applied 
    f_gravity = Gravity(Vecteur3D(0,-1,0),active=True)
    f_spring = SpringDamper(k=10, c=0.1, l0=l0, particules=[P_fix,P_test])
    f_down = ForceSelect(Vecteur3D(0,-2,0),active=False,particules=[P_test]) # Constant force

    # Adding the particules to The Foundation
    TheFoundation.addAgent(P_fix,P_test)

    # Adding the forces to The Foundation
    TheFoundation.addGenerators(f_spring,f_gravity,f_down)
    TheFoundation.keyControlled=[f_down]


    print("Veuillez appuyer sur la touche 'p' afin d'activer la force. La force restera actif tant que vous appuyer sur la touche.")

    #Starting the simulation
    TheFoundation.simulateRealTime(scale=100,background=(30,30,30))

    N = len(P_test.position)
    posY =[]

    for i in range(N) :
        posY.append(P_test.position[i].y)

    figure()
    plot(TheFoundation.time,posY,label="y(t)")
    title("Oscilliation du système masse ressort")
    xlabel("temps[s]")
    ylabel("deplacement Verticale[m]")
    legend()
    grid()
    show()


    sys.exit()
