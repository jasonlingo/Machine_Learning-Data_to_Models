"""
interact with neural network algorithm and calculate the accuracy and print the training status.
"""

import numpy as np
from collections import Counter
import datetime
from NeuralNetwork import NeuralNetwork

class Classifier:

    def __init__(self, classifier_type, **kwargs):
        """
        Initialize a classifier for managing learning model.
        Args:
            classifier_type: the type of learning model. e.g. neural_network
            **kwargs: store parameter in a dictionary
        """
        self.classifier_type = classifier_type
        self.params = kwargs

        self.clf = None
        self.file = open('../dataset/train/result/trial_' + str(datetime.datetime.today()).replace("/", "_", -1) + ".txt", 'w', 0)

    def train(self, training_data, testData, classNum, batchSize):
        """
        Create a learning model. Train the model with the training data. Print the training accuracy every certain iterations.
        If the learning rate is not chosen appropriately, let the user to enter a new
        """
        # find the numbers for feature and label
        featureNum = training_data.shape[1] - 1

        # #this will find all the unique labels automatically, but will have problem when training data is lacking some labels
        # labelNum = len(np.unique(training_data[:, :1]))
        labelNum = classNum

        # get the number of nodes for each layer
        if "hidden_layer" in self.params and self.params["hidden_layer"] is not None:
            nodeNum = [featureNum] + self.params["hidden_layer"] + [labelNum]
        else:
            nodeNum = [featureNum, featureNum * 2, labelNum]

        # get the mode for initializing the weight
        if "weightInitMode" in self.params and self.params["weightInitMode"] is not None:
            weightInitMode = self.params["weightInitMode"]
        else:
            weightInitMode = None

        # get the momentum factor
        if "momentumFactor" in self.params:
            momentumFactor = self.params["momentumFactor"]
        else:
            momentumFactor = 0.0

        self.clf = NeuralNetwork(training_data, nodeNum, weightInitMode, momentumFactor)
        iteration = 5
        totalIter = 0
        testSize  = 100000
        while iteration > 0:

            if iteration < 10:
                self.clf.train(iteration, batchSize)
                totalIter += iteration
                print "---------- Settings ----------"
                print "Examples                 :", training_data.shape[0]
                print "Batch size               :", batchSize
                print "Alpha                    :", self.clf.getAlpha()
                print "Momentum factor          :", momentumFactor
                print "# of Nodes in all layers :", nodeNum
                print "Training iteration so far:", totalIter
                self.file.write("\n")
                self.file.write("---------- Settings ----------" + "\n")
                self.file.write("Examples                 : " + str(training_data.shape[0]) + "\n")
                self.file.write("Batch size               : " + str(batchSize) + "\n")
                self.file.write("Alpha                    : " + str(self.clf.getAlpha()) + "\n")
                self.file.write("Momentum factor          : " + str(momentumFactor) + "\n")
                self.file.write("# of Nodes in all layers : " + str(nodeNum) + "\n")
                self.file.write("Training iteration so far: " + str(totalIter) + "\n")
                #self.test(training_data, "training")
                self.test(testData, "testing")
                iteration = 0

            while iteration >= testSize:
                self.clf.train(testSize, batchSize)
                totalIter += testSize
                print "---------- Settings ----------"
                print "Examples                 :", training_data.shape[0]
                print "Batch size               :", batchSize
                print "Alpha                    :", self.clf.getAlpha()
                print "Momentum factor          :", momentumFactor
                print "# of Nodes in all layers :", nodeNum
                print "Training iteration so far:", totalIter
                self.file.write("\n")
                self.file.write("---------- Settings ----------" + "\n")
                self.file.write("Examples                 : " + str(training_data.shape[0]) + "\n")
                self.file.write("Batch size               : " + str(batchSize) + "\n")
                self.file.write("Alpha                    : " + str(self.clf.getAlpha()) + "\n")
                self.file.write("Momentum factor          : " + str(momentumFactor) + "\n")
                self.file.write("# of Nodes in all layers : " + str(nodeNum) + "\n")
                self.file.write("Training iteration so far: " + str(totalIter) + "\n")
                #self.test(training_data, "training")
                self.test(testData, "testing")
                iteration -= testSize

            if iteration > 0:
                self.clf.train(iteration, batchSize)
                totalIter += iteration
                print "---------- Settings ----------"
                print "Examples                 :", training_data.shape[0]
                print "Batch size               :", batchSize
                print "Alpha                    :", self.clf.getAlpha()
                print "Momentum factor          :", momentumFactor
                print "# of Nodes in all layers :", nodeNum
                print "Training iteration so far:", totalIter
                self.file.write("\n")
                self.file.write("---------- Settings ----------" + "\n")
                self.file.write("Examples                 : " + str(training_data.shape[0]) + "\n")
                self.file.write("Batch size               : " + str(batchSize) + "\n")
                self.file.write("Alpha                    : " + str(self.clf.getAlpha()) + "\n")
                self.file.write("Momentum factor          : " + str(momentumFactor) + "\n")
                self.file.write("# of Nodes in all layers : " + str(nodeNum) + "\n")
                self.file.write("Training iteration so far: " + str(totalIter) + "\n")
                #self.test(training_data, "training")
                self.test(testData, "testing")
                iteration = 0

            print ""
            restart = raw_input("Do you want to restart? (Y/N)")
            if restart.upper() == "Y":
                totalIter = 0
                print "Current Alpha is", self.clf.getAlpha()
                alpha = raw_input("What alpha ?")
                self.clf.setAlpha(float(alpha))
                self.clf.initTheta()
                self.file.write("\n")
                self.file.write("*****************************************************\n")
                self.file.write("Re-initialize trail with alpha = " + str(alpha) + "\n")
                self.file.write("*****************************************************\n")

            print ""
            iteration = raw_input("How many iteration do you want to train the model?")
            try:
                iteration = int(iteration)
            except:
                iteration = raw_input("Please input an integer")
                iteration = 1
        print "Total training iterations:", totalIter

    def predict(self, data):
        """

        """
        return self.clf.predict(data)

    def test(self, test_data, mode, testCenter=None, predFilename=''):
        """

        """
        print "mode:", mode

        if mode == "test":
            f = open(predFilename, 'w')
            f.write("--------------------------------------------\n")
        correct = 0
        countPrediction = {}
        countCorrect = {}
        countTotal = Counter(list(test_data[:, 0]))
        allPrediction = {}

        labels = np.unique(test_data[:, 0])
        for label in labels:
            countCorrect[int(label)] = 0
            countPrediction[int(label)] = 0
            allPrediction[int(label)] = 0

        for i, e in enumerate(test_data):
            label = int(e[0])
            pred_label = self.predict(e)

            if mode == "test":
                f.write(str(label) + "|" + str(pred_label) + "|" + str(testCenter[i]) + "\n")

            if label == pred_label:
                correct += 1
                if label in countCorrect:
                    countCorrect[label] += 1
                else:
                    countCorrect[label] = 1
            if pred_label in allPrediction:
                allPrediction[pred_label] += 1
            else:
                allPrediction[pred_label] = 1

            if pred_label in countPrediction:
                countPrediction[pred_label] += 1
            else:
                countPrediction[pred_label] = 1

        if mode == "test":
            f.close()

        print "---------- Result ----------"
        print "Alpha is", self.clf.getAlpha()
        print "Count correct", [[d, countCorrect[d]] for d in countCorrect if countCorrect[d] > 0]
        print "All predictions", [[d, allPrediction[d]] for d in allPrediction if allPrediction[d] > 0]
        accuracy = float(correct) / len(test_data)
        print "The accuracy for", mode, "is", accuracy
        self.file.write("---------- Result ----------" + "\n")
        self.file.write("Alpha is " + str(self.clf.getAlpha()) + "\n")
        self.file.write("Count correct " + str([[d, countCorrect[d]] for d in countCorrect if countCorrect[d] > 0]) + "\n")
        self.file.write("All predictions " + str([[d, allPrediction[d]] for d in allPrediction if allPrediction[d] > 0]) + "\n")
        self.file.write("The accuracy for " + mode + " is " + str(accuracy) + "\n")

    def getAttrValue(self, ex):
        """
        Find the attribute values for each attribute.
        Args:
            ex: given examples
        Returns: a dictionary where the keys are the attribute indices and the values are the attribute values.
        """
        attrValue = {}
        for i in range(len(ex[0])):
            attrValue[i] = list(set([v for v in ex[:, i]]))
        return attrValue