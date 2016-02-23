from collections import defaultdict
import argparse
import random


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
        self.parents = {}
        self.children = {}
        self.cpt = cpt

    def __eq__(self, other):
        return self.varName == other.varName

    def getExps(self):
        return [(self.varName, value) for value in self.values]

    # ===== parent related methods =============
    def addParent(self, parent):
        self.parents[parent.varName] = parent

    def isParentOf(self, other):
        return self.varName in other.parents

    def hasParent(self):
        return len(self.parents) > 0

    def getParents(self):
        return self.parents.values()

    # ===== child related methods ==============    
    def addChild(self, child):
        self.children[child.varName] = child

    def hasChild(self):
        return len(self.children) > 0

    def getChildren(self):
        return self.children.values()


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
        if dict1:
            return dict1.get(rhs, None)

    def getSubCPT(self, lhs):
        # print "Cond getSubCPT", lhs
        lhs = tuple(sorted(lhs))
        return self.cpt[lhs]

    def printCPT(self):
        for prob in self.cpt:
            for p in self.cpt[prob]:
                print prob, p, self.cpt[prob][p]


class BayesQuery(object):
    """
    A Bayes network class that can produce probabilities from a graphic model.
    """

    def __init__(self, network, cpd):
        self.nodes = {}
        self.cpt = ConditionalProbTable()
        self.jpt = {}                       # joint probability table
        self.numVar = 0                     # number of total variables
        self.prior= defaultdict(dict)
        self.parseNetwork(network)
        self.parseCPD(cpd)

    def parseNetwork(self, network):
        """
        Parse data from network file. The data includes:
        1. number of total variables
        2. values of each variables
        3. relationship between variables

        :param network: (string) the file name of a netowrk data
        """
        f = open(network, 'r')
        data = f.readlines()

        self.numVar = int(data[0].strip())

        # store nodes' names and values
        for d in data[1:1 + self.numVar]:
            varName, values = d.strip().split()
            self.nodes[varName] = Node(varName, values.strip().split(","), self.cpt)

        # store network relationship
        for d in data[1 + self.numVar:]:
            parent, child = [v.strip() for v in d.split("->")]
            parentNode = self.nodes[parent]
            childNode = self.nodes[child]
            parentNode.addChild(childNode)
            childNode.addParent(parentNode)

    def parseCPD(self, cpd):
        """
        Parse data from cpd file and build a conditional probability distribution (CPD). 

        :param cpd: (string) the file name of a cpd file
        """
        f = open(cpd, 'r')
        for cpd in f.readlines():
            self.cpt.addCPDFromFile(cpd)

        # add uniform distribution for Nodes with no parents
        for n in [node for node in self.nodes.values() if not node.hasParent()]:
            for value in n.values:
                self.prior[n.varName][value] = 1.0 / len(n.values)

        # print "-- CPT -------------"
        # self.cpt.printCPT()
        # print "-- prior -----------"
        # for n in self.prior:
        #     print n, self.prior[n]
        # print "--------------------"

    def topologicalSort(self, nodeList):
        """
        Iteratively find a node with no parent in the given expression list, 
        then move the node out of the list and repeat this process until 
        all node is move out of the original list.
        :param nodeList: a list of node to be sorted
        """
        # print "topologicalSort ----------"
        visited = []
        order = []
        for node in nodeList:
            if node not in visited:
                self.dfs(node, visited, order)
        return order

    def dfs(self, node, visited, order):
        """ for topolotical sort """
        visited.append(node)
        if not node.hasChild():
            order.append(node)
            return
        else:
            for child in node.getChildren():
                if child not in visited:
                    self.dfs(child, visited, order)
            order.append(node)

    def needMarginalProb(self, exp):
        """ 
        Check whether the query expression needs marginal probability.
        return needed variables for marginal probability.
        """
        # print "check marginal prob", exp
        varNames = [e[0] for e in exp]

        parents = set()
        for name in varNames:
            for parent in self.nodes[name].getParents():
                parents.add(parent.varName)
        parents = list(parents)
        return list(set(parents) - set(varNames))

    # ==============================================================
    # Probability calculation
    # ==============================================================

    def jointMarginProb(self, exp, margin):
        marginExp = []
        self.generateMarginExp(margin, marginExp, 0, [])
        prob = 0
        for marExp in marginExp:
            prob += self.jointProb(exp + (marExp,))
        return prob

    def generateMarginExp(self, margin, marginExp, idx, path):
        if idx == len(margin):
            marginExp.append(path[0])
            return
        node = self.nodes[margin[idx]]
        values = node.values
        for value in values:
            self.generateMarginExp(margin, marginExp, idx + 1, path + [(node.varName, value)])

    def jointProb(self, exp):
        """ use chain rule to calculate the joint probability """
        # print "Joint prob:", exp
        if len(exp) <= 1: 
            return self.marginalProb(exp)

        # check whether the joint probability already exists in the joint probability table
        if self.jpt.get(tuple(sorted(exp)), None):
            return self.jpt[tuple(sorted(exp))]

        # check whether the probability need marginal probability
        marginParent = self.needMarginalProb(exp)
        if marginParent:
            return self.jointMarginProb(exp, marginParent)

        # topological sort, find the order for chain rule
        nodeList = [self.nodes[e[0]] for e in exp]
        order = self.topologicalSort(nodeList)
        # rebuild query expression according to the topological sort
        jointExp = []
        for node in order:
            for e in exp:
                if node.varName == e[0]:
                    jointExp.append(e)
                    break
        jointExp = tuple(jointExp)
        
        # perform chain rule to get the joint probability
        prob = 1
        for i, exp in enumerate(jointExp):
            if i == len(jointExp) - 1:
                prob *= self.marginalProb((exp,))
            else:
                prob *= self.condProb((exp,), jointExp[i+1:])
        self.jpt[tuple(sorted(exp))] = prob
        return prob

    def marginalProb(self, exp):
        """ Calculate marginal probability """
        # print "Get marginal", exp

        # if len(exp) > 1, it means that we want to find joint probability
        if len(exp) > 1:
            return self.jointProb(exp)

        # if the node has no parents, return its prior
        node = self.nodes[exp[0][0]]
        if not node.hasParent():
            return self.prior[ exp[0][0] ][ exp[0][1] ]
        
        # if the node has parents, need to sum over all possible eqery conditioned on its parents
        conditions = self.cpt.getSubCPT(exp)
        prob = 0
        for cond in conditions:
            prob += self.condProb(exp, cond) * self.jointProb(cond)
        return prob

    def condProb(self, lhs, rhs):
        """ Calculate conditional probability """
        # print "condProb:", lhs, "|", rhs 
        prob = self.cpt.getProb(lhs, rhs)
        if prob: return prob

        # conditional probability not in the CPT
        jointP = self.jointProb(lhs + rhs)
        marginP = self.marginalProb(rhs)
        self.cpt.addCPD(lhs, rhs, jointP / marginP)  # now we don't need this, but this can speed up for large amount of queries
        return jointP / marginP
        

def parseQuery(query):
    """ 
    parse query expression into tuple 
    e.g. MaryGetsFlu=Yes => ("MaryGetsFlu", "Yes")
    """
    if not query: 
        return None
    return tuple(sorted([tuple(e.split("=")) for e in query.strip().split(",")]))
            

if __name__=="__main__":
    # Get the arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('network', help='produces trees instead of strings')
    parser.add_argument('cpd', help='conditional probability distribution')
    parser.add_argument('lhs', type=str, help="the left hand side of a conditional probability")
    parser.add_argument('rhs', nargs='?', default=None, type=str, help="the right hand side of a conditional probability (optional)")

    args = parser.parse_args()
    network = args.network
    cpd = args.cpd
    lhs = parseQuery(args.lhs)
    rhs = parseQuery(args.rhs)

    # print "--------------------"
    # print "Input: left hand side:", lhs, ", right hand side:", rhs

    # create a BayesQuery object and parse the network and cpd file.
    bayes = BayesQuery(network, cpd)
    
    # query the probability
    if rhs:
        prob = bayes.condProb(lhs, rhs)
    else:
        if len(lhs) > 1:
            prob = bayes.jointProb(lhs)
        else:
            prob = bayes.marginalProb(lhs)

    print "%.13e" % prob

