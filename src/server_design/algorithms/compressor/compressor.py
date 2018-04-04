
from .thermodynamic import *
import numpy as np
from scipy.optimize import newton
from .miscellaneous.distribution import Spline
from .miscellaneous.tools import float_f
from .miscellaneous.tools import spin_matrix
import matplotlib.pyplot as plt

from .profileBuild import camberline, profiles


design_stylus = ['size', 'stall margin', 'cost', 'off-design']


class Compressor(object):
    def __init__(self, args):

        self.mach_0 = args[0]  # 0.6
        self.P_0 = args[1] * 1000  # 26437
        self.T_0 = args[2]  # 223.2
        self.mass_flow = args[3]  # 35
        self.PI_c = args[4]  # 6.5
        # design_parameters = [size, stall, cost, off-design]
        self.design_parameters = args[5]  # [1, 0.7, 0.6, 0.5]
        self.n_streamLines = args[6]  # 6

        self.stages = list()
        self.qns = list()

        ## Init Design parameters
        self.init()

        ## Design cycle
        self.current_stage = 0
        self.current_row = 0
        self.current_profile = 0
        self.current_iteration = 0
        self.simulation = Simulation(self)

    def init(self):
        # Estimation of Number of Stages ##############################
        PI_e = 1.3
        self.N = int(np.log(self.PI_c) / np.log(PI_e))
        ##############################################################
        # Build all parts to calculus and to contain variables ###
        for i in range(self.N*2+1):
            self.qns.append(QN(self.n_streamLines))

        for i in range(self.N):
            self.stages.append(Stage(self.qns[2*i], self.qns[2*i+1], self.qns[2*i+2], self))
        ##################################################################
        # Inlet Thermodynamic ############################################

        self.qns[0].set_all_stations('P', self.P_0)
        self.qns[0].set_all_stations('Pt', Pt(self.mach_0, self.P_0, self.T_0))
        self.qns[0].P_c = self.P_0

        self.qns[0].set_all_stations('Tt', Tt(self.mach_0, self.T_0))
        self.qns[0].set_all_stations('T',self.T_0)
        self.qns[0].T_c = self.T_0

        self.qns[0].__setattr__('mass_flow', self.mass_flow)

        C_0 = [0, 0, self.mach_0 * (gamma() * R() * self.T_0) ** 0.5]
        self.qns[0].C_z_c = self.mach_0 * (gamma() * R() * self.T_0) ** 0.5
        self.qns[0].set_all_stations('C', C_0)

        ################################################################
        # Inlet Geometry ###############################################

        # rh_0 = 0.1375  # m
        self.qns[0]._annulus_sizing(True)

        ###############################################################
        # Initiation of perform parameters ############################

        self.maximum_mach_tip = 1.1
        self.rs = self.stages[0].qns[0].stations[-1].r
        self.w = (self.maximum_mach_tip * gamma() * R() * self.T_0 - C_0[0] ** 2) ** 0.5 / self.rs
        rc_0 = self.stages[0].qns[0].rc
        phi_c_0 = self.mach_0*(gamma(self.T_0)*R()*self.T_0)**0.5/(self.w*rc_0)

        design_param = [[self.design_parameters[i], design_stylus[i]] for i in range(len(self.design_parameters))]
        design_param.sort(key=lambda tup: tup[0], reverse=True)
        binary = ''
        for i in design_param:
            if i[1] == design_stylus[0]:
                binary += '1000'
            elif i[1] == design_stylus[1]:
                binary += '100'
            elif i[1] == design_stylus[2]:
                binary += '10'
            elif i[1] == design_stylus[3]:
                binary += '1'
        criterion = int(binary, 2)
        '''
        #Lines to generate solutions files easier
        path_abs = path.abspath('')
        print(path_abs)
        h = open("{}\designSolutions\sol_{}.py".format(path_abs, criterion), "w")
        string = "def sol{}(design_parameters):\n\tpass".format(criterion)
        h.write(string)
        h.close()
        '''
        _temp = __import__('algorithms.compressor.designSolutions.sol_{}'.format(criterion), globals(), locals(),
                           ['sol{}'.format(criterion)])
        self.design_function = _temp.__dict__['sol{}'.format(criterion)]
        self.phi_dist, self.psi_dist, self.R_dist, self.n, self.m = \
            self.design_function(self.design_parameters, float_f(phi_c_0, 4),self.N)

        l=0
        for i, j, k in zip(self.phi_dist, self.psi_dist, self.R_dist):
            self.stages[l].__setattr__('phi_c', i)
            self.stages[l].__setattr__('psi_c', j)
            self.stages[l].__setattr__('R_c', k)
            self.stages[l].__setattr__('n', self.n)
            self.stages[l].__setattr__('m', self.m)
            l += 1

    def update_data(self, new_data):
        pass

    def next_stage(self):
        self.current_stage += 1

    def init_design(self):
        ##########################################################
        # 1. Velocity Triangles of stage (Absolute and Relative) #
        # 2. Flow angles (Absolute and Relative)                 #
        # 3. Set initial chord                                   #
        # 4. Calculate number of blades                          #
        # 5. Profile first row                                   #
        ##########################################################
        stage = self.stages[self.current_stage]
        stage.velocity_triangles()
        stage.flow_angles()
        stage.set_type()
        row = stage.rows[self.current_row]
        row.__setattr__('chord', 0)
        row.chord = 0.04 # m
        row.number_of_blades()
        row.solidity()
        row.blade.profile_angles()
        row.blade.build_profiles()

        """
        self.psi_dist.paint()
        self.phi_dist.paint()
        self.R_dist.paint()
        """
        """
        plt.figure()
        plt.plot([i.r for i in row.qns[0].stations], [i.stagger for i in row.qns[0].stations],'r')
        plt.plot([i.r for i in row.qns[0].stations], [i.C[1] for i in row.qns[0].stations], 'g')
        plt.plot([i.r for i in row.qns[0].stations], [i.C[1] for i in row.qns[1].stations], 'y')

        plt.plot([i.r for i in row.qns[0].stations], [i.camber for i in row.qns[0].stations], 'black')

        plt.show()

        plt.figure()
        plt.plot([i.r for i in row.qns[0].stations], [i.W[1] for i in row.qns[0].stations], 'r')

        plt.plot([i.r for i in row.qns[0].stations], [i.W[1] for i in row.qns[1].stations], 'black')

        plt.show()
        """


