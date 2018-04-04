
from miscellaneous.functions import print as prt, form


def sol553(design_parameters):
    """
            design_parameters = [size, stall margin, cost, off-design]

            Psi_c, phi_c grande :size
            constant swirl : cost and stall
            without focus in off-design characteristics

        :param design_parameters: list()
        :return: distribution of phi, psi, R
        """
    prt('Design governing by this mantras (in oder of importance): \n size, cost, stall margin, off.design', 'blue')
    pass