#!/usr/bin/python
from __future__ import division
import argparse

class ParameterEstimate(object):

    def __init__(self):
        # self.nodes = {}
        # self.cpt = ConditionalProbTable()
        self.eventCount = {}
        self.children = {}
        self.parents  = {}
        self.paramValues = {}


        self.processCnt = 0
        # simplified counting
        self.sChildren    = {}
        self.sParents     = {}
        self.sParamValues = {}
        self.counting = {}
        self.countingTimeDiff = {}  # for action_T0, Position_T0 -> Position_T1
        self.maxRow = None
        self.maxCol = None

    def parseNetwork(self, network):
        """
        Parse data from network file. The data includes:
        1. number of total variables
        2. values of each variables
        3. relationship between variables

        :param network: (string) the file name of a netowrk data
        """
        f = open(network, 'r')
        data = [line for line in f.readlines() if line.rstrip()]  # skip empty line
        f.close()

        self.numVar = int(data[0].strip())

        # store network relationship
        for d in data[1 + self.numVar:]:
            parent, child = [v.strip() for v in d.split("->")]

            if parent in self.children:
                self.children[parent].append(child)
            else:
                self.children[parent] = [child]

            if child in self.parents:
                self.parents[child].append(parent)
            else:
                self.parents[child] = [parent]

            # simplified 
            parent, child = self.checkTimeTag(parent, child)
            if parent in self.sChildren:
                self.sChildren[parent].add(child)
            else:
                self.sChildren[parent] = set([child])
            
            if child in self.sParents:
                self.sParents[child].add(parent)
            else:
                self.sParents[child] = set([parent])

        print "sParents ----------------------------------"
        for k in sorted(self.sParents.keys()):
            print k, self.sParents[k]

        print "sChildren ----------------------------------"
        for k in sorted(self.sChildren.keys()):
            print k, self.sChildren[k]

        self.sParamValues = dict.fromkeys( set(self.sParents.keys() + self.sChildren.keys()), [] )
        # print "sParamValues ---------------------------------------------------"
        # for k in sorted(self.sParamValues.keys()):
        #     print k, self.sParamValues[k]

        # store nodes' names and values
        for d in data[1 : 1 + self.numVar]:
            varName, values = d.strip().split()
            values = values.strip().split(",") 
            self.paramValues[varName] = values
            
            # simplified
            varNames = self.findOrgVarName(varName)
            for varN in varNames:
                self.sParamValues[varN] = values

        self.maxRow = int(max([int(x) for x in self.paramValues["PositionRow_0"]]))
        self.maxCol = int(max([int(x) for x in self.paramValues["PositionCol_0"]]))

        self.counting = self.genCountingDict(self.sParamValues, self.sParents)
        for k in sorted(self.counting.keys()):
            print k, self.counting[k]

    def genCountingDict(self, paramValues, parents):
        print "genCountingDict --------"
        count = {}

        for child in parents:
            parent = parents[child]
            checkPos = False
            if "Position" in child:
                checkPos = True

            combination = []
            for p in parent:
                val = paramValues[p]
                combination = self.genComb(combination, p, val)

            for pkey in combination:
                for p in pkey:
                    if "Position" in p[0]:
                        pos0 = p
                    if "Action" in p[0]:
                        action = p

                for val in paramValues[child]:
                    if not checkPos or (checkPos and self.isValidMove((child, val), pos0, action)):
                        newkey = tuple(sorted(((child, val),) + pkey))
                        count[newkey] = 1

        # TODO: generate time sequence
        return count

    def isValidMove(self, pos1, pos0, action):
        move = action[1]
        if move == "MoveEast":
            if "Col" in pos1[0]:
                return (0 <= int(pos1[1]) - int(pos0[1]) <= 1) or (int(pos0[1]) - int(pos1[1]) + 1 == self.maxCol)
            if "Row" in pos1[0]:
                return pos1[1] == pos0[1]
        elif move == "MoveWest":
            if "Col" in pos1[0]:
                return (0 <= int(pos0[1]) - int(pos1[1]) <= 1) or (int(pos1[1]) - int(pos0[1]) + 1 == self.maxCol)
            if "Row" in pos1[0]:
                return pos1[1] == pos0[1]
        elif move == "MoveNorth":
            if "Col" in pos1[0]:
                return pos1[1] == pos0[1]
            if "Row" in pos1[0]:
                return (0 <= int(pos1[1]) - int(pos0[1]) <= 1) or (int(pos0[1]) - int(pos1[1]) + 1 == self.maxRow)
        else:
            if "Col" in pos1[0]:
                return pos1[1] == pos0[1]
            if "Row" in pos1[0]:
                return (0 <= int(pos0[1]) - int(pos1[1]) <= 1) or (int(pos1[1]) - int(pos0[1]) + 1 == self.maxRow)


    def genComb(self, combination, p, val):
        res = []
        if combination:
            for v in val:
                for c in combination:
                    res.append((c, (p, v)))
        else:
            for v in val:
                res.append((p, v))
        return res

    def findOrgVarName(self, varName):
        varTimeTagPos = self.findTimeTagPos(varName)
        return [k for k in self.sParamValues if varName[:-varTimeTagPos] in k]

    def findTimeTagPos(self, varName):
        for i in xrange(1, len(varName)):
            if varName[-i] == "_":
                return i

    def checkTimeTag(self, parent, child):
        pTimeTagPos = self.findTimeTagPos(parent)
        cTimeTagPos = self.findTimeTagPos(child)
        if parent[-pTimeTagPos:] == child[-cTimeTagPos:]:
            return parent[:-pTimeTagPos], child[:-cTimeTagPos]
        else:
            return parent[:-pTimeTagPos] + "_T0", child[:-cTimeTagPos] + "_T1"

    def train(self, trainData):
        print "Start training"
        f = open(trainData, 'r')

        # get the variables and values and convert them to tuples, ignoring trajectory and time tag
        data = [self.convertExampleToTuple(line.split()[1:]) for line in f.readlines() if line.rstrip()]
        f.close()

        allObserve = set([o for o in self.sParamValues if "Observe" in o])

        # do the counting
        for d in data:
            self.printProcess()

            # count action and position
            row, col, action = self.getCoordAction(d)
            if d[0] != 0:
                preRowShare, preColShare, rowShare, colShare = self.computePosDiff(preRow, preCol, row, col, preAct)
                # if self.isValidMove(rowShare, preRowShare, preAct):  # training data will not have invalid move, no need to check
                key = tuple(sorted((self.addTimeTag(rowShare, 1), self.addTimeTag(preRowShare, 0), self.addTimeTag(preAct, 0))))
                self.counting[key] += 1
                # if self.isValidMove(colShare, preColShare, preAct):
                key = tuple(sorted((self.addTimeTag(colShare, 1), self.addTimeTag(preColShare, 0), self.addTimeTag(preAct, 0))))
                self.counting[key] += 1
            preRow, preCol, preAct = row, col, action

            # count position and observation
            observed = set([u[0] for u in d[1:] if "Observe" in u[0]])
            nonObserved = allObserve - observed
            for v in observed:
                # key = tuple(sorted(((v, "Yes"),) + pos))
                key = tuple(sorted(((v, "Yes"), row, col)))
                self.counting[key] += 1
            for v in nonObserved:
                # key = tuple(sorted(((v, "No"),) + pos))
                key = tuple(sorted(((v, "No"), row, col)))
                self.counting[key] += 1


        for k in sorted(self.counting):
            print k, self.counting[k]

    def computePosDiff(self, preRow, preCol, row, col, preAct):
        """ compute how many steps between tow position """

        if preAct[1] == "MoveEast":
            if int(col[1]) < int(preCol[1]):  # go around
                colDiff = int(col[1]) + (self.maxCol - int(preCol[1]))
            else:
                colDiff = int(col[1]) - int(preCol[1])
            return (preRow[0], "1"), (preCol[0], "1"), (row[0], "1"), (col[0], str(1 + colDiff))
        elif preAct[1] == "MoveWest":
            if int(col[1]) > int(preCol[1]):  # go around
                colDiff = int(preCol[1]) + (self.maxCol - int(col[1]))
            else:
                colDiff = int(preCol[1]) - int(col[1])
            return (preRow[0], "1"), (preCol[0], str(self.maxCol)), (row[0], "1"), (col[0], str(self.maxCol - colDiff))
        elif preAct[1] == "MoveNorth":
            if int(row[1]) < int(preRow[1]):  # go around
                rowDiff = int(row[1]) + (self.maxRow - int(preRow[1]))
            else:
                rowDiff = int(row[1]) - int(preRow[1])
            return (preRow[0], "1"), (preCol[0], "1"), (row[0], str(1 + rowDiff)), (col[0], "1")
        else:
            if int(row[1]) > int(preRow[1]):
                rowDiff = int(preRow[1]) + (self.maxRow - int(row[1]))
            else:
                rowDiff = int(preRow[1]) - int(row[1])
            return (preRow[0], str(self.maxRow)), (preCol[0], "1"), (row[0], str(self.maxRow - rowDiff)), (col[0], "1")

    def addTimeTag(self, tup, time):
        # if time == 0:
            return (tup[0] + "_T" + str(time), tup[1])
        # else:
            # return (tup[0] + "_T1", tup[1])

    def getCoordAction(self, data):
        row, col, action = None, None, None
        for d in data[1:]:
            if 'Row' in d[0]:
                row = d
            if 'Col' in d[0]:
                col = d
            if 'Action' in d[0]:
                action = d
        return row, col, action

    def convertExampleToTuple(self, ex):
        """
        convert data to tuple, excluding the time tag
        e.g.
        1 PositionRow_1=5 PositionCol_1=6 Action_1=MoveEast => (1, ("PositionRow, "5"), ("PositionCol", "6"), ("Action", "MoveEast"))
        """
        splitEX = map(lambda e: e.split("="), ex)
        output = [(e[0][:-self.findTimeTagPos(e[0])], e[1]) for e in splitEX[1:]]
        output.insert(0, int(splitEX[0][0]))
        return tuple(output)

    def outputCPD(self, outputFile):
        outputLines = []

        denoDP = {}

        print " output CPD",
        for child in sorted(self.parents):
            childTimeTagPos = self.findTimeTagPos(child)
            childWithTime, parentWithTime, timeDiff = self.checkTime(child, self.parents[child])
            childWithTimeTagPos = self.findTimeTagPos(childWithTime)
            parent = self.parents[child]
            combination = []
            for p in parent:
                val = self.paramValues[p]
                combination = self.genComb(combination, p, val)

            for pkey in combination:
                for val in self.paramValues[child]:
                    self.printProcess()

                    if timeDiff:
                        for p in pkey:
                            if "Action" in p[0]:
                                action = p
                            elif "Position" in p[0]:
                                prePos = p
                        # prePos = [p for p in pkey if "Position" in p[0]][0]
                        # action = [p for p in pkey if "Action" in p[0]][0]
                        if not self.isValidMove((child, val), prePos, action):
                            continue
                        prePos, curPos = self.decodeActionPos(prePos, (child, val), action)

                        denKey = [(p[0][:-self.findTimeTagPos(p[0])] + "_T0", p[1]) for p in pkey]
                        denKey = tuple(sorted(denKey))

                        countDenKey = [(p[0][:-self.findTimeTagPos(p[0])] + "_T0", p[1]) for p in (action, prePos)]
                        countDenKey = tuple(sorted(countDenKey))

                        numKey = tuple(sorted(((childWithTime, curPos[1]),) + countDenKey))  # TODO:check
                        # if numKey == (('Action_T0', 'MoveWest'), ('PositionCol_T0', '1'), ('PositionCol_T1', '2')):
                        #     a = 1
                        childCountKey = childWithTime
                    else:
                        denKey = tuple(sorted(self.removeTimeTag(pkey)))
                        countDenKey = denKey
                        numKey = tuple(sorted(((child[:-childTimeTagPos], val),) + denKey))
                        childCountKey = childWithTime[:-childWithTimeTagPos]

                    if (child[:-childTimeTagPos], countDenKey) not in denoDP:
                        denoDP[(child[:-childTimeTagPos], countDenKey)] = sum([self.counting.get((tuple(sorted(((childCountKey, v),) + countDenKey))), 0) for v in self.sParamValues[child[:-childTimeTagPos]]])

                    deno = denoDP[(child[:-childTimeTagPos], countDenKey)]
                    numer = self.counting[numKey]  # TODO: check
                    prob = numer / deno

                    outputLines.append(self.printCPD((child, val), denKey, prob, timeDiff) + "\n")
        f = open(outputFile, 'w')
        f.writelines(outputLines)
        f.close()
        print ""
        print "Total lines:", len(outputLines)

    def decodeActionPos(self, prePos, curPos, action):
        if action[1] == "MoveEast":
            if int(curPos[1]) < int(prePos[1]):  # go around
                diff = int(curPos[1]) + (self.maxCol - int(prePos[1]))
            else:
                diff = int(curPos[1]) - int(prePos[1])
            return (prePos[0], "1"), (curPos[0], str(1 + diff))
        elif action[1] == "MoveNorth":
            if int(curPos[1]) < int(prePos[1]):  # go around
                diff = int(curPos[1]) + (self.maxRow - int(prePos[1]))
            else:
                diff = int(curPos[1]) - int(prePos[1])
            return (prePos[0], "1"), (curPos[0], str(1 + diff))
        elif action[1] == "MoveWest":
            if int(curPos[1]) > int(prePos[1]):  # go around
                diff = int(prePos[1]) + (self.maxCol - int(curPos[1]))
            else:
                diff = int(prePos[1]) - int(curPos[1])
            return (prePos[0], str(self.maxCol)), (curPos[0], str(self.maxCol - diff))
        elif action[1] == "MoveSouth":
            if int(curPos[1]) > int(prePos[1]):  # go around
                diff = int(prePos[1]) + (self.maxRow - int(curPos[1]))
            else:
                diff = int(prePos[1]) - int(curPos[1])
            return (prePos[0], str(self.maxRow)), (curPos[0], str(self.maxRow - diff))

    def getParentValue(self, child):
        res = []
        for parent in self.parents[child]:
            res.append(parent)

    def printCPD(self, child, parents, prob, timeDiff):
        parentFullName = self.parents[child[0]]

        childTimeTagPos = self.findTimeTagPos(child[0])

        newParent = []
        if timeDiff:
            timeTag = "_" + str(int(child[0][-(childTimeTagPos-1):]) - 1)
        else:
            timeTag = child[0][-childTimeTagPos:]
        for parent in parents:
            if timeDiff:
                newParent.append((parent[0][:-self.findTimeTagPos(parent[0])] + timeTag, parent[1]))
            else:
                newParent.append((parent[0] + timeTag, parent[1]))
        # for parent in parents:
        #     for parentName in parentFullName:
        #         if parent[0] in parentName:
        #             newParent.append((parentName, parent[1]))

        childList = [self.tupleToString(child), " "]
        parentList = list(map(self.tupleToString, newParent))
        parentStr = ",".join(sorted(parentList, reverse=True))
        # probStr = "%.13e" % prob
        probStr = str(prob)
        return "".join(childList) + parentStr + " " + probStr

    def tupleToString(self, tup):
        return tup[0] + "=" + tup[1]

    def removeTimeTag(self, tup):
        return tuple([(t[0][:-self.findTimeTagPos(t[0])], t[1]) for t in tup])

    def seperateParent(self, pkey):
        result = []
        for p in pkey:
            result.append(self.tupToExp(p))
        return ",".join(result)

    def tupToExp(self, tup):
        return tup[0] + "=" + tup[1]

    def checkTime(self, child, parents):
        newParent = []
        timeDiff = False
        childTimeTagPos = self.findTimeTagPos(child)
        for parent in parents:
            if parent[-self.findTimeTagPos(parent):] != child[-childTimeTagPos:]:
                newParent.append(parent[:-self.findTimeTagPos(parent)] + "_T0")
                timeDiff = True
            else:
                newParent.append(parent[:-self.findTimeTagPos(parent)] + "_T1")
        if timeDiff:
            return child[:-childTimeTagPos] + "_T1", newParent, timeDiff
        else:
            return child, parents, timeDiff

    def printProcess(self):
        self.processCnt += 1
        if self.processCnt % 2000 == 0:
            print ".",
        if self.processCnt > 100000:
            print ""
            self.processCnt = 0

if __name__=="__main__":
    # Get the arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('network', help='network structure file')
    parser.add_argument('trainData', help='training examples')
    parser.add_argument('output', type=str, help="output file")

    args = parser.parse_args()
    network = args.network
    trainData = args.trainData
    output = args.output

    # create a parameter estimate object and parse the network structure file
    pe = ParameterEstimate()
    pe.parseNetwork(network) 
    pe.train(trainData)
    pe.outputCPD(output)


