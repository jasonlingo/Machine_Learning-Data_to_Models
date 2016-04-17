


def compare(filea, fileb, filec):

    dataA = parseData(filea)
    dataB = parseData(fileb)
    dataC = parseData(filec)

    for i in range(len(dataA)):
        print "Topic " + str(i) + " ----------"
        sa = dataA[i]
        sb = dataB[i]
        sc = dataC[i]

        print sa.intersection(sb).intersection(sc)


def parseData(file):
    f = open(file, 'r')

    data = []
    for line in f.readlines():
        if line == '\n':
            data.append(set())
        elif 'Topic' in line:
            continue
        else:
            data[-1].add(line.strip().split()[0])

    return data




if __name__=="__main__":
    file = 'col_alpha_0.001_'
    file0 = 'col_alpha_0.001_0'
    file1 = 'col_alpha_0.001_1'

    file = 'col_alpha_10_'
    file0 = 'col_alpha_10_0'
    file1 = 'col_alpha_10_1'

    # file = 'col_beta_0.001_'
    # file0 = 'col_beta_0.001_0'
    # file1 = 'col_beta_0.001_1'

    # file = 'col_beta_10_'
    # file0 = 'col_beta_10_0'
    # file1 = 'col_beta_10_1'

    compare(file, file0, file1)