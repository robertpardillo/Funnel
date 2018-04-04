
import numpy as np
import matplotlib.pyplot as plt

def lineal_inter(points, x):
    for i in range(len(points)-1):
        if points[i][0]<= x<=points[i+1][0]:
            y = points[i][1] +((points[i+1][1]-points[i][1])*(x-points[i][0])/(points[i+1][0]-points[i][0]))
            return y


def NACA65(camberline_x, camberline_y, camber, chord, tb_c):

    base_airfoil_thickness_distribution = np.matrix([[0, 0],
                                                [0.5, 1.544],
                                                [0.75, 1.864],
                                                [1.25, 2.338],
                                                [2.5, 3.480],
                                                [5.0, 4.354],
                                                [7.5, 5.294],
                                                [10, 6.080],
                                                [15, 7.332],
                                                [20, 8.286],
                                                [25, 9.006],
                                                [30, 9.520],
                                                [35, 9.848],
                                                [40, 9.992],
                                                [45, 9.926],
                                                [50, 9.624],
                                                [55, 9.060],
                                                [60, 8.292],
                                                [65, 7.364],
                                                [70, 6.312],
                                                [75, 5.168],
                                                [80, 3.974],
                                                [85, 2.770],
                                                [90, 1.620],
                                                [95, 0.612],
                                                [100,0]])
    base_airfoil_thickness_distribution[:,:] = base_airfoil_thickness_distribution[:,:]*chord/100
    camberline_x = np.matrix(camberline_x)[:,:]-camberline_x[0]
    camberline_x = camberline_x.tolist()[0]
    camberline_y = np.matrix(camberline_y)[:,:]-camberline_y[0]
    camberline_y = camberline_y.tolist()[0]


    x_up_points = list()
    x_down_points = list()
    y_up_points = list()
    y_down_points = list()
    for i in range(len(camberline_x)-1):
        alfa = np.arctan((camberline_y[i+1] -camberline_y[i])/(camberline_x[i+1] -camberline_x[i]))
        x_up_points.append(camberline_x[i]+lineal_inter(base_airfoil_thickness_distribution.tolist(),camberline_x[i])*np.cos(alfa+np.pi/2))
        y_up_points.append(camberline_y[i]+lineal_inter(base_airfoil_thickness_distribution.tolist(),camberline_x[i])*np.sin(-alfa-3*np.pi/2))

        x_down_points.append(camberline_x[i] + lineal_inter(base_airfoil_thickness_distribution.tolist(),camberline_x[i]) * np.sin(alfa))
        y_down_points.append(camberline_y[i] - lineal_inter(base_airfoil_thickness_distribution.tolist(),camberline_x[i]) * np.cos(alfa))

    X = x_up_points+x_down_points[::-1]
    Y = y_up_points+y_down_points[::-1]

    up = [[i, j] for i,j in zip(x_up_points, y_up_points)]
    down =[[i, j] for i,j in zip(x_down_points, y_down_points)]

    return X, Y, up, down


