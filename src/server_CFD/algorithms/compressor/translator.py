
from API.openFoam.case import Case
from API.openFoam.blockMesh_2 import write_block_mesh
import os
import time


def init_analysis(session, args):
    """
    args = [name, profile.up, profile.down, s, betta_1, betta_2, W1_z, W1_Theta, W2_theta, W2_z, p, T, stage, row, profile, n_iteration]
    :param args:
    :return:
    """
    path = os.path.join(session.abs_path,'{}_{}_{}_{}'.format(args[12],args[13],args[14],args[15]))
    session.case = Case(path, session.method)
    case = session.case
    if args[0].split('#')[0]=='R':
        args[7]= -args[7]

    case.file_U.set_field('internalField', 'uniform ({} {} 0)'.format(args[6], args[7]))

    case.file_U.set_field('boundaryField',
                                  {'inlet': {'type': 'freestream',
                                             'freestreamValue': 'uniform ({} {} 0)'.format(args[6], args[7])},
                                   'outlet': {'type': 'zeroGradient'},
                                   'intrados': {'type': 'fixedValue', 'value':'uniform (0 0 0)'},
                                   'extrados': {'type': 'fixedValue', 'value':'uniform (0 0 0)'},
                                   'top_down': {'type': 'empty'},
                                   'cyclic_in_1': {'type': 'cyclic'},
                                   'cyclic_in_2': {'type': 'cyclic'},
                                   'cyclic_out_1': {'type': 'cyclic'},
                                   'cyclic_out_2': {'type': 'cyclic'}})

    case.file_p.set_field('internalField', 'uniform {}'.format(args[10]))
    case.file_p.set_field('boundaryField',
                                  {'inlet': {'type': 'freestreamPressure'},
                                   'outlet': {'type': 'zeroGradient'},
                                   'intrados': {'type': 'zeroGradient'},
                                   'extrados': {'type': 'zeroGradient'},
                                   'top_down': {'type': 'empty'},
                                   'cyclic_in_1': {'type': 'cyclic'},
                                   'cyclic_in_2': {'type': 'cyclic'},
                                   'cyclic_out_1': {'type': 'cyclic'},
                                   'cyclic_out_2': {'type': 'cyclic'}})

    session.case.file_T.set_field('internalField', 'uniform {}'.format(args[11]))
    session.case.file_T.set_field('boundaryField',
                                  {'inlet': {'type': 'fixedValue', 'value': 'uniform {}'.format(args[11])},
                                   'outlet': {'type': 'zeroGradient'},
                                   'intrados': {'type': 'slip'},
                                   'extrados': {'type': 'slip'},
                                   'top_down': {'type': 'empty'},
                                   'cyclic_in_1': {'type': 'cyclic'},
                                   'cyclic_in_2': {'type': 'cyclic'},
                                   'cyclic_out_1': {'type': 'cyclic'},
                                   'cyclic_out_2': {'type': 'cyclic'}})
    """

    session.case.file_U.set_field('internalField', 'uniform ({} {} 0)'.format(args[6], args[7]))
    session.case.file_U.set_field('boundaryField',
                                  {'inlet': {'type': 'fixedValue',
                                             'value': 'uniform ({} {} 0)'.format(args[6], args[7])},
                                   'outlet': {'type': 'inletOutlet','inletValue':'uniform ({} {} 0)'.format(args[6], args[7]),
                                              'value':'uniform ({} {} 0)'.format(args[6], args[7])},
                                   'intrados': {'type': 'noSlip'},
                                   'extrados': {'type': 'noSlip'},
                                   'top_down': {'type': 'empty'},
                                   'cyclic_in_1': {'type': 'cyclic'},
                                   'cyclic_in_2': {'type': 'cyclic'},
                                   'cyclic_out_1': {'type': 'cyclic'},
                                   'cyclic_out_2': {'type': 'cyclic'}})

    session.case.file_p.set_field('internalField', 'uniform {}'.format(args[10]))
    session.case.file_p.set_field('boundaryField',
                                  {'inlet': {'type': 'fixedValue', 'value': 'uniform {}'.format(args[10])},
                                   'outlet': {'type': 'zeroGradient'},
                                   'intrados': {'type': 'zeroGradient'},
                                   'extrados': {'type': 'zeroGradient'},
                                   'top_down': {'type': 'empty'},
                                   'cyclic_in_1': {'type': 'cyclic'},
                                   'cyclic_in_2': {'type': 'cyclic'},
                                   'cyclic_out_1': {'type': 'cyclic'},
                                   'cyclic_out_2': {'type': 'cyclic'}})

    session.case.file_T.set_field('internalField', 'uniform {}'.format(args[11]))
    session.case.file_T.set_field('boundaryField',
                                  {'inlet': {'type': 'fixedValue','value':'uniform {}'.format(args[11])},
                                   'outlet': {'type': 'inletOutlet','inletValue':'uniform {}'.format(args[11]),'value':'uniform {}'.format(args[11])},
                                   'intrados': {'type': 'zeroGradient'},
                                   'extrados': {'type': 'zeroGradient'},
                                   'top_down': {'type': 'empty'},
                                   'cyclic_in_1': {'type': 'cyclic'},
                                   'cyclic_in_2': {'type': 'cyclic'},
                                   'cyclic_out_1': {'type': 'cyclic'},
                                   'cyclic_out_2': {'type': 'cyclic'}})
    """
    """
    session.case.file_U.set_field('internalField', 'uniform ({} {} 0)'.format(args[7], args[6]))
    session.case.file_U.set_field('boundaryField',
                                    {'inlet': {'type': 'fixedValue',
                                               'value': 'uniform ({} {} 0)'.format(args[7], args[6])},
                                     'outlet': {'type': 'zeroGradient'},
                                     'intrados': {'type': 'noSlip'},
                                     'extrados': {'type': 'noSlip'},
                                     'top_down': {'type': 'empty'},
                                     'cyclic_in_1': {'type': 'cyclic'},
                                     'cyclic_in_2': {'type': 'cyclic'},
                                     'cyclic_out_1': {'type': 'cyclic'},
                                     'cyclic_out_2': {'type': 'cyclic'}})

    session.case.file_p.set_field('internalField', 'uniform {}'.format(args[10]))
    session.case.file_p.set_field('boundaryField',
                                    {'inlet': {'type': 'fixedValue', 'value': 'uniform {}'.format(args[10])},
                                     'outlet': {'type': 'zeroGradient'},
                                     'intrados': {'type': 'zeroGradient'},
                                     'extrados': {'type': 'zeroGradient'},
                                     'top_down': {'type': 'empty'},
                                     'cyclic_in_1': {'type': 'cyclic'},
                                     'cyclic_in_2': {'type': 'cyclic'},
                                     'cyclic_out_1': {'type': 'cyclic'},
                                     'cyclic_out_2': {'type': 'cyclic'}})

    session.case.file_T.set_field('internalField', 'uniform {}'.format(args[11]))
    session.case.file_T.set_field('boundaryField',
                                    {'inlet': {'type': 'zeroGradient'},
                                     'outlet': {'type': 'zeroGradient'},
                                     'intrados': {'type': 'zeroGradient'},
                                     'extrados': {'type': 'zeroGradient'},
                                     'top_down': {'type': 'empty'},
                                     'cyclic_in_1': {'type': 'cyclic'},
                                     'cyclic_in_2': {'type': 'cyclic'},
                                     'cyclic_out_1': {'type': 'cyclic'},
                                     'cyclic_out_2': {'type': 'cyclic'}})
    """
    """
    session.case.file_U.set_field('internalField', 'uniform ({} {} 0)'.format(args[5], args[6]))
    session.case.file_U.set_field('boundaryField',
                                    {'inlet': {'type': 'fixedValue', 'value': 'uniform ({} {} 0)'.format(args[5], args[6])},
                                     'outlet': {'type': 'zeroGradient'},
                                     'intrados': {'type': 'noSlip'},
                                     'extrados': {'type': 'noSlip'},
                                     'top_down': {'type': 'empty'},
                                     'cyclic_in_1': {'type': 'cyclic'},
                                     'cyclic_in_2': {'type': 'cyclic'},
                                     'cyclic_out_1': {'type': 'cyclic'},
                                     'cyclic_out_2': {'type': 'cyclic'}})

    session.case.file_p.set_field('boundaryField', {'inlet': {'type': 'fixedValue','value':'uniform {}'.format(args[9])},
                           'outlet': {'type': 'zeroGradient'},
                           'intrados': {'type': 'zeroGradient'},
                           'extrados': {'type': 'zeroGradient'},
                           'top_down': {'type': 'empty'},
                          'cyclic_in_1': {'type': 'cyclic'},
                          'cyclic_in_2': {'type': 'cyclic'},
                          'cyclic_out_1': {'type': 'cyclic'},
                          'cyclic_out_2': {'type': 'cyclic'}})
    session.case.file_p.set_field('internalField', 'uniform {}'.format(args[9]))

    session.case.file_T.set_field('boundaryField', {'inlet': {'type': 'fixedValue', 'value': 'uniform {}'.format(args[10])},
                           'outlet': {'type': 'zeroGradient'},
                           'intrados': {'type': 'zeroGradient'},
                           'extrados': {'type': 'zeroGradient'},
                           'top_down': {'type': 'empty'},
                          'cyclic_in_1': {'type': 'cyclic'},
                          'cyclic_in_2': {'type': 'cyclic'},
                          'cyclic_out_1': {'type': 'cyclic'},
                          'cyclic_out_2': {'type': 'cyclic'}})
    session.case.file_T.set_field('internalField','uniform 300')

    session.case.file_nut.set_field('boundaryField', {'inlet':{'type':'calculated', 'value':'uniform 0'},
                            'outlet':{'type':'calculated', 'value':'uniform 0'},
                           'intrados': {'type': 'nutkWallFunction', 'Cmu':'0.09', 'kappa':'0.41', 'E':'9.8', 'value':'uniform 0'},
                           'extrados': {'type': 'nutkWallFunction', 'Cmu':'0.09', 'kappa':'0.41', 'E':'9.8', 'value':'uniform 0'},
                            'top_down': {'type': 'empty'},
                          'cyclic_in_1': {'type': 'cyclic'},
                          'cyclic_in_2': {'type': 'cyclic'},
                          'cyclic_out_1': {'type': 'cyclic'},
                          'cyclic_out_2': {'type': 'cyclic'}})

    session.case.file_k.set_field('internalField', 'uniform 1')
    session.case.file_k.set_field('boundaryField', {
        'inlet': {'type': 'turbulentIntensityKineticEnergyInlet', 'intensity': '0.05', 'value': 'uniform 1'},
        'outlet': {'type': 'inletOutlet', 'inletValue': 'uniform 1', 'value': 'uniform 1'},
        'intrados': {'type': 'kqRWallFunction','value':'uniform 1'},
        'extrados': {'type': 'kqRWallFunction','value':'uniform 1'},
        'top_down': {'type': 'empty'},
        'cyclic_in_1': {'type': 'cyclic'},
        'cyclic_in_2': {'type': 'cyclic'},
        'cyclic_out_1': {'type': 'cyclic'},
        'cyclic_out_2': {'type': 'cyclic'}})

    session.case.file_epsilon.set_field('boundaryField', {'inlet': {'type': 'turbulentMixingLengthDissipationRateInlet', 'mixingLength': '0.005', 'value': 'uniform 200'},
        'outlet': {'type': 'inletOutlet', 'inletValue': 'uniform 200', 'value': 'uniform 200'},
                           'intrados': {'type': 'epsilonWallFunction', 'Cmu':'0.09', 'kappa':'0.41', 'E':'9.8', 'value':'uniform 200'},
                           'extrados': {'type': 'epsilonWallFunction', 'Cmu':'0.09', 'kappa':'0.41', 'E':'9.8', 'value':'uniform 200'},
                            'top_down': {'type': 'empty'},
                          'cyclic_in_1': {'type': 'cyclic'},
                          'cyclic_in_2': {'type': 'cyclic'},
                          'cyclic_out_1': {'type': 'cyclic'},
                          'cyclic_out_2': {'type': 'cyclic'}})
    session.case.file_epsilon.set_field('internalField', 'uniform 200')

    session.case.file_alphat.set_field('boundaryField', {'inlet':{'type':'calculated', 'value':'uniform 0'},
                            'outlet':{'type':'calculated', 'value':'uniform 0'},
                           'intrados': {'type': 'compressible::alphatWallFunction', 'Prt':'0.85', 'value':'uniform 0'},
                           'extrados': {'type': 'compressible::alphatWallFunction', 'Prt':'0.85', 'value':'uniform 0'},
                            'top_down': {'type': 'empty'},
                          'cyclic_in_1': {'type': 'cyclic'},
                          'cyclic_in_2': {'type': 'cyclic'},
                          'cyclic_out_1': {'type': 'cyclic'},
                          'cyclic_out_2': {'type': 'cyclic'}})
    """
    session.case.file_controlDict.set_field('endTime', '10000')
    session.case.file_controlDict.set_field('startFrom', 'latestTime')
    session.case.file_controlDict.set_field('functions', {"#includeFunc":"MachNo"})
    session.case.file_turbulenceProperties.set_field('simulationType', 'laminar')
    session.case.interacting(100)
    sim = session.case.simulation("open40")  # Build files
    sim.limit_write = 50
    sim.block_mesh(string=write_block_mesh(args[1], args[2], args[3], args[4], args[5], session.mesh))
    sim.check_mesh()

    result_dict={"T": 0, "p":0, "Theta":0, "z":0, "profile":args[14]}

    def _function(container, args):
        current_time = container['current_time']
        if float(current_time)>=0.000015:
            print('Parsing results')
            sim.foamToVTK()
            results = sim.get_last_results('outlet')
            result_U = results.GetCellData('U')
            result_p = results.GetCellData('p')
            result_T = results.GetCellData('T')
            theta = 0.0
            z = 0.0
            p=0.0
            t=0.0
            U_length = len(result_U)
            p_length = len(result_p)
            t_length = len(result_T)
            for i,j,k in zip(result_p, result_T, result_U):
                p+= float(i[0])/p_length
                t+= float(j[0])/t_length
                theta += float(k[1])/U_length
                z += float(k[0])/U_length

            args["T"] = t
            args["p"] = p
            args["Theta"] = theta
            args["z"] = z
            return True
        return False
    
    #sim.run(_function, result_dict)
    #result_dict = {'T': 195.38959999999997, 'z': 429.3120571428572, 'p': 74001.90285714286, 'Theta': -207.19442857142855, 'profile': 0}

    print('Sending results')
    if args[0].split('#')[0]=='R':
        result_dict['Theta']= -result_dict['Theta']

    session.socket_design.send({'new_data':result_dict})


def simulation_params(session, *args):
    """
        args[0] = [method, mesh]
    :param args: 
    :return: 
    """
    session.__setattr__('method', args[0][0])
    session.__setattr__('mesh', args[0][1])