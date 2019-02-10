'''
Title: question_3a.py
Date: February 10th, 2019
Authors: Luke Rowe, Luo Dai
Version: Final

This program performs stochastic gradient descent on a set
of 10000 data points each with 100 features. The loss is computed
and output to the console and the final parameter values w are
written to a tsv file, question_3a_output.tsv
'''
import numpy as np

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

'''
This function performs stochastic gradient descent with 20 epochs

param(s): X: size Nx(D+1) numpy matrix: matrix containing feature values for all N samples
          y: size N numpy array: array of labels
ret: w: size D+1 numpy array: array of updated parameters
'''
def sto_gradient_descent(X,y):
    N = X.shape[0]
    D = X.shape[1] - 1
    w = np.random.random_sample(D+1)
    learning_rate = 0.000001

    # vector of predicted scores
    y_pred = (np.matmul(X, w)).reshape(N, 1)
    y = y.reshape(N, 1)

    #T = 20 epochs
    for T in range(20):
        for i in range(N):
            # update vector of predicted scores
            y_pred[i] = np.matmul(X[i,:].reshape(1,D+1),w)

            #compute gradient and adjust parameters
            #broadcasting so that all dimensions of w computed at the same time
            #since m = 1 we only update w using one data point
            grad = ((y[i] - y_pred[i]) * X[i,:])
            w = w + (learning_rate)*(grad)

    return w

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
    for line in lines[3:]:
        no_tab = line.split('\t')
        y[data_num] = no_tab[0]

        #append 1 to last dimension
        no_tab.append(1)
        feat = no_tab[1:]
        X[data_num] = np.asarray(feat)

        data_num += 1

    X.astype(float)
    y.astype(float)

    return X,y

def main():
    f = open('./data_10k_100.tsv', encoding='utf8')
    output = open('./question_3a_output.tsv', "w")

    #extract the lines of the tsv file and remove the end '\n'
    lines = [line.rstrip('\n') for line in f]

    #extract data into numpy arrays
    X,y = preprocess(lines)
    w = sto_gradient_descent(X,y)
    loss = compute_loss(X,y,w)
    print("Loss: ", loss)

    D = w.shape[0] - 1

    #write parameter results to tsv file
    for i in range(D):
        output.write("w{}".format(i+1) + '\t')
    output.write("w0\n")

    for i in range(D+1):
        output.write(str(w[i]) + "\t")

    f.close()
    output.close()

if __name__ == "__main__":
    main()