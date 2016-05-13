"""
Plot the clusters on the map.
"""

import os
import pygmaps
import webbrowser
import ast


def showMap(points, outputDirectory):
    """
    Show GPS path and extracted street view images' locations on Google map.

    Args:
      (list) path: a list of GPS data of a path.
      (list) framePoint: a list of GPS data of extracted video frames.
      (String) outputDirectory: the folder for storing this map file.
    """

    # Set the center of this map. Using the starting point of the
    # path as the center of the map.
    mymap = pygmaps.maps(points[0][0], points[0][1], 10)

    # Add every points in framePoint to this map.
    for point in points:
        # Set the first point with color = "#00FF00".
        mymap.addpoint(point[0], point[1], "#1515f4")

    # Create this map.
    mapFilename = outputDirectory + "map.html"
    mymap.draw('./' + mapFilename)

    # Create the local link to this map file.
    url = "file://" + os.getcwd() + "/" + mapFilename

    # Open this map on a browser
    webbrowser.open_new(url)


if __name__=="__main__":
    f = open('../dataset/train/clusters.txt', 'r')
    data = f.readlines()
    f.close()

    data = [d.strip("\n").split("|") for d in data]
    data = [ast.literal_eval(d[1]) for d in data if int(d[2]) > 1]
    print "# of clusters:", len(data)
    centers = map(lambda x: [x[1], x[0]], data)

    showMap(centers, '../dataset/train/')
