import argparse


class BayesQuerySP(object):

    def __init__(self):



    def computeSepset(self, c1, c2):
        """
        :param c1: cluster 1
        :param c2: cluster 2
        :return: the number of variables exist in c1 and c2
        """
        nodes1 = c1.getNodes()
        nodes2 = c2.getNodes()
        return len(nodes1.intersection(nodes2))


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('network', type=str, help='original network file')
    parser.add_argument('output', type=str, help='output clique file')

    args    = parser.parse_args()
    network = args.network
    output  = args.output

    bq = BayesQuerySP()

    if network:
        bq.parse(network)