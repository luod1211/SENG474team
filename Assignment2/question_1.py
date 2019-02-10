'''
Title: question_2.py
Date: February 10th, 2019
Authors: Luke Rowe, Luo Dai
Version: Final

This program trains a linear classifier using the normal equation method on a set
of 100000 data points each with 300 features. The loss is computed
and output to the console and the final parameter values w are
written to a tsv file, question_1_output.tsv
'''

import numpy as np

'''
This function extracts the data from the lines of the tsv file and stores the data in numpy arrays

param(s): lines: list: list of lines(strings) from the tsv files
ret: X: size Nx(D+1) numpy matrix: matrix containing feature values for all N samples
     y: size N numpy array: array of labels 
'''
def preprocess(lines):
    #number of data points
    N = int(lines[0])
    #number of features for each data point
    D = int(lines[1])

    X = np.zeros((N,D+1))
    y = np.zeros(N)

    data_num = 0
    # start from 4th line as the 4th line is the first line that contains feature data
    for line in lines[3:]:
        no_tab = line.split('\t')
        y[data_num] = no_tab[0]

        #append 1 to last dimension
        no_tab.append(1)
        feat = no_tab[1:]
        X[data_num] = np.asarray(feat)

        data_num += 1

    # ensure that the array values have type float
    X.astype(float)
    y.astype(float)

    return X,y


'''
This function solves the normal equation for the parameter values W

param(s): X: size Nx(D+1) numpy matrix: matrix containing feature values for all N samples
          y: size N numpy array: array of labels
ret: W: size (D+1) numpy array: the vector containing the coefficients
'''
def normal(X, y):
    N = X.shape[0]

    # ((X^T)X)^-1
    a = np.linalg.inv(np.matmul(np.transpose(X), X))
    # (X^T)y
    b = np.matmul(np.transpose(X), y)
    # multiply together to get the final vector
    W = np.matmul(a, b)

    W.astype(float)
    return W

'''
This function computes the loss using the parameters w inputted into the function

param(s): X: size Nx(D+1) numpy matrix: matrix containing feature values for all N samples
          y: size N numpy array: array of labels
          w: size D+1 numpy array: array of parameters
ret: loss: float: computed loss value
'''
def compute_loss(X,y,w):
    N = X.shape[0]
    y = y.reshape(N,1)
    loss = (1/(2*float(N))) * (np.sum(np.power(y - np.matmul(X,w).reshape(N,1),2)))
    return loss

def main():
    # extract lines from the tsv file
    f = open('./data_100k_300.tsv', encoding='utf8')
    output = open('./question_1_output.tsv', "w")

    #extract the lines of the tsv file and remove the end '\n'
    lines = [line.rstrip('\n') for line in f]

    X,y = preprocess(lines)
    W = normal(X, y)

    loss = compute_loss(X,y,W)
    print("Loss: ", loss)

    # write final parameter results to a tsv file
    D = W.shape[0] - 1

    # output to tsv file
    for i in range(D):
        output.write("w{}".format(i + 1) + '\t')
    output.write("w0\n")

    for i in range(D + 1):
        output.write(str(W[i]) + "\t")

    f.close()
    output.close()

if __name__ == "__main__":
    main()