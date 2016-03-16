#!/usr/bin/python

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

        # store nodes' names and values
        for d in data[1:1 + self.numVar]:
            varName, values = d.strip().split()
            self.nodes[varName] = Node(varName, values.strip().split(","), self.cpt)    
            self.paramValues[varName] = values.strip().split(",")

        # store network relationship
        for d in data[1 + self.numVar:]:
            parent, child = [v.strip() for v in d.split("->")]
            parentNode = self.nodes[parent]
            childNode = self.nodes[child]
            parentNode.addChild(childNode)
            childNode.addParent(parentNode)

            if parent in self.children:
                self.children[parent].append(child)
            else:
                self.children[parent] = [child]

            if child in self.parents:
                self.parents[child].append(parent)
            else:
                self.parents[child] = [parent]

        
        self.topologicalSort()

    def train(self, trainData):
        self.parseTrainData(trainData)

        # do the counting



    def parseTrainData(self, trainData):
        f = open(trainData, 'r')

        # get the variables and values, ignore trajector and time numbers
        data = [line.split()[2:] for line in f.readlines() if line.rstrip()]
        data = map(self.convertExampleToTuple, data)
        
        # count the times for each combination
        map(self.cumulate, data)
        # for k in self.timeStep:
        #     print k, self.timeStep[k

    def cumulate(self, key):
        self.eventCount[key] = self.eventCount.get(key, 0) + 1

    def convertExampleToTuple(self, ex):
        splitEX = map(lambda e: e.split("="), ex)
        output = [(e[0][:-2], e[1]) for e in splitEX]
        output.sort()
        return tuple(output)

    def topologicalSort(self):
        visited = set()
        order = []
        for node in self.paramValues.keys():
            if node not in visited:
                self.dfs(node, visited, order)
        self.topologicalOrder = tuple(order)

    def dfs(self, node, visited, order):
        """ for topolotical sort """
        visited.add(node)
        if node not in self.children:
            order.insert(0, node)
            return
        else:
            for child in self.children[node]:
                if child not in visited:
                    self.dfs(child, visited, order)
            order.insert(0, node)
        
    def estimate(self, query):
        pass

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
    # pe.printTopoOrder()
    # pe.check()         
    

