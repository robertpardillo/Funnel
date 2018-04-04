
from ..miscellaneous.tools import print as prt
from ..miscellaneous.distribution import Distribution
from ..limitPerformParam  import *
from ..miscellaneous.tools import float_f


def sol549(design_parameters, phi_0, N):
    """
        design_parameters = [size, stall margin, cost, off-design]

        Psi_c, phi_c grande :size
        swirl Constant : stall cost
        controlling twist of blades
        without focus in off-design characteristics

    :param design_parameters: list()
    :return: distribution of phi, psi, R
    """
    prt('Design governing by this mantras (in oder of importance): \nsize, stall margin, cost, off-design', 'blue')
    n = 0
    m = 0
    phi_f = phi_0*1.2
    N_lineal_phi = int(0.4 * N)
    step = (phi_f-phi_0)/(N_lineal_phi-1)
    phi_dist = [float_f(phi_0+i*step, 4) for i in range(N_lineal_phi)] + [float_f(phi_f, 4) for i in range(N_lineal_phi, N)]
    phi_dist = Distribution(phi_dist)
    N_lineal_R = int(0.3 * N)
    R_0 = 0.7
    R_f = 0.65
    step = (R_f - R_0) / (N_lineal_R - 1)
    R_dist = [float_f(R_0+i*step, 4) for i in range(N_lineal_R)] + [float_f(R_f, 4) for i in range(N_lineal_R, N)]
    R_dist = Distribution(R_dist)

    Kc = 1-0.5*design_parameters[1]
    psi_dist = Distribution(psi_limit(phi_dist, R_dist, Kc))
    if inlet_angle_flow(phi_dist,psi_dist,R_dist):
        pass

    return phi_dist, psi_dist, R_dist, n,m
