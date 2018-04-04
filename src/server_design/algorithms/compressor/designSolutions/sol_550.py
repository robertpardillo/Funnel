
from miscellaneous.functions import print as prt, form


def sol550(design_parameters):
    """
        design_parameters = [size, stall margin, cost, off-design]

        Psi_c, phi_c grande :size
        free vortex : stall
        controlling distribution of Psi_c: off_des
        without focus in cost characteristics

    :param design_parameters: list()
    :return: distribution of phi, psi, R
    """
    prt('Design governing by this mantras (in oder of importance): \n size, stall margin, off-design, cost', 'blue')
    pass