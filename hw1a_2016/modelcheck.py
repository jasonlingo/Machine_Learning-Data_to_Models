#!/usr/bin/python
import csv
from numpy import *
from numpy.linalg import *


def csvToMatrix(filename):
    """
    Read csv file and return data as matrices.
    :param filename: csv filename
    :return: X and Y matrices
    """
    with open(filename, 'rb') as csvfile:
        data = []
        rows = csv.reader(csvfile, delimiter=' ', quotechar='|')
        skipTitle = True
        for row in rows:
            if skipTitle:
                skipTitle = False
                continue
            rawData = row[0].split(",")
            data.append(rawData)
        mx = matrix(data, dtype=float)
        return mx[0:, 1:5], mx[0:, 5:]  # X, Y matrices,


def logLikelihood(X, Y, sigma, sigmaSquare, mu0):
    """
    Calculate the log likelihood according to the given parameters.
    Use Corollary 4.3.1 in Murphy's machine learning book to reduce the computation complexity of the inverse of a matrix.
    """
    dataCnt = X.shape[0]
    y_minus_xMu = Y - X * mu0
    xt_times_x = X.T * X

    # gamma = sigmaSquare * eye(dataCnt) + X * sigma * X.T  # 10000x10000, too large
    gammaInv = (1.0 / sigmaSquare) * eye(dataCnt) + sigmaSquare ** (-2) * X * inv(-inv(sigma) \
               - sigmaSquare ** (-1) * xt_times_x) * X.T

    # likelihood = (2 * pi) ** (-dataCnt / 2.0) * det(-inv(sigma) - sigmaSquare ** (-1) * xt_times_x) ** (-1) * exp(-0.5 * y_minus_xMu.T * gammaInv * y_minus_xMu)
    # The likelihood will become too small

    log_lh = (-dataCnt / 2.0 * log(2 * pi) - 0.5 * (dataCnt * log(sigmaSquare) + log(det(-inv(sigma) - sigmaSquare ** (-1) * xt_times_x))
              + log(det(-sigma))) - 0.5 * y_minus_xMu.T * gammaInv * y_minus_xMu)

    return log_lh[0, 0]


if __name__ == '__main__':

    # read data from csv file and export as a matrix
    X, Y = csvToMatrix("stocks.csv")

    # initial setting
    mu0 = matrix(zeros(4)).T
    sigmaSquare = 4
    sigma0Square = 1
    gammaSquare = 0.5
    sigma0 = eye(4) * 4
    sigmaAB = eye(4) * 4
    sigmaCD = eye(4) * 4
    sigmaAB[0, 1] = gammaSquare
    sigmaAB[1, 0] = gammaSquare
    sigmaCD[2, 3] = gammaSquare
    sigmaCD[3, 2] = gammaSquare

    print "M_0:", logLikelihood(X, Y, sigma0, sigmaSquare, mu0)
    print "M_AB:", logLikelihood(X, Y, sigmaAB, sigmaSquare, mu0)
    print "M_CD:", logLikelihood(X, Y, sigmaCD, sigmaSquare, mu0)



