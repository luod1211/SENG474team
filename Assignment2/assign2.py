import numpy as np


def preprocess(lines):
    # number of data points
    N = int(lines[0])
    # number of features for each data point
    D = int(lines[1])

    X = np.zeros((N, D + 1))
    y = np.zeros(N)

    data_num = 0
    for line in lines[3:]:
        no_tab = line.split('\t')
        y[data_num] = no_tab[0]

        # append 1 to last dimension
        no_tab.append(1)
        feat = no_tab[1:]
        X[data_num] = np.asarray(feat)

        # alternative method, but less "Pythonic"
        # feat_num = 0
        # for feat in no_tab[1:]:
        #    X[tr_num,feat_num] = float(feat)
        #    feat_num +=1
        # X[tr_num,feat_num] = 1

        data_num += 1

    X.astype(float)
    y.astype(float)

    return X, y


# ()((X^T)X)^-1)(X^T)Y
def quest1((X, y)):
    N = X.shape[0]
    D = X.shape[1] - 1
    a = np.linalg.inv(np.matmul(np.transpose(X), X))
    b = np.matmul(np.transpose(X), y.reshape(N, 1))
    W = np.matmul(a, b)
    return W


def compute_loss(X, y, w):
    N = X.shape[0]
    y = y.reshape(N, 1)
    loss = (1 / (2 * float(N))) * (np.sum(np.power(y - np.matmul(X, w).reshape(N, 1), 2)))
    print(np.sum(np.power(y - np.matmul(X, w).reshape(N, 1), 2)))
    return loss


def main():
    info = [line.rstrip('\n') for line in open('./data_100k_300.tsv')]
    X, y = preprocess(info)
    W = quest1((X, y))
    print(compute_loss(X, y, W))


main()