class Stage(object):
    def __init__(self, qn1, qn2, qn3, parent):
        self.owner_compressor = parent
        self.qns = [qn1, qn2, qn3]
        self.rows = [Row(i, self.qns[j], self.qns[j+1], self) for j, i in zip([0, 1], ['Rotor', 'Stator'])]
        self.current_row = 0

    def velocity_triangles(self):
        self.qns[0].C_theta_rotor(self.phi_c, self.psi_c, self.R_c, self.n, self.m, self.owner_compressor.w)
        self.qns[1].C_theta_stator(self.phi_c, self.psi_c, self.R_c, self.n, self.m, self.owner_compressor.w, self.qns[0])

        self.qns[0].sizing_qn(self)
        self.qns[1].C_z_rotor([i.C[2] for i in self.qns[0].stations])

        self.qns[0].W_rotor(self.owner_compressor.w)
        self.qns[1].W_stator(self.owner_compressor.w, self.qns[0])

    def set_type(self):
        mach_tip = float_f((self.qns[0].stations[-1].W[1]**2 + self.qns[0].stations[-1].W[2]**2)**0.5/(R()*self.qns[0].stations[-1].T*gamma())**0.5, 3)
        if mach_tip >= 1.0:
            self.blade_type = 'DCA#CA'
        else:
            self.blade_type = 'NACA65#CA'

    def flow_angles(self):
        self.qns[0].flow_angles()
        self.qns[1].flow_angles()


