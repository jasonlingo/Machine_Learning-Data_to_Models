import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(trainll, testll):

    trainData = readFile(trainll)
    testData  = readFile(testll)

    # plot 
    plt.title("Training and Testing likelihood")
    fig, ax = plt.subplots(figsize=(20, 15))
    plt.xticks([i * 100 for i in range(len(trainData))])
    # fig.suptitle("Throughput Chart\n\nExperiment parameters: page type, page size, workload mode")
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Likelihood')

    x = [i for i in range(1, len(trainData) + 1)]

    y = trainData
    plt.plot(x, y, "b-", lw=2.5)
    # y = testData
    # plt.plot(x, y, "b--", lw=2.5)

    plt.savefig(trainll.split(".")[0] + ".png")
    plt.clf()

def readFile(file):
    f = open(file, 'r')
    data = [float(d) for d in f.readlines()]
    f.close()

    return data

if __name__ == "__main__":
    trainll = 'collapsed-output-Q52.txt-trainll'
    testll  = 'collapsed-output-Q52.txt-testll'

    main(trainll, testll)
