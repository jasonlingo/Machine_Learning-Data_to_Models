import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math


def main(collapsed, blocked, collTime, blockTime, title, filename):

    collapsedData = readFile(collapsed)
    blockedData  = readFile(blocked)
    collTime = readFile(collTime)
    blockTime = readFile(blockTime)

    # plot 
    # plt.title("Training and Testing likelihood")
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_title(title, fontsize=20)
    # plt.xticks([i * 100 for i in range(len(collapsedData))])
    # fig.suptitle("Throughput Chart\n\nExperiment parameters: page type, page size, workload mode")
    ax.set_xlabel('Runtime (millisecond)')
    ax.set_ylabel('Log Likelihood')

    maxX = int(math.ceil(max(blockTime[-1], collTime[-1])) / 1000) * 1000


    # x = [i for i in range(1, len(collapsedData) + 1)]

    plt.plot(collTime, collapsedData, "b-", lw=2.5)
    plt.plot(blockTime, blockedData, "r-", lw=2.5)

    plt.savefig(filename)
    plt.clf()

def readFile(file):
    f = open(file, 'r')
    data = [float(d) for d in f.readlines()]
    f.close()

    return data

if __name__ == "__main__":
    block = 'submission/timed-block-output-Q5-3-25-0.5-0.1.txt-trainll'
    blockTime = 'submission/timed-collapsed-output-Q5-3-25-0.5-0.1.txt-time'
    coll  = 'submission/timed-collapsed-output-Q5-3-25-0.5-0.1.txt-trainll'
    collTime = 'submission/timed-block-output-Q5-3-25-0.5-0.1.txt-time'
    title = "Training log likelihood for Collapsed and blocked-collapsed Gibbs samplers for different runtime\n(Topic, lambda, alpha, beta)=(25, 0.5, 0.1, 0.01)"
    filename = "Q5-3-output.png"
    main(coll, block, collTime, blockTime, title, filename)




