
from builtins import print as pr
import numpy as np
from matplotlib import pyplot as plt

color_coll = {'white': "\033[37;1m",
              'red': "\033[31;1m",
              'green': "\033[33;1m",
              'blue': "\033[34;1m"}


def print(value, color="default"):
    if color == "default":
        color = 'white'
    pr(color_coll[color.lower()] + str(value) + color_coll['white'])


def float_f(n, decimals):
    string = '{'+'0:.{}f'.format(decimals)+'}'
    return float(string.format(round(n,decimals)))


def spin_matrix(theta):
    return np.matrix([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])


def plot_list(*_list):
    plt.figure()
    for j in _list:
        plt.plot([i[0] for i in j], [i[1] for i in j])
    plt.axis('equal')
    plt.show()