class Row(object):
    def __init__(self, rotor_stator, qn1, qn2, parent):
        self.owner_stage = parent
        self.rotor_stator = rotor_stator
        self.qns = [qn1, qn2]
        self.blade = Blade(rotor_stator, qn1, qn2, self)

    def number_of_blades(self):
        """
            blades calculated imposing solidity_c = 1
        :return:
        """
        self.__setattr__('n_blades', 0)
        self.n_blades = int(2*np.pi*self.qns[0].rc/self.chord)

    def solidity(self):
        """
            Calculation of solidity and s
        :return:
        """
        self.qns[0].__setattr__('chord', 0)
        self.qns[0].chord = self.chord
        self.blade.chord = self.chord
        self.qns[0].solidity(self.n_blades)


class Blade(object):
    def __init__(self, rotor_stator, qn1, qn2, parent):
        self.owner_row = parent
        self.rotor_stator = rotor_stator
        self.qns = [qn1, qn2]
        self.profiles = list()
        self.current_profile = 0

    def profile_angles(self):
        self.tb_c = 0.1  ### assumption
        self.blade_type = self.owner_row.owner_stage.blade_type
        if  self.blade_type.split('#')[0] == 'NACA65':
            K_s_h = 1
        elif self.blade_type.split('#')[0] == 'DCA':
            K_s_h = 0.7
        K_t_i = (10 * self.tb_c) ** (0.28 / (0.1 + self.tb_c ** 0.3))
        K_t_d = 6.25 * self.tb_c + 37.5 * self.tb_c ** 2

        for i,j in zip(self.qns[0].stations, self.qns[1].stations):
            sol = i.solidity
            # Camber angle theta=A/(1-B) from equations chapter 6
            # A
            if self.rotor_stator=="Rotor":
                bet1 = -i.betta_rel*180/np.pi
                bet2 = -j.betta_rel*180/np.pi
            else:
                bet1 = i.betta * 180 / np.pi
                bet2 = j.betta * 180 / np.pi

            d_0 = 0.01*sol*bet1+(0.74*sol**1.9+3*sol)*(bet1/90)**(1.67+1.09*sol)
            i_0 = bet1**(0.914+sol**3/160)/(5+46*np.exp(-2.3*sol))-0.1*sol**3*np.exp((bet1-70)/4)
            A = bet1-bet2 + K_s_h*(K_t_d*d_0-K_t_i*i_0)

            #B
            x=bet1/100
            m=(0.249-0.074*x-0.135*x**2+0.316*x**3)/sol**(0.9625-0.17*x-0.85*x**3)
            n=0.025*sol-0.06-(bet1/90)**(1+1.2*sol)/(1.5+0.43*sol)
            B = m-n

            i.camber = A/(1-B)

            # Stagger=betta1-alpha
            alpha = (3.6*K_s_h*K_t_i+0.3532*i.camber*0.5**0.25)*sol**(0.65-0.002*i.camber)

            i.stagger = bet1-alpha

        """
        j = 0
        for i in self.qns[1].stations:
            sol = self.qns[0].stations[j].solidity
            if self.rotor_stator == 'Rotor':
                bet = ((i.betta_rel*180/np.pi)**2)**0.5
            elif self.rotor_stator == 'Stator':
                bet = i.betta*180/np.pi
            betta2.append(bet)
            d_0 = 0.01 * sol * bet + (0.74 * sol ** 1.9 + 3 * sol) * (bet / 90) ** (1.67 + 1.09 * sol)
            C.append(K_s_h * K_t_d * d_0)
            x = bet / 100
            m_1 = 0.249 + 0.074 * x - 0.132 * x ** 2 + 0.316 * x ** 3  # Circular arc camberline
            b = 0.9625 - 0.17 * x - 0.85 * x ** 3
            D.append(m_1 / sol ** b)
            j += 1
        j = 0
        for i in self.qns[0].stations:
            sol = i.solidity
            if self.rotor_stator == 'Rotor':
                bet = ((i.betta_rel*180/np.pi)**2)**0.5
            elif self.rotor_stator == 'Stator':
                bet = i.betta*180/np.pi
            p = 0.914 + sol ** 3 / 160
            i_0 = bet ** p / (5 + 46 * np.exp(-2.3 * sol)) - 0.1 * sol ** 3 * np.exp((bet - 70) / 4)
            A = K_s_h * K_t_i * i_0
            B = 0.025 * sol - 0.06 - ((bet / 90) ** (1 + 1.2 * sol)) / (1.5 + 0.43 * sol)
            i.camber = (bet - betta2[j] + C[j] - A) / (1 + B - D[j])
            alfa = (3.6 * K_s_h * K_t_i + 0.3532 * i.camber * 0.5 ** 0.25) * sol ** (0.65 - 0.002 * i.camber)
            i.stagger = bet - alfa
            j += 1
        """

    def build_profiles(self):
        self.profiles=[]
        if self.rotor_stator=='Rotor':
            ext = '_rel'
        elif self. rotor_stator=='Stator':
            ext=''
        for i, j in zip(self.qns[0].stations, self.qns[1].stations):
            self.profiles.append(Profiles(self.blade_type, i.camber, i.stagger, i.__getattribute__('betta'+ext), j.__getattribute__('betta'+ext),
                                          i.solidity, self.chord, i.r, i.W, i.C, j.W, j.C, i.P, i.T, self.tb_c))


