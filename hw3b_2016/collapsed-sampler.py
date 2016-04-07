#!/usr/bin/python
from __future__ import division
import argparse
import numpy as np



class CollapseGibb(object):
    """
    a collapsed Gibb sampler
        d       : document index
        C_d     : {A, S},
                  where A: ACL, S: NIPS
        w_{d,i} : words set index
        V       : total number of word
        v       : indexes the v-th word in the vocabulary
        K       : total topics
        phi_k   : global parameter
        phi_k^c : collection parameter
        theta_d : mixing proportions for the topics in document d
        N_d     : the number of words in the document d
        Z_{d,i} : topic index, sampled from Mult(theta_d)
        lambda  : the probability that the word w_{d,i} is sampled according to the collection-specific distribution phi_k^c
        x_{d,i} : binary random variable, whether to use phi or phi^c
                  x is a Bernoulli random variable with parameter lambda
        alpha, beta, lambda : are hyperparameters that is the parameter of prior distribution
    """

    def __init__(self):
        self.lamb  = None
        self.alpha = None
        self.beta  = None
        self.k     = None
        self.v     = None
        self.wType = {}
        self.ndk   = None
        self.nds   = None
        self.nkw   = None
        self.nckw  = None
        self.ncks  = None

    def sampling(self, train, test, output, k, lamb, alpha, beta, iterNum, biNum):
        self.k = k
        self.alpha = alpha
        self.beta = beta
        self.lamb = lamb

        #Parse input data
        trainData = self.parseDoc(train)
        testData  = self.parseDoc(test)

        self.buildWType(trainData)


    def buildWType(self, docs):
        idx = 0

        for d in docs:
            for s in d[1:]:





    def train(self):
        pass


    def parseDoc(self, file):
        """ split each line and return as a list of lists """
        f = open(file, 'r')
        data = [doc.split() for doc in f.readlines()]
        f.close()
        return data


















if __name__=="__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('train', type=str, help='training data file')
    # parser.add_argument('test', type=str, help='test data file')
    # parser.add_argument('output', type=str, help='output file name')
    # parser.add_argument('k', type=str, help='number of topics')
    # parser.add_argument('lamb', type=str, help='lambda')
    # parser.add_argument('alpha', type=str, help='alpha')
    # parser.add_argument('beta', type=str, help='beta')
    # parser.add_argument('iterNum', type=str, help='total number of iterations')
    # parser.add_argument('biNum', type=str, help='number of burn-in samples')
    #
    # args    = parser.parse_args()
    # train   = args.train
    # test    = args.test
    # output  = args.output
    # k       = args.k
    # lamb    = args.lamb
    # alpha   = args.alpha
    # beta    = args.beta
    # iterNum = args.iterNum
    # biNum   = args.biNum

    #####################
    # for testing
    #####################
    train   = 'hw3b-files/input-train.txt'
    test    = 'hw3b-files/input-test.txt'
    output  = 'output.txt'
    k       = 10
    lamb    = 0.5
    alpha   = 0.1
    beta    = 0.01
    iterNum = 1100
    biNum   = 1000
    #####################


    cg = CollapseGibb()
    cg.sampling(train, test, output, k, lamb, alpha, beta, iterNum, biNum)



