"""
load data from original csv file and shuffle the data and write back to txt file.
"""

import numpy as np
import csv
import sys
import random
import ast


def load_csv(filename, startIdx, endIdx):
    """
    Load the data from csv file and store the data into several smaller
    file. The data will be parsed before being stored.
    Args:
        filename: the input csv file
        startIdx: the starting index of the data to be loaded
        endIdx: the ending index of the data to be loaded
    """
    print "loading data"

    maxTaxiStand = -sys.maxint
    minTaxiStand = sys.maxint

    data = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i = 0
        for row in spamreader:
            i += 1

            if i == 1:  # skip first row that contains column titles
                continue

            # data size limit
            if i < startIdx:
                i += 1
                continue
            if i >= endIdx:
                break

            if i % 5000 == 0:
                print ".",
            if i % 250000 == 0:
                print ""

            rawData = ast.literal_eval(row[0])

            # rawData = row[0].strip('"').rstrip('"').split('","')

            # skip data row that has missing value or has no GPS points
            if 'True' in rawData[7] or '[]' in rawData[8]:
                continue

            if rawData[3]:
                if int(rawData[3]) > maxTaxiStand:
                    maxTaxiStand = int(rawData[3])
                elif int(rawData[3]) < minTaxiStand:
                    minTaxiStand = int(rawData[3])

            data.append(rawData)

    f = open('../dataset/train/statistics.txt', 'w')
    f.write("max taxi stand id: " + str(maxTaxiStand) + "\n")
    f.write("min taxi stand id: " + str(minTaxiStand) + "\n")
    return data

    # return np.array(data)


def writeToFile(filename, data):
    print "Output files..."
    i = 0
    fileIdx = 0

    f = open(filename + str(fileIdx) + ".txt", 'w')
    for d in data:
        i += 1
        f.write("|".join(d))
        f.write("\n")

        if i % sys.maxint == 0:
            f.close()
            fileIdx += 1
            f = open(filename + str(fileIdx) + ".txt", "w")
    f.close()


def loadLastGPS(filename):
    """
    Load GPS point from file and return it as a numpy array.

    :arg
        filename: input file that contains GPS points (one point per line) in the format (latitude, longitude)
    :return numpy array
    """
    f = open(filename, 'r')
    data = [l.strip().split(",") for l in f.readlines()]
    f.close()

    gps = map(lambda x: (float(x[0]), float(x[1])), data)

    return np.array(gps)



if __name__=="__main__":
    filename = '../dataset/train.csv'
    outputFilename = '../dataset/train/data_'

    data = load_csv(filename, 1, sys.maxint)

    random.shuffle(data)
    writeToFile(outputFilename, data)