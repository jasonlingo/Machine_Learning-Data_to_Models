import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(collapsed, blocked, title, filename):

    collapsedData = readFile(collapsed)
    blockedData  = readFile(blocked)

    # plot 
    # plt.title("Training and Testing likelihood")
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_title(title, fontsize=20)
    plt.xticks([i * 100 for i in range(len(collapsedData))])
    # fig.suptitle("Throughput Chart\n\nExperiment parameters: page type, page size, workload mode")
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Log Likelihood')

    x = [i for i in range(1, len(collapsedData) + 1)]

    y = collapsedData
    plt.plot(x, y, "b-", lw=2.5)
    y = blockedData
    plt.plot(x, y, "r-", lw=2.5)

    plt.savefig(filename)
    plt.clf()

def readFile(file):
    f = open(file, 'r')
    data = [float(d) for d in f.readlines()]
    f.close()

    return data

if __name__ == "__main__":
    trainll = 'submission/collapsed-output-5-0.5-0.1.txt-trainll'
    testll  = 'submission/blocked-output-5-0.5-0.1.txt-trainll'
    title = "Training log likelihood for Collapsed and blocked-collapsed Gibbs samplers\n(Topic, lambda, alpha, beta)=(5, 0.5, 0.1, 0.01)"
    filename = "Q5-2-output-5-0.5-0.1.png"
    main(trainll, testll, title, filename)

    trainll = 'submission/collapsed-output-5-0.8-0.1.txt-trainll'
    testll  = 'submission/blocked-output-5-0.8-0.1.txt-trainll'
    title = "Training log likelihood for Collapsed and blocked-collapsed Gibbs samplers\n(Topic, lambda, alpha, beta)=(5, 0.8, 0.1, 0.01)"
    filename = "Q5-2-output-5-0.8-0.1.png"
    main(trainll, testll, title, filename)

    trainll = 'submission/collapsed-output-25-0.5-0.1.txt-trainll'
    testll  = 'submission/blocked-output-25-0.5-0.1.txt-trainll'
    title = "Training log likelihood for Collapsed and blocked-collapsed Gibbs samplers\n(Topic, lambda, alpha, beta)=(25, 0.5, 0.1, 0.01)"
    filename = "Q5-2-output-25-0.5-0.1.png"
    main(trainll, testll, title, filename)

    trainll = 'submission/collapsed-output-25-0.2-0.1.txt-trainll'
    testll  = 'submission/blocked-output-25-0.2-0.1.txt-trainll'
    title = "Training log likelihood for Collapsed and blocked-collapsed Gibbs samplers\n(Topic, lambda, alpha, beta)=(25, 0.2, 0.1, 0.01)"
    filename = "Q5-2-output-25-0.2-0.1.png"
    main(trainll, testll, title, filename)        

    trainll = 'submission/collapsed-output-25-0.5-1.0.txt-trainll'
    testll  = 'submission/blocked-output-25-0.5-1.0.txt-trainll'
    title = "Training log likelihood for Collapsed and blocked-collapsed Gibbs samplers\n(Topic, lambda, alpha, beta)=(25, 0.5, 1.0, 0.01)"
    filename = "Q5-2-output-25-0.5-1.0.png"
    main(trainll, testll, title, filename)  

