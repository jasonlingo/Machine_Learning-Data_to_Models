import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(trainll, testll, stamp, filename):
    print trainll, testll
    # parse data
    trainData = readFile(trainll)
    testData  = readFile(testll)

    # plot
    # plt.title("Training and Testing likelihood" + str(stamp))
    fig, ax1 = plt.subplots(figsize=(16, 12))
    title = "Training and Testing Log likelihood - " + str(stamp) + "\n(Topic, lambda, alpha, beta)=(25, 0.5, 0.1, 0.01)"
    ax1.set_title(title, fontsize=20)
    plt.xticks([i * 100 for i in range(len(trainData))])
    ax1.set_xlabel('Iteration')
    x = [i for i in range(1, len(trainData) + 1)]


    ax1.set_ylabel('Log Likelihood for training data', color='b')
    y = trainData
    ax1.plot(x, y, "b-", lw=2.5)
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Log Likelihood for testing data', color='r')
    y = testData
    ax2.plot(x, y, 'r-', label="Testing")
    for tl in ax2.get_yticklabels():
        tl.set_color('r')


    plt.savefig(filename)

    plt.clf()


    # ======


def readFile(file):
    f = open(file, 'r')
    data = [float(d) for d in f.readlines()]
    f.close()

    return data

if __name__ == "__main__":
    folder = "result"

    trainll = folder + '/collapsed-output-Q5-1-1.txt-trainll'
    testll  = folder + '/collapsed-output-Q5-1-1.txt-testll'
    filename = "Q5-1-1.png"
    main(trainll, testll, 1, filename)

    trainll = folder + '/collapsed-output-Q5-1-2.txt-trainll'
    testll  = folder + '/collapsed-output-Q5-1-2.txt-testll'
    filename = "Q5-1-2.png"
    main(trainll, testll, 2, filename)

    trainll = folder + '/collapsed-output-Q5-1-3.txt-trainll'
    testll  = folder + '/collapsed-output-Q5-1-3.txt-testll'
    filename = "Q5-1-3.png"
    main(trainll, testll, 3, filename)    