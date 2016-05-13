"""
The main process that perform the neural network training process and
predict the final destinations for each testing data.
"""

from classifier import Classifier
import numpy as np
import sys
import random
import ast


def runNeuralNetwork(trainData, testData, testCenter, batchSize, classNum, predFilename, hLayer=None, mode=None, momentumFactor=0.0):
    """
    A function that call the the classifier to train a learning model.
    Args:
        trainData: training examples (numpy)
        testData: testing examples (numpy)
        batchSize: the number of training example for each iteration
        classNum: the number of classes
        hLayer: number of the hidden layer nodes (list)
        mode: weight initializing mode
        momentumFactor: momentum factor
    """
    print ""
    print "Neural Network =============================="
    print " - number of hidden layer nodes:",
    if hLayer is not None:
        print hLayer
    else:
        print " default (one hidden layer with node number = 2 * feature number)"

    print " - weight initialization mode:",
    if mode is not None:
        print mode
    else:
        print "default"

    print " - momentum factor", momentumFactor

    nn = Classifier("neural_network", hidden_layer=hLayer, weightInitMode=mode, momentumFactor=momentumFactor)
    nn.train(trainData, testData, classNum, batchSize)
    nn.test(testData, "test", testCenter, predFilename)


if __name__ == "__main__":
    """
    The data has been shuffled.
    """

    # get clusters
    f = open('../dataset/train/clusters.txt', 'r')
    clusters = [k.strip("\n").split("|") for k in f.readlines()]
    f.close()
    # clusters = [[int(d1), ast.literal_eval(d2)] for d1, d2, d3 in clusters if int(d3) > 1]
    # filterClut = [int(d1) for d1, d2, d3 in clusters]
    # print len(filterClut)


    # read training data
    f = open('../dataset/train/trainData_withLabel.txt', 'r')
    data = [l for l in f.readlines() if l]
    rawData = []
    err = 0
    for d in data:
        if not d:
            continue
        l = d.strip("\n").split("|")
        rawData.append(l)
        if len(rawData) % 10000 == 0:
            print ".",
        if len(rawData) >= 100000:
            break
    f.close()

    print len(rawData)

    # only take items we need
    cols = [i for i in xrange(1, 41)]

    allData = [[float(d[i]) for i in cols] for d in rawData]
    # allData = np.array([[float(d[i]) for i in cols] for d in rawData])
    allData = np.array(allData)


    # allData = allData[:, :-1]

    # feature scaling
    maxLng = maxLat = -sys.maxint
    minLng = minLat = sys.maxint
    for j in [i for i in range(20, 39, 2)]:
        maxLng = max(maxLng, np.amax(allData[:, j]))
        minLng = min(minLng, np.amin(allData[:, j]))
    for j in [i for i in range(21, 40, 2)]:
        maxLat = max(maxLat, np.amax(allData[:, j]))
        minLat = min(minLat, np.amin(allData[:, j]))

    for j in [i for i in xrange(20, 39, 2)]:
        allData[:, j] = (allData[:, j] - minLng) / (maxLng - minLng)
    for j in [i for i in xrange(21, 40, 2)]:
        allData[:, j] = (allData[:, j] - minLat) / (maxLat - minLat)

    # divide data into trainData and testData
    testDataNum = len(rawData) / 10
    testData    = allData[len(allData) - testDataNum:, :]
    trainData   = allData[:len(allData) - testDataNum, :]
    realCenter  = [ast.literal_eval(d[-1]) for d in rawData[len(rawData) - testDataNum:]]
    del allData

    momentumFactor = 0.8
    classNum = len(clusters)

    # node numbers of hidden and output layers
    # the last one is the output layer
    hiddenLayer = [200]
    weightInitMode = "shallow"
    batchSize = 1000
    predFilename = '../dataset/train/result/prediction_300.txt'

    runNeuralNetwork(trainData, testData, realCenter, batchSize, classNum, predFilename, hiddenLayer, weightInitMode, momentumFactor)