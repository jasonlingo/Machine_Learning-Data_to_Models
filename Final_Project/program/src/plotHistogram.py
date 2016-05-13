"""
plot the histogram of distance error of predicted destination.
"""

import ast
from score import haversine
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import math


def calcDist(labels, centers):
    dist = []
    for real, predict, realCenter in labels:
        predCenter = centers[predict]
        dist.append(haversine(realCenter[1], realCenter[0], predCenter[1], predCenter[0]))

    return np.array(dist)


def plotHistogram(labels, centers):
    data = calcDist(labels, centers)
    f = open('../dataset/train/result/dist.txt', 'w')
    for d in data:
        f.write(str(d) + "\n")
    f.close()


    fig, ax = plt.subplots()

    # histogram our data with numpy
    n, bins = np.histogram(data, [i/10.0 for i in xrange(0, int(math.ceil(max(data))), 1)])

    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + n


    # we need a (numrects x numsides x 2) numpy array for the path helper
    # function to build a compound path
    XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

    # get the Path object
    barpath = path.Path.make_compound_path_from_polys(XY)

    # make a patch out of it
    patch = patches.PathPatch(
        barpath, facecolor='blue', edgecolor='gray', alpha=0.8)
    ax.add_patch(patch)

    plt.title("Distance Error Histogram")
    plt.xlabel('Distance Error (km)')
    plt.ylabel('Number of Trips')
    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max())

    plt.show()


if __name__=="__main__":
    # read prediction data
    f = open('../dataset/train/result/prediction_200.txt', 'r')
    labels = [l.strip("\n").split("|") for l in f.readlines() if l and "--" not in l]
    f.close()
    for l in labels:
        l[2] = ast.literal_eval(l[2])

    # read cluster centers into a dictionary
    f = open('../dataset/train/clusters.txt', 'r')
    centers = dict(map(lambda x: (x[0], ast.literal_eval(x[1])),
                       [(l.strip("\n").split("|")[:2]) for l in f.readlines() if l]))
    f.close()

    plotHistogram(labels, centers)






