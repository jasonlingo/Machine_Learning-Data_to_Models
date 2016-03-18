#!/usr/bin/python
from __future__ import division
from collections import defaultdict
import argparse

class Node(object):
    """
    A class that represents a variable in a Bayesian network.
    """

    def __init__(self, varName, values, cpt):
        """
        :param varName: the name of this variable
        :param values: a list of possible values of this variable
        """
        self.varName = varName
        self.values = values
        self.parents = defaultdict(list)
        self.children = defaultdict(list)
        self.cpt = cpt

    def __eq__(self, other):
        return self.varName == other.varName

    def getExps(self):
        return [(self.varName, value) for value in self.values]

    # ===== parent related methods =============
    def addParent(self, parent):
        self.parents[parent.varName].append(parent)

    def isParentOf(self, other):
        return self.varName in other.parents

    def hasParent(self):
        return len(self.parents) > 0

    def getParents(self):
        return self.parents.values()

    # ===== child related methods ==============    
    def addChild(self, child):
        self.children[child.varName].append(child)

    def hasChild(self):
        return len(self.children) > 0

    def getChildren(self):
        return self.children.values()


class Trajectory(object):

    def __init__(self, param):
        data = param.split()
        self.trajNum = data[0]
        self.timeStep = list(map(lambda d: tuple(d.split("=")), data[2:])) 

    def printData(self):
        print self.trajNum + "---------------------"
        for data in self.timeStep:
            print data


class ConditionalProbTable(object):
    """ The class that deals with conditional probability table """

    def __init__(self):
        self.cpt = defaultdict(dict)

    def addCPDFromFile(self, cpd):
        """ add cpd from input string of cpd file """
        lhs, rhs, prob = cpd.strip().split()
        lhs = parseQuery(lhs)
        rhs = parseQuery(rhs)
        self.addCPD(lhs, rhs, prob)

    def addCPD(self, lhs, rhs, prob):
        lhs = tuple(sorted(lhs))
        rhs = tuple(sorted(rhs))
        self.cpt[lhs][rhs] = float(prob)

    def getProb(self, lhs, rhs):
        lhs = tuple(sorted(lhs))
        rhs = tuple(sorted(rhs))
        dict1 = self.cpt.get(lhs, None)
        if dict1 is not None:
            return dict1.get(rhs, None)

    def getSubCPT(self, lhs):
        # print "Cond getSubCPT", lhs
        lhs = tuple(sorted(lhs))
        return self.cpt[lhs]

    def printCPT(self):
        for prob in self.cpt:
            for p in self.cpt[prob]:
                print prob, p, self.cpt[prob][p]


