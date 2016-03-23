#!/usr/bin/python
from __future__ import division
import argparse
import random
import math
import time


def parseExp(exp):
    """
    Convert expression into tuple
    e.g. MaryGetsFlu=Yes => ("MaryGetsFlu", "Yes")
    """
    if exp:
        return [tuple(e.split("=")) for e in exp.strip().split(",")]

def createCombination(varValues):
    """
    Generate all combination of variables and values.
    """
    res = []
    pre = []
    for var in sorted(varValues):
        res = []
        if pre:
            for v in varValues[var]:
                for c in pre:
                    res.append(c + ((var, v),))
        else:
            for v in varValues[var]:
                res.append(((var, v),))
        pre = res
    return res

class ConditionalProbTable(object):
    """ The class that deals with conditional probability table """

    def __init__(self):
        self.cpt = {}

    def addCPD(self, cpd):
        """ add cpd from input string of cpd file and convert the probability to log-prob"""
        lhs, rhs, prob = cpd.strip().split()
        lhs = tuple(sorted(parseExp(lhs)))
        rhs = tuple(sorted(parseExp(rhs)))
        if lhs in self.cpt:
            self.cpt[lhs][rhs] = math.log(float(prob))
        else:
            self.cpt[lhs] = {}
            self.cpt[lhs][rhs] = math.log(float(prob))

    def getProb(self, lhs, rhs):
        lhs = tuple(sorted(lhs))
        rhs = tuple(sorted(rhs))
        dict1 = self.cpt.get(lhs, None)
        if dict1 is not None:
            return dict1.get(rhs, None)

    def getAllCPD(self):
        return self.cpt


class Factor(object):

    def __init__(self, lhs, rhs, prob):
        self.lhs = sorted([v[0] for v in lhs])
        self.rhs = sorted([v[0] for v in rhs])
        self.prob = {}
        self.addProb(lhs, rhs, prob)
        self.key = None

    def addProb(self, lhs, rhs, prob):
        query = self.genQuery(lhs, rhs)
        self.prob[query] = prob

    def getProb(self, lhs, rhs):
        query = self.genQuery(lhs, rhs)
        return self.prob.get(query, None)

    def getVarProb(self, vars):
        lhsExp = [d for d in vars if d[0] in self.lhs]
        rhsExp = [d for d in vars if d[0] in self.rhs]
        query = self.genQuery(lhsExp, rhsExp)
        return self.prob.get(query, None)

    def getAllProb(self):
        return self.prob

    def combineFactor(self, other):
        """ update probabilities from other factor """
        self.prob.update(other.getAllProb())

    def getKey(self):
        if not self.key:
            self.key = str(self.lhs) + " " + str(self.rhs)
        return self.key

    @staticmethod
    def genQuery(lhs, rhs):
        lhsStr = ",".join(sorted([v[0] + "=" + v[1] for v in lhs]))
        rhsStr = ",".join(sorted([v[0] + "=" + v[1] for v in rhs]))
        return lhsStr + " " + rhsStr


class Edge(object):

    def __init__(self, cluster1, cluster2):
        self.cluster1 = cluster1
        self.cluster2 = cluster2
        self.sepset = cluster1.getVariables().intersection(cluster2.getVariables())
        self.mu = 1
        self.key = None

    def updateMu(self, msg):
        self.mu = msg.copy()

    def passMessage(self, fromClut, targetClut, msg):
        msg = self.normalize(msg)
        if self.mu == 1:
            self.updateMu(msg)
            targetClut.receiveMessage(fromClut, msg)
        else:
            newMsg = self.divideMu(msg)
            self.updateMu(msg)
            targetClut.receiveMessage(fromClut, newMsg)

    def normalize(self, msg):
        z = sum([math.exp(p) for p in msg.values()])
        for k in msg:
            msg[k] = math.log(math.exp(msg[k]) / z)
        return msg

    def divideMu(self, msg):
        newMsg = {}
        for k in msg:
            newMsg[k] = msg[k] - self.mu[k]  # TODO: only multiply those in msg?
        return newMsg

    def getSepset(self):
        return self.sepset

    def reset(self):
        self.mu = 1

    def getKey(self):
        if not self.key:
            self.key = self.genKey(self.cluster1, self.cluster2)
        return self.key

    @staticmethod
    def genKey(cluster1, cluster2):
        key = sorted([cluster1.name, cluster2.name])
        return " -- ".join(key)