def DCA(camberline_x, camberline_y, camber, chord, tb_c):

    camber = ((camber * np.pi/180)**2)**0.5
    tb = tb_c * chord
    ro = 0.3 * tb

    ###### Upper surface ###########
    incre_x_u = chord/2-ro*np.cos(camber/2)
    y_0 = np.tan(camber/4)*chord/2
    d = y_0 +tb/2 -ro * np.sin(camber/2)
    Ru = (d**2-ro**2+(chord/2-ro*np.cos(camber/2))**2)/(2*(d-ro))
    incre_y_u = Ru - d

    theta_u = np.arctan2(incre_x_u, incre_y_u)

    upper_points = list()
    x_center = 0
    y_center = y_0+tb/2-Ru

    for i in np.arange(-theta_u, theta_u, 0.001):
        x = x_center + Ru*np.sin(i)
        y = y_center + Ru*np.cos(i)
        upper_points.append([x,y])


    plt.show()
    ###### Lower surface ###########

    d = ro*np.sin(camber/2)-(y_0-tb/2)
    Rl = (-incre_x_u**2-d**2+ro**2)/(2*(d-ro))
    #Rl=(Rl**2)**0.5
    c=chord
    #A=tb**2/4+tb*y_0+tb*ro*np.sin(camber/2)+y_0**2-2*y_0*ro*np.sin(camber/2)+ro**2*np.sin(camber/2)+c**2/4+ro**2*np.cos(camber/2)**2-c*ro*np.cos(camber/2)-ro**2
    #B=2*ro-tb+2*y_0-2*ro*np.sin(camber/2)

    #Rl =(A)/(B)
    incre_y_u = Rl+d

    theta_u = np.arctan2(incre_x_u, incre_y_u)
    lower_points = list()
    x_center = 0
    y_center = y_0-tb/2-Rl
    from_ = -theta_u
    to_ = theta_u
    if Rl<0:
        from_0 = from_+np.pi
        from_ = -(from_+np.pi)
        to_ = from_0


    for i in np.arange(from_, to_, 0.001):
        x = x_center + Rl * np.sin(i)
        y = y_center + Rl * np.cos(i)
        lower_points.append([x, y])

    ## Leading edge

    y_center = ro*np.sin(camber/2)
    x_center = -(chord/2-ro*np.cos(camber/2))

    angle_from = np.arctan2(upper_points[0][1]-y_center, upper_points[0][0]-x_center)
    angle_to = np.arctan2(lower_points[0][1]-y_center, lower_points[0][0]-x_center)+2*np.pi
    if Rl<0:
        angle_to=angle_to-np.pi/2

    lead = list()

    for i in np.arange(angle_from, angle_to, 0.02):
        lead.append([x_center+ro*np.cos(i), y_center+ro*np.sin(i)])

    ## Trailing edge
    """
    y_center = ro * np.sin(camber / 2)
    x_center = +(chord / 2 - ro*np.cos(camber/2) )

    angle_from = np.arctan2(lower_points[-1][1] - y_center, lower_points[-1][0] - x_center)
    angle_to = np.arctan2(upper_points[-1][1] - y_center, upper_points[-1][0] - x_center)

    tra = list()

    for i in np.arange(angle_from, angle_to, 0.02):
        tra.append([x_center+ro*np.cos(i),y_center+ro*np.sin(i)])
    """
    tra = [[-lead[i][0],
             lead[i][1]]for i in range(len(lead))]

    tra = tra[::-1]
    up = [i for i in lead[::-1] if i[1]>=0] + upper_points + [i for i in tra[::-1] if i[1]>=0]
    down = [i for i in tra[::-1] if i[1]<0]+ lower_points[::-1] + [i for i in lead[::-1] if i[1]<0]

    X = [i[0] for i in up] + [i[0] for i in down]
    Y = [i[1] for i in up] + [i[1] for i in down]


    """
    y_0 = chord*np.tan(camber/4)/2

    x_center = -(chord/2-ro*np.cos(camber/2))

    y_center = ro*np.sin(camber/2)

    alpha_u = np.arctan2((camberline_y[1]-camberline_y[0]),(camberline_x[1]-camberline_x[0]))

    x_u = x_center - ro*np.sin(alpha_u)
    x_u = [x_u, -x_u]
    y_u = y_center + ro*np.cos(alpha_u)

    x_l = x_center + ro*np.sin(alpha_u)
    x_l = [x_l, -x_l]
    y_l = y_center - ro*np.cos(alpha_u)

    d = y_0 +tb/2-ro*np.sin(camber/2)
    Ru = (d**2-ro**2+(chord/2-ro*np.cos(camber/2))**2)/(2*(d-ro))
    y_u_center = y_0+tb/2-Ru
    theta_u = np.arctan2(x_u[1], (y_u - y_u_center))
    theta_u = np.arange(-theta_u, theta_u+0.001, 0.001)
    x_u_points = list()
    y_u_points = list()
    for i in theta_u:
        x_u_points.append(Ru*np.sin(i))
        y_u_points.append(y_u_center+Ru*np.cos(i))

    d = y_0-tb/2-ro*np.sin(camber/2)
    Rl = (d**2-ro**2+(chord/2-ro*np.cos(camber/2))**2)/(2*(d+ro))
    y_l_center = y_0-tb/2-Rl
    theta_u = np.arctan2(x_l[1], (y_l - y_l_center))
    theta_u = np.arange(-theta_u, theta_u+0.001, 0.001)
    x_l_points = list()
    y_l_points = list()
    for i in theta_u:
        x_l_points.append(Rl * np.sin(i))
        y_l_points.append(y_l_center + Rl * np.cos(i))

    # trailing edge

    x_tra = list()
    y_tra = list()
    theta_tra = np.arange(-np.pi/2-alpha_u, np.pi/2-alpha_u, 0.001)
    for i in theta_tra:

        x_tra.append(-x_center+ro*np.cos(i))
        y_tra.append(y_center + ro * np.sin(i))

    x_lea = list()
    y_lea = list()
    lea_points = list()
    theta_lea = np.arange(np.pi / 2 + alpha_u, 3*np.pi / 2 + alpha_u,  0.001)
    for i in theta_lea:
        x_lea.append(x_center + ro * np.cos(i))
        y_lea.append(y_center + ro * np.sin(i))
        lea_points.append([x_center + ro * np.cos(i), y_center + ro * np.sin(i)])

    lea_points_1 = sorted(lea_points, key=lambda x: x[0] and x[1] >= 0)
    up = [[j[0], j[1]] for j in lea_points_1[::-1] if j[1]>=0]
    up += [[i,j] for i,j in zip(x_u_points, y_u_points)]
    up += [[i, j] for i, j in zip(x_tra[::-1], y_tra[::-1]) if j>=0]
    down = [[i, j] for i, j in zip(x_tra[::-1], y_tra[::-1]) if j < 0]
    down += [[i, j] for i, j in zip(x_l_points[::-1], y_l_points[::-1])]
    down += [[i[0], i[1]] for i in lea_points_1[::-1] if i[1]<0]

    X = [i[0] for i in up] + [j[0] for j in down]
    Y = [i[1] for i in up] + [j[1] for j in down]
    """

    return X,Y, up, down[::-1]