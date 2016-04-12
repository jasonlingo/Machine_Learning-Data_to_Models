import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main(data, title, filename):

    data = map(readFile, data)
    print data

    # plot 
    # plt.title("Training and Testing likelihood")
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title(title, fontsize=20)

    plt.xticks([i * 10 for i in range(1, 6)])
    # fig.suptitle("Throughput Chart\n\nExperiment parameters: page type, page size, workload mode")
    ax.set_xlabel('Topic Size')
    ax.set_ylabel('Log Likelihood')


    x = [i * 10 for i in range(1, 6)]
    y = data
    index = np.arange(5)
    bar_width = 0.35
    rects1 = plt.bar(index+bar_width/2.0, data, bar_width,
                 alpha=0.8,
                 color='b'
                 )

    for i, d in enumerate(data):
        ax.text(i+bar_width, d, '%d' % d, ha='center', va='bottom', color='w')
    
    plt.xticks(index + bar_width, ('10', '20', '30', '40', '50'))




    # plt.plot(x, y, "b-", lw=2.5)
    # y = blockedData
    # plt.plot(x, y, "r-", lw=2.5)

    plt.savefig(filename)
    plt.clf()

def readFile(file):
    f = open(file, 'r')
    data = [float(d) for d in f.readlines()][-1]
    f.close()

    return data

if __name__ == "__main__":

    testll10  = 'submission/collapsed-output-Q5-4-10.txt-testll'
    testll20  = 'submission/collapsed-output-Q5-4-20.txt-testll'
    testll30  = 'submission/collapsed-output-Q5-4-30.txt-testll'
    testll40  = 'submission/collapsed-output-Q5-4-40.txt-testll'
    testll50  = 'submission/collapsed-output-Q5-4-50.txt-testll'
    data = [testll10, testll20, testll30, testll40, testll50]


    title = "Testing log likelihood for Collapsed-Gibbs sampler on different topic sizes\n(lambda, alpha, beta)=(0.5, 0.1, 0.01)"
    filename = "Q5-4-output.png"
    main(data, title, filename)