class Cluster(object):

    def __init__(self, name, values):
        # all the variables' name
        self.name = name

        # all the varialbes
        self.variables = set()

        # all the variable and their values
        self.varValues = {}

        # all the neighbor clusters
        self.neighbors = {}
        self.edges = {}

        # all the messages from every neighbor
        self.msgs = {}

        # all the factors in this cluster
        self.factors = {}

        # the initial potential
        self.initPotential = {}
        self.initPotentialFlag = False

        # cluster belief
        self.beta = None

        self.addVariables(name, values)

        # for upward and downward pass
        self.parent = None
        self.children = []

        self.allCombination = None
        self.combination = {}
        self.evidence = None


    def addFactor(self, factor):
        orgFactor = self.factors.get(factor.getKey(), None)
        if orgFactor:
            orgFactor.combineFactor(factor)
        else:
            self.factors[factor.getKey()] = factor

    def addVariables(self, exp, values):
        for v in exp.strip().split(","):
            self.variables.add(v)
            self.varValues[v] = values[v]

    def getVariables(self):
        return self.variables

    def addNeighbor(self, other, edge):
        self.neighbors[other.name] = other
        self.edges[other.name] = edge

    def getNeighbors(self):
        return self.neighbors

    def computeInitBelief(self):
        combination = createCombination(self.varValues)
        for vars in combination:
            vars = tuple(sorted(vars))
            prob = 0
            hasProb = True
            for f in self.factors.values():
                subProb = f.getVarProb(vars)
                if subProb is not None:
                    prob += subProb
                else:
                    hasProb = False
                    break
            if hasProb:
                self.initPotential[vars] = prob   # FIXME: should include variable not in the factors?
        self.reset()

    def query(self, que, evidence):
        lhs = set(que[0])
        combination = self.checkEvidence(createCombination(self.varValues), evidence)
        normalize = [self.beta.get(q) for q in combination]
        normalize = sum([math.exp(p) for p in normalize if p is not None])

        queExp = [q for q in combination if lhs.issubset(set(q))]
        querySum = [self.beta.get(q) for q in queExp]
        querySum = sum([math.exp(p) for p in querySum if p is not None])
        print "%.13e" % (querySum / normalize)

    def isLeaf(self):
        return len(self.children) == 0

    def passMessage(self, targetCluster, evidence):
        edge = self.edges[targetCluster.name]
        if self.allCombination is None or evidence != self.evidence:
            self.allCombination = createCombination(self.varValues)
            self.allCombination = self.checkEvidence(self.allCombination, evidence)
            self.allCombination = [set(p) for p in self.allCombination]
            self.evidence = evidence

        if targetCluster.name not in self.combination:
            varValue = {}
            for var in edge.getSepset():
                varValue[var] = self.varValues[var]
            combination = createCombination(varValue)
            self.combination[targetCluster.name] = combination

        allCombination = self.allCombination
        combination = self.combination[targetCluster.name]
        msg = {}
        for var in combination:
            prob = self.sumOver(set(var), allCombination)
            if prob is not None:
                msg[tuple(sorted(var))] = prob
        edge.passMessage(self, targetCluster, msg)

    def sumOver(self, varValue, allComb):
        query = [tuple(q) for q in allComb if varValue.issubset(q)]
        if not query:
            return None
        prob = 0
        for q in query:
            p = self.beta.get(tuple(sorted(q)), None)
            if p is not None:
                prob += math.exp(p)

        if prob == 0:
            return None
        else:
            return math.log(prob)  # FIXME: if prob == 0, need to send it to next point to make related item zero?

    def checkEvidence(self, combination, evidence):
        newComb = []
        for c in combination:
            add = True
            for var, val in c:
                if var in evidence and val != evidence[var]:
                    add = False
                    break
            if add:
                newComb.append(c)
        return newComb

    def receiveMessage(self, fromCluster, msg):
        self.msgs[fromCluster.name] = msg.copy()
        for m in msg:
            for b in self.beta:
                if self.match(m, b):
                    self.beta[b] += msg[m]

    def match(self, msgKey, betaKey):
        """ if the mesKey is contained in the betaKey, return True """
        m = set(msgKey)
        b = set(betaKey)
        return m.issubset(b)

    def addParent(self, pa):
        self.parent = pa

    def getParent(self):
        return self.parent

    def addChild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def contains(self, vars):
        """ check this cluster contains all the given variables """
        varSet = set(vars)
        return varSet.issubset(self.varValues)

    def resetParentChild(self):
        self.parent = None
        self.children = []

    def reset(self):
        self.beta = self.initPotential.copy()
        self.msgs = {}
        self.allCombination = None
        self.combination = {}

    def isChildMsgReady(self):
        if not self.children:
            return True
        childName = set([clust.name for clust in self.children])
        inMsg = set(self.msgs)
        return childName.issubset(inMsg)

