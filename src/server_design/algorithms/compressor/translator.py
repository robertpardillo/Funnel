
from .compressor import Compressor


def get_graphic(session, args):
    compressor = session.compressor
    row = compressor.stages[0].rows[0]
    session.socket_handler.send({'set_camber': [[row.blade.profiles[i].camber for i in range(len(row.blade.profiles))],
                                                [row.blade.profiles[i].stagger for i in
                                                 range(len(row.blade.profiles))], [row.blade.profiles[i].r for i in
                                                 range(len(row.blade.profiles))]]})


def init_analysis(session, args):

    session.tolerance = 0.05

    compressor = Compressor(args)
    session.compressor = compressor
    compressor.init_design()
    stage = compressor.stages[compressor.current_stage]
    session.checker_list = [False] * len(stage.qns[0].stations)
    row = stage.rows[compressor.current_row]
    #session.socket_model3D.send({'stage':['test', 8]})

    """
    session.socket_handler.send({'set_z':[row.blade.profiles[i].r for i in range(len(row.blade.profiles))]})
    session.socket_handler.send({'set_profile': [row.blade.profiles[-1].X, row.blade.profiles[-1].Y]})
    session.socket_handler.send({'set_camber': [[row.blade.profiles[i].camber for i in range(len(row.blade.profiles))],[row.blade.profiles[i].stagger for i in range(len(row.blade.profiles))]]})
    """
    """
    blade = row.blade
    blade_list = []
    
    for i in blade.profiles:
        blade_list.append({'profile_UP': i.up, 'profile_DOWN': i.down, 'r': i.r})
    blade_list.append('R_1')
    blade_list.append(row.n_blades)
    session.socket_model3D.send({'stage': blade_list})

    """
    profile=row.blade.profiles[compressor.current_profile]
    compressor.current_iteration += 1
    session.socket_CFD.send({'init_analysis': ['R#1', profile.up, profile.down, profile.s, profile.betta_1,
                                               profile.betta_2, profile.W_1[2], profile.W_1[1], profile.W_2[2],
                                               profile.W_2[1], profile.P, profile.T, compressor.current_stage,
                                               compressor.current_row, compressor.current_profile, compressor.current_iteration]})

    """
    data_list={0:[60000, 224.14, 175.87, 470],
               1: [55585, 199, -67.135, 459],
               2: [54041, 205, -128.343, 461],
               3:[46481, 199.3, -221.167, 456.65]}

    for i in range(4):
        compressor.current_profile = i
        qn_outlet = compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[
            compressor.current_profile]
        qn_outlet.W[1] = data_list[i][2]
        qn_outlet.W[2] = data_list[i][3]
        qn_outlet.C[1] = data_list[i][2] + compressor.w * qn_outlet.r
        print()
        qn_outlet.C[2] = data_list[i][3]
        qn_outlet.p = data_list[i][0]
        qn_outlet.T = data_list[i][1]

    profile_before = compressor.stages[compressor.current_stage].rows[compressor.current_row].blade.profiles[compressor.current_profile]
    row.blade.profile_angles()
    print(compressor.current_profile)
    session.flag = True
    new_data(session, {'p': 46481, 'profile':3, 'T':199.3, 'z':456.65, 'Theta': -221.167})
    """


def profile_iteration(session, args):
    compressor = session.compressor
    profile_index = args['profile']
    qn_outlet = compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[profile_index]
    tolerance = session.tolerance
    checker = False

    # Recalculate parameters
    print("Updating profile Data")
    print(qn_outlet.W[1], args["Theta"])
    print(qn_outlet.W[2], args["z"])
    qn_outlet.W[1] = args["Theta"]
    qn_outlet.W[2] = args["z"]
    compressor.stages[compressor.current_stage].flow_angles()
    row = compressor.stages[compressor.current_stage].rows[compressor.current_row]
    profile_before = row.blade.profiles[profile_index]
    row.blade.profile_angles()
    row.blade.build_profiles()
    profile_after = row.blade.profiles[profile_index]
    print('Before',profile_before.camber, profile_before.stagger)
    print('After', profile_after.camber, profile_after.stagger)
    input()

    if abs((profile_before.camber - profile_after.camber) / profile_before.camber) < tolerance and abs((profile_before.stagger - profile_after.stagger) / profile_before.stagger) < tolerance:
        checker = True

    if checker:
        if compressor.current_profile<=compressor.n_streamLines:
            compressor.current_profile+=1
            row=compressor.stages[compressor.current_stage].rows[compressor.current_row]

    else:
        new_profile(session, profile_after)
        """
        print("Updating profile Data")
        qn_outlet.W[1] = args["Theta"]
        qn_outlet.W[2] = args["z"]
        compressor.stages[compressor.current_stage].flow_angles()
        row = compressor.stages[compressor.current_stage].rows[compressor.current_row]
        profile_before = row.blade.profiles[profile_index]
        row.blade.profile_angles()
        row.blade.build_profiles()
        profile_after = row.blade.profiles[profile_index]
        print("Updated profile Data")
        plt.figure()
        plt.plot(profile_before.X, profile_before.Y, 'b')
        plt.plot(profile_after.X, profile_after.Y, 'g')
        plt.title('Profile {}'.format(profile_index))
        plt.axis('equal')
        plt.show()
        new_profile(session,profile_after)
        """

    if False in session.checker_list:
        pass
    else:
        next_row()
    print('Result checked')


def next_row():
    pass