class ParameterEstimate(object):

    def __init__(self):
        self.nodes = {}
        self.cpt = ConditionalProbTable()
        self.eventCount = {}
        self.children = {}
        self.parents  = {}
        self.paramValues = {}

        # simplified counting
        self.sChildren    = {}
        self.sParents     = {}
        self.sParamValues = {}
        self.counting = {}
        self.counting = {}
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
            # parentNode = self.nodes[parent]
            # childNode = self.nodes[child]
            # parentNode.addChild(childNode)
            # childNode.addParent(parentNode)

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
            self.nodes[varName] = Node(varName, values, self.cpt)   
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
            combination = []
            for p in parent:
                val = paramValues[p]
                combination = self.genComb(combination, p, val)
            for pkey in combination:
                sortKey = tuple(sorted(pkey))
                for val in paramValues[child]:
                    newkey = tuple(sorted(((child, val),) + sortKey))
                    count[newkey] = 1

        # TODO: generate time sequence
        return count 

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
        print "Start training..."
        f = open(trainData, 'r')

        # get the variables and values and convert them to tuples, ignoring trajectory and time tag
        data = [self.convertExampleToTuple(line.split()[1:]) for line in f.readlines() if line.rstrip()]
        f.close()

        allObserve = set([o for o in self.sParamValues if "Observe" in o])

        # do counting
        for d in data:
            # count action and position
            row, col, action = self.getCoordAction(d)
            if d[0] != 0:
                preRowShare, preColShare, rowShare, colShare = self.computePosDiff(preRow, preCol, row, col, preAct)
                key = tuple(sorted((self.addTimeTag(rowShare, 1), self.addTimeTag(preRowShare, 0), self.addTimeTag(preAct, 0))))
                self.counting[key] += 1
                key = tuple(sorted((self.addTimeTag(colShare, 1), self.addTimeTag(preColShare, 0), self.addTimeTag(preAct, 0))))
                self.counting[key] += 1
            preRow, preCol, preAct = row, col, action

            # count position and observation
            # pos = tuple(sorted((row, col)))
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
        if preAct[1] == "MoveEast":
            if int(col[1]) < int(preCol[1]):
                colDiff = int(col[1]) + (self.maxCol - int(preCol[1])) + 1
            else:
                colDiff = int(col[1]) - int(preCol[1]) + 1
            return (preRow[0], "1"), (preCol[0], "1"), (row[0], "1"), (col[0], str(colDiff))

        elif preAct[1] == "MoveWest":
            if int(col[1]) > int(preCol[1]):
                colDiff = int(preCol[1]) + (self.maxCol - int(col[1])) + 1
            else:
                colDiff = int(preCol[1]) - int(col[1]) + 1
            return (preRow[0], "1"), (preCol[0], "1"), (row[0], "1"), (col[0], str(colDiff))

        elif preAct[1] == "MoveNorth":
            if int(row[1]) < int(preRow[1]):
                rowDiff = int(row[1]) + (self.maxRow - int(preRow[1])) + 1
            else:
                rowDiff = int(row[1]) - int(preRow[1]) + 1
            return (preRow[0], "1"), (preCol[0], "1"), (row[0], str(rowDiff)), (col[0], "1")

        else:
            if int(row[1]) > int(preRow[1]):
                rowDiff = int(preRow[1]) + (self.maxRow - int(row[1])) + 1
            else:
                rowDiff = int(preRow[1]) - int(row[1]) + 1
            return (preRow[0], "1"), (preCol[0], "1"), (row[0], str(rowDiff)), (col[0], "1")

    def addTimeTag(self, tup, time):
        if time == 0:
            return (tup[0] + "_T0", tup[1])
        else:
            return (tup[0] + "_T1", tup[1])

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

    def cumulate(self, key):
        self.eventCount[key] = self.eventCount.get(key, 0) + 1

    def convertExampleToTuple(self, ex):
        """
        convert data to tuple, excluding the time tag
        e.g.
        1 PositionRow_1=5 PositionCol_1=6 Action_1=MoveEast => (1, ("PositionRow, "5"), ("PositionCol", "6"), ("Action", "MoveEast"))
        """
        splitEX = map(lambda e: e.split("="), ex)
        output = [(e[0][:-self.findTimeTagPos(e[0])], e[1]) for e in splitEX[1:]]
        # output.sort()
        output.insert(0, int(splitEX[0][0]))
        return tuple(output)

    def check(self):
        # check network parsing
        num = 0
        for k in self.nodes:
            num += 1
            print k, self.nodes[k].values
        print "total var num:", num

    def outputCPD(self, outputFile):
        totalLine = 0
        f = open(outputFile, 'w')

        denoDP = {}

        print " output CPD --------------------------"
        for child in sorted(self.parents):
            if "Obser" not in child:
                a = 1

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
                    if timeDiff:
                        prePos = [p for p in pkey if "Position" in p[0]][0]
                        action = [p for p in pkey if "Action" in p[0]][0]
                        prePos, curPos = self.decodeActionPos(prePos, (child, val), action)

                        denKey = [(p[0][:-self.findTimeTagPos(p[0])] + "_T0", p[1]) for p in pkey]
                        denKey = tuple(sorted(denKey))
                        countDenKey = [(p[0][:-self.findTimeTagPos(p[0])] + "_T0", p[1]) for p in (action, prePos)]
                        countDenKey = tuple(sorted(countDenKey))

                        # numKey = tuple(sorted(((childWithTime, val),) + denKey))
                        numKey = tuple(sorted(((childWithTime, curPos[1]),) + countDenKey))
                        childCountKey = childWithTime
                    else:
                        denKey = tuple(sorted(self.removeTimeTag(pkey)))
                        countDenKey = denKey
                        numKey = tuple(sorted(((child[:-childTimeTagPos], val),) + denKey))
                        childCountKey = childWithTime[:-childWithTimeTagPos]

                    if (child[:-childTimeTagPos], countDenKey) not in denoDP:
                        denoDP[(child[:-childTimeTagPos], denKey)] = sum([self.counting[(tuple(sorted(((childCountKey, v),) + countDenKey)))] for v in self.sParamValues[child[:-childTimeTagPos]]])

                    deno = denoDP[(child[:-childTimeTagPos], countDenKey)]
                    numer = self.counting[numKey]
                    prob = numer / deno

                    f.write(self.printCPD((child, val), denKey, prob, timeDiff) + "\n")
                    totalLine += 1
                    # print self.printCPD((child, val), denKey, prob, timeDiff)
        f.close()
        print "Total lines:", totalLine

    def decodeActionPos(self, prePos, curPos, action):
        if action[1] in ["MoveEast", "MoveNorth"]:
            if int(curPos[1]) < int(prePos[1]):
                diff = int(curPos[1]) + (self.maxCol - int(prePos[1])) + 1
            else:
                diff = int(curPos[1]) - int(prePos[1]) + 1
            return (prePos[0], "1"), (curPos[0], str(diff))

        elif action[1] in ["MoveWest", "MoveSouth"]:
            if int(curPos[1]) > int(prePos[1]):
                diff = int(prePos[1]) + (self.maxCol - int(curPos[1])) + 1
            else:
                diff = int(prePos[1]) - int(curPos[1]) + 1
            return (prePos[0], "1"), (curPos[0], str(diff))

    def getParentValue(self, child):
        res = []
        for parent in self.parents[child]:
            res.append(parent)

    def printCPD(self, child, parents, prob, timeDiff):
        parentFullName = self.parents[child[0]]

        newParent = []
        if timeDiff:
            timeTag = str(int(child[0][-1]) - 1)
        else:
            timeTag = child[0][-1]
        for parent in parents:
            if timeDiff:
                newParent.append((parent[0][:-self.findTimeTagPos(parent[0])] + timeTag, parent[1]))
            else:
                newParent.append((parent[0] + "_" + timeTag, parent[1]))
        # for parent in parents:
        #     for parentName in parentFullName:
        #         if parent[0] in parentName:
        #             newParent.append((parentName, parent[1]))

        childList = [self.tupleToString(child), " "]
        parentList = list(map(self.tupleToString, newParent))
        parentStr = ",".join(parentList)
        probStr = "%.13e" % prob
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


