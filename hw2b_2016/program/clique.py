import argparse

def removeTimeTage(varName):
    return varName[:-findTimeTagPos(varName)]

def findTimeTagPos(varName):
    for i in xrange(1, len(varName)):
        if varName[-i] == "_":
            return i

def printClique(network, output):
    f = open(network, 'r')
    data = [line.split()[0] for line in f.readlines() if line.rstrip()]
    f.close()

    timeNum = int(network.split("-")[-1].split(".")[0][1:])
    varNum = int(data[0])
    data = map(removeTimeTage, data[1:1+varNum])

    landmark = set([d for d in data if "Landmark" in d])
    landmarkNum = len(landmark) / 4

    result = []  # for cluster
    result2 = [] # for edges

    preAction2 = None
    for i in xrange(timeNum):
        if i < timeNum - 1:
            action1 = "Action_%d,PositionRow_%d,PositionCol_%d,PositionRow_%d\n" % (i, i, i, i+1)
            action2 = "Action_%d,PositionCol_%d,PositionRow_%d,PositionCol_%d\n" % (i, i, i+1, i+1)
            result.append(action1)
            result.append(action2)

            if preAction2:
                result2.append(preAction2.strip("\n") + " -- " + action1)
            preAction2 = action2
            action1 = action1.strip("\n")
            result2.append(action1 + " -- " + action2)
            for dir in ["N", "S", "E", "W"]:
                result2.append(action1 + " -- " + "ObserveWall_%s_%d,PositionRow_%d,PositionCol_%d\n" % (dir, i, i, i))
                for n in xrange(1, landmarkNum+1):
                    result2.append(action1 + " -- " + "ObserveLandmark%d_%s_%d,PositionRow_%d,PositionCol_%d\n" % (n, dir, i, i, i))

        for dir in ["N", "S", "E", "W"]:
            result.append("ObserveWall_%s_%d,PositionRow_%d,PositionCol_%d\n" % (dir, i, i, i))
            for n in xrange(1, landmarkNum+1):
                result.append("ObserveLandmark%d_%s_%d,PositionRow_%d,PositionCol_%d\n" % (n, dir, i, i, i))

    result.append("Action_%d\n" % (timeNum - 1))  # append the action for last time tag
    result.insert(0, "%d\n" % (len(result)))

    # the last part of edges for clique tree
    lastAction2 = "Action_%d,PositionCol_%d,PositionRow_%d,PositionCol_%d" % (timeNum - 2, timeNum - 2, timeNum - 1, timeNum - 1 )
    for dir in ["N", "S", "E", "W"]:
        result2.append(lastAction2 + " -- ObserveWall_%s_%d,PositionRow_%d,PositionCol_%d\n" % (dir, timeNum - 1, timeNum - 1, timeNum - 1))
        for n in xrange(1, landmarkNum + 1):
            result2.append(lastAction2 + " -- ObserveLandmark%d_%s_%d,PositionRow_%d,PositionCol_%d\n" % (n, dir, timeNum - 1, timeNum - 1, timeNum - 1))

    # output result to file
    outputFile = open(output, 'w')
    outputFile.writelines(result)
    outputFile.writelines(result2)
    outputFile.close()


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('network', type=str, help="original network")
    parser.add_argument('output', type=str, help='output file')

    args    = parser.parse_args()
    network = args.network
    output  = args.output

    if not network or not output:
        print "Please check network and output file addresses!"

    printClique(network, output)
