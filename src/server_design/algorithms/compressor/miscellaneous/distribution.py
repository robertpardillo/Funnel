
import numpy as np
import scipy.interpolate as inter
from collections import deque
import matplotlib.pyplot as plt


class Spline(object):
    def __init__(self, controls_points,spline_type='not-a-knot'):
        self.x = deque()
        self.y = deque()
        self.spline_type = spline_type
        for i in controls_points:
            self.x.append(i[0])
            self.y.append(i[1])
        self.calc()

    def add_control_point(self, point):
        for i in range(len(self.x)-1):
            if (self.x[i]<=point[0]<=self.x[i+1]) or (self.x[i]>=point[0]>=self.x[i+1]):
                self.x.insert(i+1, point[0])
                self.y.insert(i+1, point[1])
        self.calc()

    def change_point(self, new, index):
        self.x[index] = new[0]
        self.y[index] = new[1]
        self.calc()

    def calc(self):
        self.spline = inter.CubicSpline(self.y, self.x, bc_type=self.spline_type)

    def paint(self, step, *title):
        xs = np.arange(self.x[0], self.x[-1], step)
        return [xs, self.spline(xs)]

    def __call__(self, x):
        return self.spline(x)

class Distribution(object):
    def __init__(self, points):
        self.points = points

    def paint(self):
        X_points = list()
        Y_points = list()
        for i,j in zip(range(len(self.points)),self.points):
            X_points.append(i)
            Y_points.append(j)
        plt.figure()

        plt.scatter(X_points, Y_points)
        plt.show()

    def __getitem__(self, item):
        return self.points[item]