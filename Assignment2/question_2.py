import numpy as np


def compute_loss(X,y,w):
    N = X.shape[0]
    y = y.reshape(N,1)
    loss = (1/(2*N)) * (np.sum(np.power(y - np.matmul(X,w).reshape(N,1),2)))
    return loss


def batch_gradient_descent(X,y):
    N = X.shape[0]
    D = X.shape[1] - 1
    w = np.random.random_sample(D+1)
    learning_rate = 0.000001

    #T = 200 epochs
    for T in range(200):
        for j in range(D+1):
            #vector of predicted scores
            y_pred = (np.matmul(X,w)).reshape(N,1)
            y = y.reshape(N,1)

            #compute gradient and adjust parameters
            grad = (1/N) * np.sum((y - y_pred).reshape(N,1) * X[:,j].reshape(N,1))
            w[j] = w[j] + (learning_rate)*(grad)
        print(T)

    return w

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
    output = open('./question_2_output', "w")

    #extract the lines of the tsv file and remove the end '\n'
    lines = [line.rstrip('\n') for line in f]

    #extract data into numpy arrays
    X,y = preprocess(lines)
    w = batch_gradient_descent(X,y)
    loss = compute_loss(X,y,w)
    print("Loss: ", loss)

    

    f.close()
    output.close()

if __name__ == "__main__":
    main()