class Profiles(object):
    def __init__(self, profile_type, camber, stagger, betta_1, betta_2, solidity, chord, r, W_1, C_1, W_2, C_2,P, T, tb_c):
        self.profile_type = profile_type
        self.camber = camber
        self.stagger = stagger
        self.betta_1 = betta_1
        self.betta_2 = betta_2
        self.P = P
        self.T = T
        self.W_1 = W_1
        self.C_1 = C_1
        self.W_2 = W_2
        self.C_2 = C_2
        self.solidity = solidity
        self.chord = chord
        self.s = self.chord/self.solidity
        self.r = r
        self.iteration = 0
        self.tb_c = tb_c
        x_c, y_c = camberline.__dict__['{}'.format(self.profile_type.split('#')[1])](camber, chord)
        self.X, self.Y , self.up, self.down = profiles.__dict__[self.profile_type.split('#')[0]](x_c, y_c, self.camber,chord, self.tb_c)

        self.turn_to_stagger()

    def turn_to_stagger(self):
        CG = [0, 0]

        points_matrix = np.matrix([[ i, j] for i,j in zip(self.X, self.Y)])
        translation_matrix = np.matrix([[ CG[0], CG[1]] for i in range(len(self.X))])
        translated_points = points_matrix - translation_matrix
        spinned_matrix = translated_points * spin_matrix(-self.stagger*np.pi/180)

        new_points = spinned_matrix + translation_matrix
        new_points = new_points.tolist()
        self.X = [i[0] for i in new_points]
        self.Y = [i[1] for i in new_points]

        up_matrix = np.matrix(self.up)

        translation_matrix = np.matrix([[CG[0], CG[1]] for i in range(len(self.up))])
        translated_points = up_matrix - translation_matrix
        spinned_matrix = translated_points * spin_matrix(-self.stagger*np.pi/180)
        new_up =spinned_matrix + translation_matrix
        self.up = new_up.tolist()


        down_matrix = np.matrix(self.down)
        translation_matrix = np.matrix([[CG[0], CG[1]] for i in range(len(self.down))])
        translated_points = down_matrix - translation_matrix
        spinned_matrix = translated_points * spin_matrix(-self.stagger*np.pi/180)
        new_down = spinned_matrix + translation_matrix
        self.down = new_down.tolist()


