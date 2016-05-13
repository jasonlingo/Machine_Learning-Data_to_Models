"""
Process the raw data. Convert the variables to the desired variables for the input of the neural network.
"""


import ast
import datetime
import math
import random


MAX_TAXI_STAND_ID = 63.0
PERIOD_LENGTH = 30.0
PERIOD_NUM_HOUR = 60.0 / PERIOD_LENGTH
TOT_PERIOD_NUM = PERIOD_NUM_HOUR * 24.0
PERIOD_BIT = len(bin(int(TOT_PERIOD_NUM))[2:])

def timePeriod(hour, minute):
    bins = bin(int(hour * PERIOD_NUM_HOUR + minute / PERIOD_LENGTH + 1))[2:]
    bits = []

    if len(bins) < PERIOD_BIT:
        bits.extend([0 for _ in range(PERIOD_BIT - len(bins))])
    for b in bins:
        bits.append(b)

    return bits


def convertTrainingData(file, output, gpsNum, trajRatio, maxTaxiBitNum):
    """
    Convert the origin training data to the desired format.
    :param file: filename for original training data
    :param output: filename for converted training data
    :param periodLength: the length of period that used to divide a day time
    :param gpsNum: the number of gps points used in the converted training data
    :param trajRatio: the ratio to
    """
    # read data
    f = open(file, 'r')
    data = f.readlines()
    # data = []
    # for j in range(500):
    #     data.append(f.readline())
    f.close()

    random.shuffle(data)

    out = open(output, 'w')

    rows = []
    cnt = 0
    for d in data:
        rawData = d.split("|")
        row = []

        ##################################
        # columns:
        # 0 : Trip ID
        # 1 : Call type
        # 2 : Origin call
        # 3 : Origin stand
        # 4 : Taxi id
        # 5 : Time stamp
        # 6 : Day type
        # 7 : Missing data
        # 8 : GPS
        ##################################

        # append trip id
        row.append(rawData[0])

        # convert origin call:
        #   if exist: 1
        #   else: 0
        if rawData[2]:
            row.append(1)
        else:
            row.append(-1)

        # convert origin stand
        #   use binary bit to represent taxi stand id
        if rawData[3]:
            bins = bin(int(rawData[3]))[2:]
            if len(bins) < maxTaxiBitNum:
                row.extend([0 for _ in range(maxTaxiBitNum - len(bins))])
            for b in bins:
                row.append(b)
        else:
            row.extend([-1 for _ in range(maxTaxiBitNum)])


        # convert time stamp
        #   1. convert unix time to date time
        #   2. find time period of a day for this record
        #   3. add day type: Mon ~ Thur: 1
        #                    Fri       : 2
        #                    Sat, Sun  : 3
        dateTime = datetime.datetime.fromtimestamp(float(rawData[5]))
        # add time period tag
        row.extend(timePeriod(dateTime.hour, dateTime.minute))
        # add weed day tag
        weekDay = dateTime.isoweekday()
        if 1 <= weekDay <= 4:
            row.extend([1, -1, -1])
        elif weekDay == 5:
            row.extend([-1, 1, -1])
        else:
            row.extend([-1, -1, 1])

        # convert day type
        #   A: 1
        #   B: 2
        #   C: 3
        if rawData[6] == 'A':
            row.extend([1, -1, -1])
        elif rawData[6] == 'B':
            row.extend([-1, 1, -1])
        else:
            row.extend([-1, -1, 1])

        # get first k and last k GPS points
        # 1. make the full trajectory to partial trajectory
        # 2. if the total GPS points is less than k, then repeat the last one point
        coords = ast.literal_eval(rawData[-1])

        # add the destination point
        lastPtr = coords[-1]

        # convert the full trajectory to partial trajectory
        numPtr = max(int(math.floor(len(coords) * trajRatio)), 1)
        coords = coords[:numPtr]

        while len(coords) < gpsNum:
            coords.append(coords[-1])

        # add first gpsNum points
        map(lambda x: row.extend(x), coords[:gpsNum])
        # add last gpsNum points
        map(lambda x: row.extend(x), coords[-1 : -1 - gpsNum : -1])

        # append the last point
        row.append(lastPtr)

        # convert the data into string and append it to rows
        if len(row) == 0:
            print "err:", d
        rows.append("|".join(str(k) for k in row))

        cnt += 1
        if cnt >= 600000:
            break

        # if already collecting many rows, write data to file
        if len(rows) >= 10000:
            print ".",
            out.writelines("\n".join(rows))
            rows = []

    if rows:
        out.writelines("\n".join(rows))

    out.close()


if __name__=="__main__":
    file = "../dataset/train/data_0.txt"
    outputFile = "../dataset/train/trainData.txt"

    f = open('../dataset/train/statistics.txt', 'r')
    data = f.readline()
    f.close()

    maxTaxiStand = int(data.strip("\n").split(" ")[-1])
    maxTaxiBitNum = len(bin(maxTaxiStand)[2:])

    gpsNum = 5
    trajRatio = 0.3
    convertTrainingData(file, outputFile, gpsNum, trajRatio, maxTaxiBitNum)
