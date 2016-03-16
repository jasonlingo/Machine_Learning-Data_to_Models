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
        self.topologicalOrder = None

        # simplified counting
        self.sChildren    = {}
        self.sParents     = {}
        self.sParamValues = {}
        self.sTopologicalOrder = None
        self.counting = {}
        self.counting = {}

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
            # print parent, child
            if parent in self.sChildren:
                self.sChildren[parent].add(child)
            else:
                self.sChildren[parent] = set([child])
            
            if child in self.sParents:
                self.sParents[child].add(parent)
            else:
                self.sParents[child] = set([parent])

        # print "----- sParents -----"
        # for k in self.sParents:
        #     print k, self.sParents[k]
        # print ""
        # print "----- sChildren -----"
        # for k in self.sChildren:
        #     print k, self.sChildren[k]

        print "sParents ----------------------------------"
        for k in sorted(self.sParents.keys()):
            print k, self.sParents[k]

        print "sChildren ----------------------------------"
        for k in sorted(self.sChildren.keys()):
            print k, self.sChildren[k]


        self.sParamValues = dict.fromkeys( set(self.sParents.keys() + self.sChildren.keys()), [] )
        print "sParamValues ---------------------------------------------------"
        for k in sorted(self.sParamValues.keys()):
            print k, self.sParamValues[k]

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

        self.topologicalOrder = self.topologicalSort(self.paramValues, self.children)
        self.sTopologicalOrder = self.topologicalSort(self.sParamValues, self.sChildren)
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
                # count[sortKey] = 1

                for val in paramValues[child]:
                    newkey = tuple(sorted(((child, val),) + sortKey))
                    count[newkey] = 1

        # TODO: generate time sequence
        return count 

    # def isValidKey(self, child, parents):
    #     """ check the parameters-values combination is valid """
    #     if "T1" in child[0]:
    #         action = self.extractParam(parents, "Action")
    #         PositionCol = self.extractParam(parents, "PositionCol")
    #         PositionRow = self.extractParam(parents, "PositionRow")
    #     else:
    #         return True

    def extractParam(self, parents, keywd):
        for p in parents:
            if keywd in p[0]:
                return p

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
        return [k for k in self.sParamValues if varName[:-2] in k] 

    def checkTimeTag(self, parent, child):
        if parent[-1] == child[-1]:
            return parent[:-2], child[:-2]
        else:
            return parent[:-1] + "T0", child[:-1] + "T1"

    def train(self, trainData):
        print "Start training..."
        f = open(trainData, 'r')

        # get the variables and values, ignore trajector and time numbers
        data = [line.split()[1:] for line in f.readlines() if line.rstrip()]
        f.close()

        data = map(self.convertExampleToTuple, data)

        # do counting
        for d in data:
            # count action and position
            row, col, action = self.getCoordAction(d)
            if d[0] != 0: 
                key = tuple(sorted((self.addTimeTag(row, 1), self.addTimeTag(preRow, 0), self.addTimeTag(preAct, 0))))
                self.counting[key] += 1
                # key = tuple(sorted((self.addTimeTag(preRow, 0), self.addTimeTag(preAct, 0))))
                # self.counting[key] += 1
                key = tuple(sorted((self.addTimeTag(col, 1), self.addTimeTag(preCol, 0), self.addTimeTag(preAct, 0))))
                self.counting[key] += 1
                # key = tuple(sorted((self.addTimeTag(preRow, 0), self.addTimeTag(preAct, 0))))
                # self.counting[key] += 1
            preRow, preCol, preAct = row, col, action

            # count position and observation
            pos = tuple(sorted((row, col)))
            for v in [u for u in d[1:] if "Observe" in u[0]]:
                key = tuple(sorted((v,) + pos))
                self.counting[key] += 1
        for k in self.counting:
            print k, self.counting[k]

    def addTimeTag(self, tup, time):
        if time == 0:
            return (tup[0]+"_T0", tup[1])
        else:
            return (tup[0]+"_T1", tup[1])

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
        splitEX = map(lambda e: e.split("="), ex)
        output = [(e[0][:-2], e[1]) for e in splitEX[1:]]
        output.sort()
        output.insert(0, int(splitEX[0][0]))
        return tuple(output)

    def topologicalSort(self, paraValue, childDict):
        visited = set()
        order = []
        for node in sorted(paraValue):
            if node not in visited:
                self.dfs(node, visited, order, childDict)
        return tuple(order)

    def dfs(self, node, visited, order, childDict):
        """ for topolotical sort """
        visited.add(node)
        if node not in childDict:
            order.insert(0, node)
        else:
            for child in childDict[node]:
                if child not in visited:
                    self.dfs(child, visited, order, childDict)
            order.insert(0, node)

    def check(self):
        # check network parsing
        num = 0
        for k in self.nodes:
            num += 1
            print k, self.nodes[k].values
        print "total var num:", num

        # check training example parsing

    def printTopoOrder(self):
        print "------- topological order -------"
        for node in self.topologicalOrder:
            print node + " -> "

    def outputCPD(self):
        denoDP = {}

        for child in self.parents:
            print "--------------------------"
            print child
            childWithTime, parentWithTime, timeDiff = self.checkTime(child, self.parents[child])
            print childWithTime, parentWithTime

            parent = self.parents[child]
            combination = []
            for p in parent:
                val = self.paramValues[p]
                combination = self.genComb(combination, p, val)


            for pkey in combination:
                for val in self.paramValues[child]:
                    print (((child, val),) + pkey)
                    print "check", child, childWithTime
                    if timeDiff:
                        denKey = tuple(sorted(parentWithTime))
                        numKey = tuple(sorted(((childWithTime, val),) + denKey))
                    else:
                        denKey = tuple(sorted(self.removeTimeTag(pkey)))
                        numKey = tuple(sorted(((child[:-2], val),) + denKey))


                    if denKey not in denoDP:
                        self.denoDp[denKey] = sumDeno(child, )


                    # num = self.counting[numKey]
                    # den = self.counting[denKey]
                    # print self.tupToExp((child, val)), self.seperateParent(pkey), self.counting[numKey] / self.counting[denKey]
                    # newkey = tuple(sorted(((child, val),) + pkey))

    def printCPD(self, child, parents, prob):
        childList = list(map(self.tupleToString, child))
        childList.append(" ")
        parentList = list(map(self.tupleToString, parents))
        parentList.append(" ")
        parentList.append(str(prob))
        print "".join(childList + parentList)

    def tupleToString(self, tup):
        return tup[0] + "=" + tup[1]


    def removeTimeTag(self, tup):
        return tuple([(t[0][:-2], t[1]) for t in tup])

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
        for parent in parents:
            if parent[-1] != child[-1]:
                newParent.append(parent[:-1] + "T0")
                timeDiff = True
            else:
                newParent.append(parent[:-1] + "T1")
        if timeDiff:
            return child[:-1] + "T1", newParent, timeDiff
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
    pe.outputCPD()