class QN(object):
    def __init__(self, streamlines):
        self.n_stations = streamlines
        self.stations = [Station() for i in range(streamlines+2)]

    def set_all_stations(self, field, value):
        for i in self.stations:
            if isinstance(value, list):
                i.__setattr__(field, value.copy())
            else:
                i.__setattr__(field, value)

    def _annulus_sizing(self, is_first=False,r_0=0):
        if is_first:
            region_mass_flow = self.mass_flow/(self.n_stations+1)
            r_0 = 0.18 #m
            self.stations[0].__setattr__('r', r_0)
            for i in range(1, len(self.stations)):
                def f(x):
                    return region_mass_flow/np.pi - (x - r_0)*(self.stations[i-1].P/(R()*self.stations[i-1].T))*r_0*self.stations[i-1].C[2] - (x - r_0)*(self.stations[i].P/(R()*self.stations[i].T))*x*self.stations[i].C[2]

                sol1 = newton(f, r_0)
                self.stations[i].__setattr__('r', float_f(sol1, 5))
                r_0 = sol1

        else:
            region_mass_flow = self.mass_flow / (self.n_stations + 1)
            W_z = self.get_distribution('C[2]')
            P_dist = self.get_distribution('p')
            T_dist = self.get_distribution('T')

            r_0 = r_0

            self.stations[-1].__setattr__('r', r_0)
            stations_range = [i for i in range(len(self.stations))][::-1]

            for i in range(len(self.stations)-2,0-1, -1):
                def f(x):
                    f_r_1 = P_dist(x)/(R()*T_dist(x))*(W_z(x)*2*np.pi*x)
                    f_r_0 = P_dist(r_0) / (R() * T_dist(r_0)) * (W_z(r_0) * 2 * np.pi * r_0)
                    return region_mass_flow+(f_r_1+f_r_0)*(x-r_0)/2

                sol1 = newton(f, r_0)
                self.stations[i].__setattr__('r', float_f(sol1, 5))
                r_0 = sol1

        self.rc = ((self.stations[-1].r**2 + self.stations[0].r**2)/2)**0.5

    def C_theta_rotor(self, phi, psi, R, n, m,w):
        for i in self.stations:
            i.C[1] = w*self.rc*((1-R)*(self.rc/i.r)**n-(psi/2)*(self.rc/i.r)**m)
        else:
            self.C_theta_c = w*self.rc*((1-R)*(self.rc/self.rc)**n-(psi/2)*(self.rc/self.rc)**m)

    def C_theta_stator(self, phi, psi, R, n, m, w, qn_before):
        for i, j in zip(self.stations, qn_before.stations):
            i.C[1] = (j.r*j.C[1]+ psi*w*qn_before.rc**2)/j.r
            i.r=j.r
        else:
            self.C_theta_c = (qn_before.rc*qn_before.C_theta_c+psi*w*qn_before.rc**2)/qn_before.rc

    def C_z_rotor(self, new_data):
        for i, j in zip(self.stations, new_data):
            i.C[2] = j

    def C_z(self):
        """
        Must be calculated when C_theta and rc were been calculated
        :return:
        """
        index = 0
        for i in self.stations:
            if i.r<self.rc:
                index+=1

        C_z_0 = self.C_z_c
        C_theta_0 = self.C_theta_c
        r_0 = self.rc
        for i in range(index, len(self.stations)):
            station = self.stations[i]
            A = ((station.C[1]**2/station.r+C_theta_0**2/r_0)*(station.r-r_0))/2
            B = (C_z_0**2)/2-A-(station.C[1]**2)/2+(C_theta_0**2)/2
            C_z_0 = (2*B)**0.5
            C_theta_0 = station.C[1]
            r_0 = station.r
            station.C[2]= C_z_0

        # Down
        C_z_0 = self.C_z_c
        C_theta_0 = self.C_theta_c
        r_0 = self.rc
        for i in range(index-1, -1,-1):
            station2 = self.stations[i]
            A = ((station.C[1]**2/station2.r+C_theta_0**2/r_0)*(station2.r-r_0))/2
            B = C_z_0 ** 2 / 2 - A - station2.C[1] ** 2 / 2 + C_theta_0 ** 2 / 2
            C_z_0 = (2 * B) ** 0.5
            C_theta_0 = station2.C[1]
            r_0 = station2.r
            station2.C[2] = C_z_0

    def W_rotor(self, w):
        for i in self.stations:
            i.__setattr__('W', [0,0,0])
            i.W[0] = i.C[0]
            i.W[1] = +i.C[1]-w*i.r
            i.W[2] = i.C[2]

    def W_stator(self,w, qn_before):
        for i,j in zip(self.stations, qn_before.stations):
            i.__setattr__('W', [0,0,0])
            i.W[0] = i.C[0]
            i.W[1] = i.C[1]-w*j.r
            i.W[2] = i.C[2]

    def flow_angles(self):
        for i in self.stations:
            i.__setattr__('betta', 0)
            i.betta = np.arcsin(i.C[1]/(i.C[2]**2+i.C[1]**2)**0.5)

            i.__setattr__('betta_rel', 0)
            i.betta_rel = np.arcsin(i.W[1]/(i.W[2]**2+i.W[1]**2)**0.5)

    def solidity(self, n_blades):
        for i in self.stations:
            i.solidity = self.chord * n_blades / (2 * np.pi * i.r)
            i.s = self.chord/i.solidity

    def update_thermo(self):
        """
        Update thermodynamic properties, T, P , Tt, Pt of all stations.
        Hypothesis:
            - Entropy constant over radius
            - Enthalpy constant over radius
            - Thermally and calorically perfect gases
        :return:
        """
        h_refe, T_ref = h_ref()
        h = h_refe +cp()*(self.T_c-T_ref)
        H_c = h + 0.5*(self.C_theta_c**2+self.C_z_c**2)
        s_refe, T_ref, P_ref = s_ref()
        S_c = s_refe + cp()*np.log(self.T_c/T_ref)-R()*np.log(self.P_c/P_ref)
        for i in self.stations:
            i.mach = (i.C[1]**2+i.C[2]**2)**0.5/(gamma()*R()*i.T)
            i.T = (H_c-h_refe-0.5*(i.C[1]**2+i.C[2]**2))/cp()+T_ref
            i.T_t = Tt(i.mach,i.T)

            A = (s_refe+cp()*np.log(i.T/T_ref)-S_c)/R()
            i.P = np.exp(A)*P_ref
            i.P_t = Pt(i.mach, i.P, i.T)

    def sizing_qn(self, owner_stage, is_first=True):
        checker=False
        while not checker:
            if is_first:
                self.C_z()
                self.update_thermo()
                rc_0 = self.rc
                self._annulus_sizing(is_first)
                if abs((rc_0-self.rc)/rc_0)<0.01:
                    checker=True

                owner_stage.rs = self.stations[-1].r
                A = (gamma()*R()*self.stations[-1].T*owner_stage.owner_compressor.maximum_mach_tip**2-self.stations[-1].C[2]**2)**0.5
                owner_stage.owner_compressor.w = ( self.stations[-1].C[1]+A)/self.stations[-1].r

                phi_c_0 = owner_stage.owner_compressor.mach_0 * (gamma() * R() * owner_stage.owner_compressor.T_0) ** 0.5 / (owner_stage.owner_compressor.w * self.rc)
                comp = owner_stage.owner_compressor
                comp.phi_dist, comp.psi_dist, comp.R_dist, comp.n, comp.m = \
                    comp.design_function(comp.design_parameters, float_f(phi_c_0, 4), comp.N)
                l = 0
                for i, j, k in zip(comp.phi_dist, comp.psi_dist, comp.R_dist):
                    comp.stages[l].__setattr__('phi_c', i)
                    comp.stages[l].__setattr__('psi_c', j)
                    comp.stages[l].__setattr__('R_c', k)
                    comp.stages[l].__setattr__('n', comp.n)
                    comp.stages[l].__setattr__('m', comp.m)
                    l += 1

                owner_stage.qns[0].C_theta_rotor(owner_stage.phi_c, owner_stage.psi_c, owner_stage.R_c, owner_stage.n,
                                                 owner_stage.m, owner_stage.owner_compressor.w)
                owner_stage.qns[1].C_theta_stator(owner_stage.phi_c, owner_stage.psi_c, owner_stage.R_c, owner_stage.n,
                                                  owner_stage.m, owner_stage.owner_compressor.w, owner_stage.qns[0])
                owner_stage.owner_compressor.rs = self.stations[-1].r
            else:
                self._annulus_sizing(is_first, owner_stage.owner_compressor.rs)

    def get_distribution(self,field):
        x = list()
        for i in self.stations:
            eval("x.append([i.{}, i.{}])".format(field, 'r'))
        spline = Spline(x)
        spline.calc()
        return spline


