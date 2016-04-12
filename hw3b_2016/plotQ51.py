import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(trainll, testll, stamp):
    print trainll, testll
    # parse data
    trainData = readFile(trainll)
    testData  = readFile(testll)

    # plot
    # plt.title("Training and Testing likelihood" + str(stamp))
    fig, ax1 = plt.subplots(figsize=(16, 12))
    ax1.set_title("Training and Testing Log likelihood - " + str(stamp), fontsize=20)
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
    ax2.plot(x, y, 'r-')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')

    plt.savefig(trainll.split(".")[0] + ".png")

    plt.clf()


    # ======
    # plt.title("Training and Testing likelihood")
    # fig, ax1 = plt.subplots()
    # t = np.arange(0.01, 10.0, 0.01)
    # s1 = np.exp(t)
    # ax1.plot(t, s1, 'b-')
    # ax1.set_xlabel('Iteration')
    # # Make the y-axis label and tick labels match the line color.
    # ax1.set_ylabel('exp', color='b')
    # for tl in ax1.get_yticklabels():
    #     tl.set_color('b')


    # ax2 = ax1.twinx()
    # s2 = np.sin(2*np.pi*t)
    # ax2.plot(t, s2, 'r.')
    # ax2.set_ylabel('sin', color='r')
    # for tl in ax2.get_yticklabels():
    #     tl.set_color('r')
    # plt.show()

def readFile(file):
    f = open(file, 'r')
    data = [float(d) for d in f.readlines()]
    f.close()

    return data

if __name__ == "__main__":
    trainll = 'submission/collapsed-output-Q5-1-1.txt-trainll'
    testll  = 'submission/collapsed-output-Q5-1-1.txt-testll'
    main(trainll, testll, 1)

    trainll = 'submission/collapsed-output-Q5-1-2.txt-trainll'
    testll  = 'submission/collapsed-output-Q5-1-2.txt-testll'
    main(trainll, testll, 2)

    trainll = 'submission/collapsed-output-Q5-1-3.txt-trainll'
    testll  = 'submission/collapsed-output-Q5-1-3.txt-testll'
    main(trainll, testll, 3)    