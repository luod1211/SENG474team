import numpy as np
import csv

# This function extracts the data and ready them for calculation
# Parameter: The data in a array of lines
# return: The vector X and y (Values and labels)

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


# This function solves the normal equation in question1
# parameter: the preprocessed vectors X and y
# return: the vector W containing the coefficients
def normal(X, y):
    N = X.shape[0]
    # considering the extra dimension
    D = X.shape[1] - 1
    # ((X^T)X)^-1
    a = np.linalg.inv(np.matmul(np.transpose(X), X))
    # (X^T)y
    b = np.matmul(np.transpose(X), y.reshape(N, 1))
    # multiply together to get the final vector
    W = np.matmul(a, b)
    return W


def compute_loss(X, y, w):
    N = X.shape[0]
    y = y.reshape(N, 1)
    loss = (1 / (2 * N)) * (np.sum(np.power(y - np.matmul(X, w).reshape(N, 1), 2)))
    return loss


def main():
    # extract lines from the tsv file
    Lines = [line.rstrip('\n') for line in open('./data_100k_300.tsv')]
    X, y = preprocess(Lines)
    W = normal(X, y)
    names = []
    for w in range(len(W)-1):
        names.append('w' + str(w+1))
    names.append('w0')

    output = open('./PA2question1.tsv', "w")
    tsv_writer = csv.writer(output, delimiter='\t')
    tsv_writer.writerow(names)
    tsv_writer.writerow(W)



main()