class Station(object):
    """

        Parameters:
                    -mach
                    -T
                    -Tt
                    -P
                    -Pt
                    -C
                    -W
                    -r
                    -betta
                    -betta_rel
                    -camber
                    -stagger

    """
    def __init__(self):
        self.T = 0
        self.Tt = 0
        self.P = 0
        self.Pt = 0

        self.C = [0,0,0]
        self.W = [0,0,0]

        self.r = 0

        self.betta = 0
        self.betta_rel =0

        self.solidity = 0


class Simulation(object):
    def __init__(self, compressor):
        self.compressor = compressor

    def stator_init(self, session):
        # Establish rc of next stage
        current_stage = self.compressor.stages[self.compressor.current_stage]
        current_row = current_stage.rows[self.compressor.current_row]

        stator_inlet = self.compressor.stages[self.compressor.current_stage].rows[self.compressor.current_row].qns[0]

        stator_inlet.mass_flow = self.compressor.mass_flow

        stator_inlet.sizing_qn(current_stage, False)

        current_row.qns[1].rc = current_stage.qns[0].rc
        for i,k,j in zip(current_stage.qns[2].stations, current_stage.qns[1].stations,current_stage.qns[0].stations):
            i.r = j.r
            k.r = j.r

        stage = self.compressor.stages[self.compressor.current_stage + 1]
        # Velocity triangles #########################
        stage.qns[0].C_theta_rotor(stage.phi_c, stage.psi_c, stage.R_c, stage.n, stage.m, stage.owner_compressor.w)
        stage.qns[1].C_theta_stator(stage.phi_c, stage.psi_c, stage.R_c, stage.n, stage.m, stage.owner_compressor.w,
                                    stage.qns[0])

        stage.qns[0].sizing_qn(stage, False)
        stage.qns[1].C_z_rotor([i.C[2] for i in self.qns[0].stations])

        stage.qns[0].W_rotor(stage.owner_compressor.w)
        stage.qns[1].W_stator(stage.owner_compressor.w, stage.qns[0])

        ##############################################
        stage.flow_angles()
        row = self.compressor.stages[self.compressor.current_stage].rows[self.compressor.current_row]
        row.number_of_blades()
        row.solidity()
        row.blade.profile_angles()
        row.blade.build_profiles()

        """
        for i,j,k in zip(self.compressor.stages[self.compressor.current_stage].rows[self.compressor.current_row].qns[1].stations,
                       self.compressor.stages[self.compressor.current_stage].rows[0].qns[0].stations,
                       self.compressor.stages[self.compressor.current_stage].rows[self.compressor.current_row].qns[
                           0].stations):
            print(j.r)
            i.r = j.r
            k.r = j.r

        stage = self.compressor.stages[self.compressor.current_stage+1]
        stage.velocity_triangles()
        stage.flow_angles()

        self.compressor.stages[self.compressor.current_stage].rows[self.compressor.current_row].qns[0].rc = \
        self.compressor.stages[self.compressor.current_stage].rows[self.compressor.current_row - 1].qns[0].rc

        row = self.compressor.stages[self.compressor.current_stage].rows[1]
        row.__setattr__('chord', 0)
        row.chord = 0.04  # m
        row.number_of_blades()
        row.solidity()
        row.blade.profile_angles()
        row.blade.build_profiles()

        plt.figure()
        plt.plot([i.r for i in row.qns[0].stations],[i.camber for i in row.qns[0].stations],'b')
        plt.plot([i.r for i in row.qns[0].stations], [i.stagger for i in row.qns[0].stations],'r')
        plt.axis('equal')
        plt.show()
        """

    def init_design(self):
        stage = self.compressor.stages[self.compressor.current_stage]
        stage.flow_angles()
        row = self.compressor.stages[self.compressor.current_stage].rows[self.compressor.current_row]
        row.number_of_blades()
        row.solidity()
        row.blade.profile_angles()
        row.blade.build_profiles()




