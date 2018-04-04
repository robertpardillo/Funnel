
import numpy as np
from matplotlib import pyplot as plt


def CA(camber, chord):

    camber = camber*np.pi/180
    Rc = (chord/2)/np.sin(camber/2)
    step = 0.001
    x_points = np.arange(-(chord/2), 0, step).tolist()
    x_points += np.arange(0, chord/2+step,  step).tolist()
    y_points = [-Rc*np.cos(camber/2)+(Rc**2-i**2)**0.5 for i in x_points]

    return x_points, y_points


def NACA65_camber(camber, chord):
    camber = camber*np.pi/180
    cl_0 = np.tan(camber/4)/0.1103
    base_camberline = np.matrix([[0, 0],
                                 [0.5, 0.250],
                                 [0.75, 0.325],
                                 [1.25, 0.535],
                                 [2.5, 0.930],
                                 [5.0, 1.580],
                                 [7.5, 2.120],
                                 [10, 2.585],
                                 [15, 3.365],
                                 [20, 3.980],
                                 [25, 4.475],
                                 [30, 4.860],
                                 [35, 5.150],
                                 [40, 5.355],
                                 [45, 5.475],
                                 [50, 5.515],
                                 [55, 5.475],
                                 [60, 5.355],
                                 [65, 5.150],
                                 [70, 4.860],
                                 [75, 4.475],
                                 [80, 3.980],
                                 [85, 3.365],
                                 [90, 2.585],
                                 [95, 1.580],
                                 [100, 0]])

    camberline_points_x = base_camberline[:,0] * chord / 100
    camberline_points_y = base_camberline[:,1] * cl_0 *chord/100
    camberline_points_x = [camberline_points_x[j,0] for j in range(len(camberline_points_x))]
    camberline_points_y = [camberline_points_y[j, 0] for j in range(len(camberline_points_y))]

    return camberline_points_x, camberline_points_y
