"""
calculate the mean distance error between the predicted destination and true destination.
"""

from math import radians, cos, sin, asin, sqrt
import ast

EARTH_RADIUS_MILE = 3959.0
EARTH_RADIUS_KM = 6371.0

def haversine(lat1, lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Args:
      (float) lat1, lng1: the position of the first point
      (float) lat2, lng2: the position of the second point
    Return:
      (float) distance (in km) between two nodes
    """
    # Convert decimal degrees to radians
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # haversine formula
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    c = 2 * asin(sqrt(a))

    return c * EARTH_RADIUS_KM

def calcScore(labels, centers):
    dist = []
    for real, pred, realCenter in labels:
        predL = int(float(pred))
        predCenter = centers[str(predL)]
        realCenter = ast.literal_eval(realCenter)
        # realCenter = center[real]
        dist.append(haversine(realCenter[1], realCenter[0], predCenter[1], predCenter[0]))

    return sum(dist) / float(len(dist)),


if __name__=="__main__":
    # read cluster center
    f = open('../dataset/train/clusters.txt', 'r')
    data = [l.strip("\n").split("|")[:2] for l in f.readlines() if l]
    f.close()

    centers = {}
    for d, coord in data:
        centers[d] = ast.literal_eval(coord)

    # read prediction
    f = open('../dataset/train/result/prediction_200.txt', 'r')
    labels = [l.strip("\n").split("|") for l in f.readlines() if l and "--" not in l]
    f.close()

    print "mean distanct:", calcScore(labels, centers)