def new_data(session, args):
    """

    :param session:
    :param args: {Theta, z, p, T}
    :return:
    """
    ############# checker results #########
    # Checking angles
    # Recalculate parameters
    compressor = session.compressor
    qn_outlet = compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[compressor.current_profile]
    tolerance = session.tolerance
    checker = False
    print("Updating profile Data: ", "{}_{}_{}_{}".format(compressor.current_stage, compressor.current_row, compressor.current_profile, compressor.current_iteration))


    if compressor.current_row==0:
        qn_outlet.W[1] = args["Theta"]
        qn_outlet.W[2] = args["z"]
        qn_outlet.C[1] = args["Theta"] + compressor.w*qn_outlet.r
        qn_outlet.C[2] = qn_outlet.W[2] = args["z"]
    elif compressor.current_row==1:
        qn_outlet.C[1] = args["Theta"]
        qn_outlet.C[2] = args["z"]
        qn_outlet.W[1] = args["Theta"] - compressor.w * qn_outlet.r
        qn_outlet.W[2] = args["z"]
    #compressor.stages[compressor.current_stage].flow_angles()
    row = compressor.stages[compressor.current_stage].rows[compressor.current_row]
    profile_before = row.blade.profiles[compressor.current_profile]
    """
    row.blade.profile_angles()
    row.blade.build_profiles()
    profile_after = row.blade.profiles[compressor.current_profile]
    print(abs((profile_before.camber - profile_after.camber) / profile_before.camber), abs(
                    (profile_before.stagger - profile_after.stagger) / profile_before.stagger), 'Tolerance')
    
    if abs((profile_before.camber - profile_after.camber) / profile_before.camber) < tolerance and abs(
                    (profile_before.stagger - profile_after.stagger) / profile_before.stagger) < tolerance:
        print(profile_after.camber, 'Camber')
        print(profile_after.stagger, 'Stagger')
        compressor.current_iteration=0
        checker = True
    """
    print(profile_before.camber, 'Camber')
    print(profile_before.stagger, 'Stagger')
    compressor.current_iteration = 0
    checker = True
    #######################################
    if checker:
        if compressor.current_profile == compressor.n_streamLines+1:
            ## change row
            if compressor.current_row==1:
                #compressor.current_row=0
                ## change stage
                if compressor.current_stage==compressor.N-1:
                    #Finish analysis
                    pass
                else:
                    compressor.current_row=0
                    compressor.current_stage+=1
                    compressor.current_profile=0
                    compressor.simulation.init_design()
            else:
                compressor.current_profile=0
                print('Sending to model3D')
                save_blade(session, compressor)
                print('Next row')
                compressor.current_row+=1
                compressor.simulation.stator_init(session)
                new_profile(compressor, session)
        else:
            if compressor.current_row==0:
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[compressor.current_profile].T = args["T"]
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[compressor.current_profile].P = args["p"]
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[compressor.current_profile].W[1] = args["Theta"]
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[compressor.current_profile].W[2] = args["z"]
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[
                    compressor.current_profile].C[1] = args["Theta"]+compressor.w*compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[compressor.current_profile].r
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[
                    compressor.current_profile].C[2] = args["z"]
            elif compressor.current_row == 1:
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[
                    compressor.current_profile].T = args["T"]
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[
                    compressor.current_profile].P = args["p"]
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[
                    compressor.current_profile].C[1] = args["Theta"]
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[
                    compressor.current_profile].C[2] = args["z"]
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[
                    compressor.current_profile].W[1] = args["Theta"] - compressor.w * \
                                                       compressor.stages[compressor.current_stage].rows[
                                                           compressor.current_row].qns[1].stations[
                                                           compressor.current_profile].r
                compressor.stages[compressor.current_stage].rows[compressor.current_row].qns[1].stations[
                    compressor.current_profile].W[2] = args["z"]
            compressor.current_profile+=1
            new_profile(session, None)

    else:
        # Update profile data and recalculate parameters

        new_profile(session, None)

    print("{}_{}_{}_{}".format(compressor.current_stage, compressor.current_row, compressor.current_profile, compressor.current_iteration))


def save_blade(session, compresor):
    row = compresor.stages[compresor.current_stage].rows[compresor.current_row]
    blade = row.blade
    blade_list = []

    for i in blade.profiles:
        blade_list.append({'profile_UP': i.up, 'profile_DOWN': i.down, 'r': i.r})
    blade_list.append('R_1')
    blade_list.append(row.n_blades)
    session.socket_model3D.send({'stage': blade_list})


def new_profile(session, args):
    compressor = session.compressor
    profile = compressor.stages[compressor.current_stage].rows[compressor.current_row].blade.profiles[compressor.current_profile]
    compressor.current_iteration += 1
    if compressor.current_row==0:
        name="R#{}".format(compressor.current_profile)
        vel_inlet_t = profile.W_1[1]
        vel_inlet_z = profile.W_1[2]
        vel_outlet_z = profile.W_2[2]
        vel_outlet_t = profile.W_2[1]
    elif compressor.current_row == 1:
        name = "S#{}".format(compressor.current_profile)
        vel_inlet_t = profile.C_1[1]
        vel_inlet_z = profile.C_1[2]
        vel_outlet_z = profile.C_2[2]
        vel_outlet_t = profile.C_2[1]
    session.socket_CFD.send({'init_analysis': [name, profile.up, profile.down, profile.s, profile.betta_1,
                                               profile.betta_2, vel_inlet_z, vel_inlet_t, vel_outlet_z,
                                               vel_outlet_t, profile.P, profile.T, compressor.current_stage,
                                               compressor.current_row, compressor.current_profile, compressor.current_iteration]})


def update_data(session, args):
    print('new_value')