class BayesQuerySP(object):

    def __init__(self):
        # the input files
        self.network = None
        self.clique  = None
        self.cpd = None

        # store clusters
        self.clusters = {}
        self.edges = {}

        # store the clusters that a variable belongs to
        self.varToCluster = {}

        # store the variables and cluster numbers
        self.varNum = None
        self.cliqueNum = None

        # store variables and their values
        self.variables = {}

        # store conditional probabilities
        self.cpt = ConditionalProbTable()

        # keep the evidence from queries
        self.evidence = {}
        self.preRoot = None

    def cTreeBUCalibrate(self, network, cpd, clique):
        self.network = network
        self.cpd     =  cpd
        self.clique  = clique

        self.parseNetwork(network)
        self.parseCPD(cpd)
        self.initCTree(clique)

    def parseNetwork(self, network):
        """
        Get the variables' name and their values.
        Store the data in the self.variables dictionary.
        :param network (str): the network file
        """
        f = open(network, 'r')
        data = [l for l in f.readlines() if l.rstrip()]
        f.close()

        self.varNum = int(data[0].strip())
        data = [l.split() for l in data[1 : 1 + self.varNum]]
        for var, vals in data:
            self.variables[var] = vals.split(",")

    def parseCPD(self, cpd):
        f = open(cpd, 'r')
        data = [l for l in f.readlines() if l.rstrip()]
        f.close()
        map(self.cpt.addCPD, data)

    def initCTree(self, clique):
        """
        Initialize clique tree
        """
        f = open(clique, 'r')
        data = [l.rstrip("\n") for l in f.readlines()]
        f.close()

        # construct clusters
        self.cliqueNum = int(data[0].strip())
        self.constructCluster(data[1 : 1 + self.cliqueNum])
        self.assignFactor(self.cpt.getAllCPD())
        self.connectCluster(data[1 + self.cliqueNum :])

        # initialize each clique's potential
        for cluster in self.clusters.values():
            cluster.computeInitBelief()

    def constructCluster(self, data):
        """ construct clusters according to the clique tree data"""
        for d in data:
            cluster = Cluster(d, self.variables)
            self.clusters[d] = cluster
            for var in d.split(","):
                if var in self.varToCluster:
                    self.varToCluster[var].append(cluster)
                else:
                    self.varToCluster[var] = [cluster]

    def connectCluster(self, edges):
        """ connect cluster and create a Edge object between them """
        for e in edges:
            clusterNames = [c for c in e.split(" -- ")]
            clut1 = self.clusters[clusterNames[0]]
            clut2 = self.clusters[clusterNames[1]]
            edge = Edge(clut1, clut2)
            clut1.addNeighbor(clut2, edge)
            clut2.addNeighbor(clut1, edge)
            self.edges[edge.getKey()] = edge

    def assignFactor(self, cpds):
        """
        Get factors from the cpds and assign a corresponding cluster that contains all the variables of the factor.
        :param cpds:
        :return:
        """
        dispatchToCluster = {}
        for lhs in cpds:
            for rhs in cpds[lhs]:
                factor = Factor(lhs, rhs, cpds[lhs][rhs])

                # find the cluster that contains all the variables in lhs and rhs
                if factor.getKey() in dispatchToCluster:
                    targetCluster = dispatchToCluster[factor.getKey()]
                else:
                    clustersForKey = []
                    keys = [d[0] for d in lhs + rhs]
                    for key in keys:
                        clustersForKey.append(set(self.varToCluster[key]))
                    intersects = list(reduce(lambda x, y: x.intersection(y), clustersForKey))
                    targetCluster = random.choice(intersects)
                    dispatchToCluster[factor.getKey()] = targetCluster
                targetCluster.addFactor(factor)

    def initBU(self, que):
        """
        Initialize belief update process:
        Choose an cluster as the root and run a dfs to set parent and child relationship
        for each cluster.
        """
        if not (self.preRoot and self.preRoot.contains([q[0] for q in que[0]])):
            root = self.findRoot([d[0] for d in que[0]])
            for clus in self.clusters.values():
                clus.resetParentChild()
            self.setParentChild(root)
            self.preRoot = root
        root = self.preRoot
        if self.checkRecalibration(que[1]):
            self.addEvidence(que[1])
            self.upwardPass()
            self.downwardPass(root)
        return root

    def upwardPass(self):
        """ pass messages from leaves to root """
        queue = [c for c in self.clusters.values() if c.isLeaf()]
        while queue:
            child = queue.pop(0)
            parent = child.getParent()
            if parent is not None:
                if child.isChildMsgReady():
                    child.passMessage(parent, self.evidence)
                    if parent not in queue:
                        queue.append(parent)
                else:
                    queue.append(child)

    def downwardPass(self, root):
        """ pass messages from root to leaves """
        # if not root.isChildMsgReady():
        #     print "Err: root is not ready to pass msg"
        queue = [root]
        while queue:
            parent = queue.pop(0)
            for child in parent.getChildren():
                parent.passMessage(child, self.evidence)
                queue.append(child)
            # if len(queue) % 5 == 0:
            #     print len(queue)

    def checkRecalibration(self, que):
        """ if need recalibration, return True """
        org = set(self.evidence.items())
        # if que is None:
        #     que = []
        new = set(que)
        if org.issubset(new) and len(org) < len(new):
            # original evidence is a subset of new evidence: additive
            return True
        elif len(org.difference(new)) > 0:
            # there is at least one evidence in the original evidence set
            # but not in the new evidence set: retractive
            self.resetBelief()
            self.evidence = {}
            return True
        else:
            # the evidences are the same, no need to recalibrate
            return False

    def resetBelief(self):
        for clus in self.clusters.values():
            clus.reset()
        for e in self.edges.values():
            e.reset()

    def addEvidence(self, evi):
        for key, val in evi:
            self.evidence[key] = val

    def setParentChild(self, root):
        queue = [root]
        while queue:
            curr = queue.pop(0)
            parent = curr.getParent()
            for clus in curr.getNeighbors().values():
                if clus != parent:
                    curr.addChild(clus)
                    clus.addParent(curr)
                    queue.append(clus)

    def findRoot(self, vars):
        """ find all the clusters that contain all the variables """
        roots = []
        for clut in self.clusters.values():
            if clut.contains(vars):
                roots.append(clut)
        if len(roots) == 0:
            print vars
        return random.choice(roots)

    def query(self, queryFile):
        f = open(queryFile, 'r')
        queryData = [self.parseQuery(line) for line in f.readlines() if line.rstrip()]
        f.close()

        for que in queryData:
            root = self.initBU(que)
            root.query(que, self.evidence)

    def parseQuery(self, query):
        q = query.strip().split()
        lhs = [tuple(d.split("=")) for d in q[0].split(",")]
        if len(q) > 1:
            rhs = [tuple(d.split("=")) for d in q[1].split(",")]
        else:
            rhs = []
        return (lhs, rhs)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('network', type=str, help='original network file')
    parser.add_argument('cpd', type=str, help='original CPD file')
    parser.add_argument('clique', type=str, help='original clique tree file')
    parser.add_argument('query', type=str, help='query file')

    args    = parser.parse_args()
    network = args.network
    cpd     = args.cpd
    clique  = args.clique
    query   = args.query

    bq = BayesQuerySP()
    bq.cTreeBUCalibrate(network, cpd, clique)
    bq.query(query)