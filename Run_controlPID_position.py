# -*- coding: utf-8 -*-

from Run_moteurCC import MoteurCC
from pylab import figure,legend,show,plot,grid,title,xlabel,ylabel # type: ignore
from math import pi

class ControlPID_position : 

    def __init__(self, motor, kp = 0, ki = 0, kd = 0) :
        self.motor = motor
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.positionC = 0
        self.voltage = 0

        self.error = 0
        self.sumError = 0
        self.lastError = 0


    def __str__(self):
        """
        Returns:
            string: gives us information about the PID Controler 
        """
        return f"PID Position's Controler  ( P = {self.kp} , I = {self.ki} N.m/A, D = {self.kd} )"
    

    def __repr__(self):
        return str(self)


    def setTarget(self, position):
        # Setting the targeted position
        self.positionC = position


    def getVoltage(self):
        return self.voltage
    

    def calculateVoltage(self,step):
        """
            This function calculate the parameters of the PID controler and then changes the voltage to be applied to the motor 
            for the next iteration

        """
        # Error of between the desired value and the simulated one
        self.error = self.positionC - self.motor.getpositionAng()
        
        # The added error
        self.sumError += self.error

        # The differential error for one step of time
        diffError = self.error - self.lastError

        # Updating the last error
        self.lastError = self.error

        # Parameters of the PID controler
        P = self.kp * self.error
        I = self.ki * self.sumError
        D = self.kd * diffError / step
        commande = P + I + D

        self.voltage = commande


    def simule(self,step=0.1):
        
        self.calculateVoltage(step)

        # Setting the voltage after calculation
        self.motor.setVoltage(self.getVoltage())

        # Simulation of the motor for one step
        self.motor.simule(step)
        


if __name__ == '__main__':
    # Fonctionnement en boucle fermé, en positions
    #
    m_bo = MoteurCC(R=1, Kc=0.1, Ke= 0.01, J=0.01, f= 0.1, L=0.1)
    m_bf = MoteurCC(R=1, Kc=0.1, Ke= 0.01, J=0.01, f= 0.1, L=0.1)
    control = ControlPID_position(m_bf,kp=8,ki=0.01,kd=0.5) #these works very well
    t = 0
    step = 0.01
    temps = [t]
    while t<2 :
        t=t+step
        temps.append(t)
        control.setTarget(pi)
        m_bo.setVoltage(1)
        m_bo.simule(step)
        control.simule(step)

    figure()

    m_bo.plotPos("Bo")
    m_bf.plotPos("Bf")

    title("Control en position en boucle fermée avec un controlleur PI")
    xlabel("temps[s]")
    ylabel("theta[rad]")
    legend()
    grid()
    show()

    ####################################################################################################
    # # Controlleur proportionel Integral
    # # Kp = 1 Ki = 0.0005
    # m_bf00005 = MoteurCC(R=1, Kc=0.1, Ke= 0.01, J=0.01, f= 0.1, L=0.1)
    # control00005 = ControlPID_position(m_bf00005,kp=10,ki=0.0005,kd=0)

    # # Kp = 1 ki = 0.01
    # m_bf001 = MoteurCC(R=1, Kc=0.1, Ke= 0.01, J=0.01, f= 0.1, L=0.1)
    # control001 = ControlPID_position(m_bf001,kp=10,ki=0.01,kd=0)
    
    # # Kp = 1 ki = 0.001
    # m_bf0001 = MoteurCC(R=1, Kc=0.1, Ke= 0.01, J=0.01, f= 0.1, L=0.1)
    # control0001 = ControlPID_position(m_bf0001,kp=10,ki=0.001,kd=0)

    # t = 0
    # step = 0.0001
    # temps = [t]
    # while t<2 :
    #     t=t+step
    #     temps.append(t)

    #     control00005.setTarget(pi)
    #     control0001.setTarget(pi)
    #     control001.setTarget(pi)

    #     control00005.simule(step)
    #     control0001.simule(step)
    #     control001.simule(step)



    # figure()

    # m_bf001.plotPos("k_p = 1, k_i = 0.01")
    # m_bf0001.plotPos("k_p = 1, k_i = 0.001")
    # m_bf00005.plotPos("k_p = 1, k_i = 0.0005")

    # title("Control en position en boucle fermée avec un controlleur PI")
    # xlabel("temps[s]")
    # ylabel("theta[rad]")
    # legend()
    # grid()
    # show()


    ####################################################################################################
    # # Controlleur proportionel pur
    # Kp = 10
    # m_bf10 = MoteurCC(R=1, Kc=0.1, Ke= 0.01, J=0.01, f= 0.1, L=0.1)
    # control10 = ControlPID_position(m_bf10,kp=10,ki=0,kd=0)

    # # Kp = 5
    # m_bf5 = MoteurCC(R=1, Kc=0.1, Ke= 0.01, J=0.01, f= 0.1, L=0.1)
    # control5 = ControlPID_position(m_bf5,kp=5,ki=0,kd=0)
    
    # # Kp = 1
    # m_bf1 = MoteurCC(R=1, Kc=0.1, Ke= 0.01, J=0.01, f= 0.1, L=0.1)
    # control1 = ControlPID_position(m_bf1,kp=1,ki=0,kd=0)


    # t = 0
    # step = 0.01
    # temps = [t]
    # while t<2 :
    #     t=t+step
    #     temps.append(t)
    #     control10.setTarget(pi)
    #     control5.setTarget(pi)
    #     control1.setTarget(pi)

    #     control10.simule(step)
    #     control5.simule(step)
    #     control1.simule(step)

    # figure()
    # m_bf1.plotPos("k_p = 1")
    # m_bf5.plotPos("k_p = 5")
    # m_bf10.plotPos("k_p = 10")

    # title("Control en position en boucle fermée avec un correcteur proportionnel")
    # xlabel("temps[s]")
    # ylabel("Theta[rad]")
    # legend()
    # grid()
    # show()
