"""
Perform mean shift to cluster the destination points of the training darta.
"""


import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.cluster import MeanShift, estimate_bandwidth
import ast
from dataLoader import loadLastGPS
from collections import Counter


def loadData(file):
    """
    Load data from trainData format
    :param file: filename of trainData
    :return: a list of data
    """
    f = open(file, 'r')
    data = [l.split("|") for l in f.readlines() if l]
    f.close()

    for d in data:
        d[-1] = ast.literal_eval(d[-1])

    return data


def meanShift(X):
    print "Clustering..."
    # The following bandwidth can be automatically detected using
    bandwidth = estimate_bandwidth(X, quantile=0.005, n_samples=500)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    counts = Counter(labels)

    # output cluster statistics
    print counts
    f = open('../dataset/train/statistics.txt', 'a')
    f.write("\n")
    f.write(str(counts) + "\n")
    f.write("----- clusters that have less than 3 points -----\n")
    for c in counts:
        if counts[c] <= 3:
            f.write(str(c) + ":" + str(counts[c]) + "\n")
    f.close()

    # print "Plotting results..."
    # n_clusters_ = len(ms.cluster_centers_)
    # colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    # for k, col in zip(range(n_clusters_), colors):
    #     my_members = labels == k
    #     cluster_center = cluster_centers[k]
    #     plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    #     plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #              markeredgecolor='k', markersize=2)
    #     # if k > 3:
    #     #     break
    # plt.title('Estimated number of clusters: %d' % n_clusters_)
    # plt.show()

    return labels, cluster_centers, counts


if __name__=="__main__":
    data = loadData("../dataset/train/trainData.txt")

    # clustering
    lastPtrs = [d[-1] for d in data]
    # lastPtrs = filter(lambda x: x[0] < 0, lastPtrs)
    print "origin points:", len(lastPtrs)
    labels, centers, counts = meanShift(np.array(lastPtrs))

    print "final points:", len(labels)

    if len(lastPtrs) != len(labels):
        print "number of data is not consistent"
        exit(0)

    # write cluster center to file
    # filter those clusters that have only one point
    filterClut = [d for d in counts if counts[d] > 1]
    clutMap = {}
    i = 0
    for org in filterClut:
        clutMap[org] = i
        i += 1

    centerTag = []
    for i in xrange(len(centers)):
        if i in filterClut:
            centerTag.append(str(clutMap[i]) + "|" + str(list(centers[i])) + "|" + str(counts[i]) + "\n")

    f = open('../dataset/train/clusters.txt', 'w')
    f.writelines(centerTag)
    f.close()

    # add labels to trainData
    dataWithLabel = []
    for i in xrange(len(labels)):
        if labels[i] in filterClut:
            data[i].insert(1, clutMap[labels[i]])
            dataWithLabel.append(data[i])

    dataWithLabel = map(lambda x: "|".join(str(k) for k in x), dataWithLabel)
    f = open('../dataset/train/trainData_withLabel.txt', 'w')
    f.writelines("\n".join(dataWithLabel))
    f.close()
