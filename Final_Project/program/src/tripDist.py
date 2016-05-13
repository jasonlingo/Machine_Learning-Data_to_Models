"""
Group the trips into three types: short, median, and long trips.
For each trip group, plot every trip's starting point with its color determined by the
error ratio:
    1. blue color: error distance < trip distance * 0.1
    2. green color: trip distance * 0.1 <= error distance < trip distance * 0.5
    3. red color: trip distance * 0.5 <= error distance
    where trip distance is the distance between the start and end points of each trip.
"""

import ast
import numpy as np
import sys
from score import haversine
import os
import pygmaps
import webbrowser


def plotErrMap(trips, title, outputFile):

    SMALL_ERR_COLOR = "#0000FF"  # blue
    MED_ERR_COLOR   = "#00FF00"  # green
    LARGE_ERR_COLOR = "#FF0000"  # red

    # set the center of this map

    center = trips[0][2]
    mymap = pygmaps.maps(center[1], center[0], 10)

    # Add every points in framePoint to this map.
    for dist, errDist, point in trips:

        if errDist < dist * 0.1:
            color = SMALL_ERR_COLOR
            
        elif errDist < dist * 0.5:
            color = MED_ERR_COLOR

        else:
            color = LARGE_ERR_COLOR

        mymap.addpoint(point[1], point[0], color)

    # Create this map.
    mapFilename = outputFile
    mymap.draw('./' + mapFilename)

    # Create the local link to this map file.
    url = "file://" + os.getcwd() + "/" + mapFilename

    # Open this map on a browser
    webbrowser.open_new(url)




if __name__=="__main__":
    # get clusters
    f = open('../dataset/train/clusters.txt', 'r')
    clusters = [k.strip("\n").split("|") for k in f.readlines()]
    f.close()

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

    f = open('../dataset/train/result/dist.txt', 'r')
    dist = [float(l) for l in f.readlines()]
    f.close()


    # divide data into trainData and testData
    testDataNum = len(rawData) / 10
    testData    = rawData[len(rawData) - testDataNum:]
    print len(testData), len(dist)

    shortTrips  = []  # trip dist < 5km
    medianTrips = []  # 5km <= trip dist < 10km
    longTrips   = []  # 10km <= trip dist

    # f = open('../dataset/train/result/erro_ratio.txt', 'w')
    for i in xrange(10000):
        trip = testData[i]
        errDist = dist[i]
        dest = ast.literal_eval(trip[41])

        tripDist =  haversine(float(trip[22]), float(trip[21]), float(dest[1]), float(dest[0]))
        # f.write(str(tripDist) + "|" + str(errDist) + "\n")
        # f.write(str(tripDist) + "\n")

        data = (tripDist, errDist, (float(trip[21]), float(trip[22])))

        if 10 <= tripDist:
            longTrips.append(data)
        elif 5 <= tripDist:
            medianTrips.append(data)
        else:
            shortTrips.append(data)

    # f.close()

    # calculate average distance error
    shortErr  = sum(map(lambda x: x[1], shortTrips)) / len(shortTrips)
    medianErr = sum(map(lambda x: x[1], medianTrips)) / len(medianTrips)
    longErr   = sum(map(lambda x: x[1], longTrips)) / len(longTrips)

    print "avg short err:", shortErr
    print "avg median err:", medianErr
    print "avg long err:", longErr


    outputFile = '../dataset/train/result/small_' + "map.html"
    title = 'Distance Error of Short Trips'
    plotErrMap(shortTrips, title, outputFile)

    outputFile = '../dataset/train/result/med_' + "map.html"
    title = 'Distance Error of Median Trips'
    plotErrMap(medianTrips, title, outputFile)

    outputFile = '../dataset/train/result/large_' + "map.html"
    title = 'Distance Error of Long Trips'
    plotErrMap(longTrips, title, outputFile)
