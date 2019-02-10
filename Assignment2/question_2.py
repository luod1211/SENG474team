'''
Title: question_2.py
Date: February 10th, 2019
Authors: Luke Rowe, Luo Dai

This program performs batch gradient descent on a set
of 10000 data points each with 100 features. The loss is computed
and output to the console and the final parameter values w are \
written to a tsv file, question_2_output.tsv
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
This function performs batch gradient descent with 200 epochs

param(s): X: size Nx(D+1) numpy matrix: matrix containing feature values for all N samples
          y: size N numpy array: array of labels
          w: size D+1 nump array: array of parameters
ret: w: size D+1 numpy array: array of updated parameters
'''
def batch_gradient_descent(X,y):
    N = X.shape[0]
    D = X.shape[1] - 1
    #initialize w to D+1 random floats between 0 and 1
    w = np.random.random_sample(D+1)
    learning_rate = 0.000001

    #T = 200 epochs
    for T in range(200):
        #update w element-wise
        for j in range(D+1):
            #vector of predicted scores
            y_pred = (np.matmul(X,w)).reshape(N,1)
            y = y.reshape(N,1)

            #compute gradient and adjust parameters
            grad = (1/float(N)) * np.sum((y - y_pred).reshape(N,1) * X[:,j].reshape(N,1))
            w[j] = w[j] + (learning_rate)*(grad)
        print(T) # TAKE OUT LATER

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

def main():
    f = open('./data_10k_100.tsv', encoding='utf8')
    output = open('./question_2_output', "w")

    #extract the lines of the tsv file and remove the end '\n'
    lines = [line.rstrip('\n') for line in f]

    #extract data into numpy arrays
    X,y = preprocess(lines)

    w = batch_gradient_descent(X,y)
    loss = compute_loss(X,y,w)
    print("Loss: ", loss)

    D = w.shape[0] - 1

    # output to tsv file
    for i in range(D):
        output.write("w{}".format(i+1) + '\t')
    output.write("w0\n")

    for i in range(D+1):
        output.write(str(w[i]) + "\t")

    f.close()
    output.close()

if __name__ == "__main__":
    main()