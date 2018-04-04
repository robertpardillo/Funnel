
from .miscellaneous.tools import print as prt
from .miscellaneous.tools import float_f
import time

def psi_limit(phi, R, Kc):
    """
    De Haller stall limit, Limiting W2/W1>=0.7
    
    :param phi: Distribution object
    :param R: Distribution object
    :return: psi -- points list
    """
    psi_dist = list()
    for i in range(len(phi.points)):
        pseudo_R = 0.5 + abs(R.points[i] - 0.5)
        psi = (6*pseudo_R)/17 + 0.85*(0.5/pseudo_R)**1.18*phi.points[i]**(2+0.1/pseudo_R)
        if psi<=1:
            psi_dist.append(psi*Kc)
        else:
            while True:
                pseudo_R =  0.5 + abs(R.points[i] - 0.5)
                R.points[i] = R.points[i] * 1.05
                psi = (6*pseudo_R)/17 + 0.85*(0.5/pseudo_R)**1.18*phi.points[i]**(2+0.1/pseudo_R)
                try: psi-psi_0
                except: psi_0 = 1
                if psi<=1:
                    psi_dist.append(float_f(psi*Kc, 4))
                    break
                else:
                    time.sleep(0.3)
                    if psi-psi_0>0:
                        phi.points[i] = ((1-6*pseudo_R/17)/(0.85*(0.5/pseudo_R)**1.18))**(1/(2+0.1/pseudo_R))
                    else:
                        psi_0 = psi

                    #prt('Rc up due to Psi_lim >=1', 'red')
                    continue

    return psi_dist


def inlet_angle_flow(phi, psi, R):
    """
    Limiting inlet angle flow, betta1 <= 70º
    
    :param phi: Distribution object
    :param psi: Distribution object
    :param R: Distribution object
    :return: boolean
    """
    for i in range(len(phi.points)):
        if not psi.points[i]/2<=2.75*phi.points[i]-R.points[i]:
            prt('Rc down due to betta>=70º','red')
    else:
        return True