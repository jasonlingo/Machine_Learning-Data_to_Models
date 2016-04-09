import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(collapsed, blocked):

    collapsedData = readFile(collapsed)
    blockedData  = readFile(blocked)

    # plot 
    plt.title("Training and Testing likelihood")
    fig, ax = plt.subplots(figsize=(20, 15))
    plt.xticks([i * 100 for i in range(len(collapsedData))])
    # fig.suptitle("Throughput Chart\n\nExperiment parameters: page type, page size, workload mode")
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Likelihood')

    x = [i for i in range(1, len(collapsedData) + 1)]

    y = collapsedData
    plt.plot(x, y, "b-", lw=2.5)
    y = blockedData
    plt.plot(x, y, "r-", lw=2.5)

    plt.savefig("collapsed-blocked-25-0.5-0.1.png")
    plt.clf()

def readFile(file):
    f = open(file, 'r')
    data = [float(d) for d in f.readlines()]
    f.close()

    return data

if __name__ == "__main__":
    trainll = 'collapsed-output-25-0.5-0.1.txt-trainll'
    testll  = 'blocked-output-25-0.5-0.1.txt-trainll'

    main(trainll, testll)
