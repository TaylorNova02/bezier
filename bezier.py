#!/usr/bin/env python3

import numpy as np
import scipy.special
import argparse
from matplotlib import pyplot as plt

def cords(s):
    try:
        x, y = map(float, s.split(','))
        return x, y
    except:
        raise argparse.ArgumentTypeError("Coordinates must be x,y")
#example ./bezier.py -p 0,0 1,2 2,1 -c -n 1000
parser = argparse.ArgumentParser(description='Plot a Bézier curve.')
parser.add_argument('-p', '--points', dest='cords', nargs='+',help='point to plot, appends to list')
parser.add_argument('-c', '--control_polygon', help='plot control polygon')
parser.add_argument('-n', '--nTimes', type=int, default=1000, help='number of time steps, defaults to 1000')
args = parser.parse_args()

def plot_bezier_curve(points, nTimes=1000, control_polygon=False):
    """
        points should be a list of lists, or numpy array of numpy arrays
        such that len(points) >= 2
        nTimes is the number of time steps, defaults to 1000
        control_polygon is a boolean value, if True, then plot the control
        polygon, if False don't plot it. Defaults to False
    """
    points = np.char.split(points, sep=',')
    nPoints = len(points)
    xPoints = np.array([p[0] for p in points], dtype=float)
    yPoints = np.array([p[-1] for p in points], dtype=float)
    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    if control_polygon:
        plt.plot(xPoints, yPoints, "g:") #plot Control Polygon

    plt.plot(xPoints, yPoints, "ro") #add Control Points to plot

    plt.plot(xvals, yvals, "b-") # plot Bézier Curve
    plt.show()

def bernstein_poly(i, n, t):
    return scipy.special.comb(n, i) * ( t**(n-i) ) * (1 - t)**i

if __name__ == '__main__':
    control_polygon = False
    if args.control_polygon:
        control_polygon = True
    if args.cords:

        points = []
        for point in args.cords:
            points.append(cords(point))

        plot_bezier_curve(np.array(args.cords), control_polygon=args.control_polygon, nTimes=args.nTimes)
