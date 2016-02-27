from bayes_query import BayesQuery, Node



def parseNetwork(network):
    """
    Parse data from network file. The data includes:
    1. number of total variables
    2. values of each variables
    3. relationship between variables

    :param network: (string) the file name of a netowrk data
    """
    f = open(network, 'r')
    data = [line for line in f.readlines() if line.rstrip()]  # skip empty line
    nodes = {}

    numVar = int(data[0].strip())

    # store nodes' names and values
    for d in data[1:1 + numVar]:
        varName, values = d.strip().split()
        nodes[varName] = Node(varName, values.strip().split(","), None)

    f.close()
    return nodes.values()

    # store network relationship
    # for d in data[1 + self.numVar:]:
    #     if d:
    #         parent, child = [v.strip() for v in d.split("->")]
    #         parentNode = self.nodes[parent]
    #         childNode = self.nodes[child]
    #         parentNode.addChild(childNode)
    #         childNode.addParent(parentNode)

def genQuery(nodes):
    """ generate all possible queries """
    nodeNum = len(nodes)
    print nodeNum
    queries = []

    # for node in nodes:
    #     curQuery = []
    #     for q in queries:
    #         for value in node.values:
    #             curQuery.append(q + [(node.varName, value)])

    dfs(nodes, [], [], queries)

    output = open("query.txt", "r+")
    for query in queries:
        output.write(str(tuple(query)))

    output.close()
    return queries
        # dfs(nodes[:length], [], queries)



def dfs(nodes, used, path, query):
    if len(used) == len(nodes): return
    # print "used:", [d.varName for d in used], "path:", path

    for node in nodes:
        if node not in used:
            for value in node.values:
                newPath = path + [(node.varName, value)]
                query.append(newPath)
                dfs(nodes, used + [node], newPath, query)





if __name__=="__main__":
    networkFile = "network-extended.txt"
    cpdFile = "cpd-extended.txt"

    nodes = parseNetwork(networkFile)
    bayes = BayesQuery(networkFile, cpdFile)

    queries = genQuery(nodes)

    for lhs, rhs in queries:
        for i in range()
        if rhs:
            prob = bayes.condProb(lhs, rhs)
            print "p(%s|%s) = %f" % (lhs, rhs, prob)
        else:
            if len(lhs) > 1:
                prob = bayes.jointProb(lhs)
            else:
                prob = bayes.marginalProb(lhs)
            print "p(%s) = %f" % (lhs, prob)





