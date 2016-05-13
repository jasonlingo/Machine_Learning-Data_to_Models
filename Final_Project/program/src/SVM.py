"""
Use sklearn's SVM classifier to do the same classification task for the comparison purpose.
"""

from classifier import Classifier
import ast
import numpy as np
from sklearn.svm import SVC
from collections import Counter
import sys


if __name__ == "__main__":

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

    # only take items we need
    cols = [i for i in xrange(1, 41)]

    # shuffle data
    allData = np.array([[float(d[i]) for i in cols] for d in rawData])
    # np.random.shuffle(allData)

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

    print allData[0]

    # divide data into trainData and testData
    testDataNum = len(rawData) / 10
    testData    = allData[len(allData) - testDataNum:, :]
    trainData   = allData[:len(allData) - testDataNum, :]
    realCenter = [ast.literal_eval(d[-1]) for d in rawData[len(rawData) - testDataNum:]]
    del allData

    trainLabel = trainData[:, 0]
    trainData  = trainData[:, 1:]
    testLabel  = testData[:, 0]
    testData   = testData[:, 1:]

    # clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(300, ), random_state=1)
    clf = SVC()
    clf.fit(trainData, trainLabel)


    f = open('../dataset/train/result/prediction_svm_1000.txt', 'w')
    total = 0
    correct = 0
    result = []
    for i in xrange(len(testData)):
        pred = clf.predict(testData[i].reshape(1, 39))[0]

        f.write(str(testLabel[i]) + "|" + str(pred) + "|" + str(realCenter[i]) + "\n")


        result.append(pred)
        total += 1
        if int(testLabel[i]) == pred:
            correct += 1
    f.close()

    print Counter(result)
    print "Testing accuracy:", correct / float(total)
