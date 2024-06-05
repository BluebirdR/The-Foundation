# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 09:23:59 2024

@author: UserTP
"""

from Run_particuleM import *
from random import random
from math import sin,cos,pi
from Run_moteurCC import MoteurCC

angle = 60
angle = angle*pi/180

# Creating the universe
espace_temps = Univers(name='Alpha Quadrant',step=0.0005, dimensions=(10,5) )

# Adding particules to the universe
m1 = MoteurCC(pos = Vecteur3D(6,3,1) )
P0 = Particule(p0=Vecteur3D(5+1*sin(angle),3-1*cos(angle),0),v0=Vecteur3D(0,0,0))
P1 = Particule(p0=Vecteur3D(random()*1,random()*0.5,0), \
               v0=Vecteur3D(0,0,0), \
               name='pif',color='green',test=True)
P2 = Particule(p0=Vecteur3D(5,4,0),v0=Vecteur3D(0,0,0),color="orange")
P3 = Particule(p0=Vecteur3D(5+1*sin(angle)-0.4*sin(angle-(40*pi/180)),3-1*cos(angle)-40*cos(angle-(40*pi/180)),0),v0=Vecteur3D(0,0,0),color="green")
P_fix = Particule(p0=Vecteur3D(5,3,0),fix=True,name="fixie",color="white")

P01 = Particule(p0=Vecteur3D(2.5,3,.5),v0=Vecteur3D(0,0,0),color="cyan")
P02 = Particule(p0=Vecteur3D(2.5,3,0),v0=Vecteur3D(0,0,0)) 

# Creating the forces 
f_right = ForceSelect(Vecteur3D(150,0,0),active=False,particules=[P2])
f_down = Gravity(Vecteur3D(0,-2,0),active=True)
f_boing = SpringDamper(k=100,c=1,l0=1,particules=[P_fix,P0])
f_prism = Prismatic(P0,P2,axis=Vecteur3D(1,0,0))
f_link = Link(P0,P2)

# Adding agents and forces to the univers
espace_temps.addAgent(P0,P1,P_fix,P2,P01,P02,P3,m1)
espace_temps.addGenerators(f_down,f_boing,f_prism,f_right)

espace_temps.keyControlled=[f_right]

# Launching the simulation
espace_temps.simulateRealTime(scale=100,background=(30,30,30))