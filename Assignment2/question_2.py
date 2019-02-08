import numpy as np

def batch_gradient_descent(X,y):
    print("Hello Earth")

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

        #alternative method, but less "Pythonic"
        #feat_num = 0
        #for feat in no_tab[1:]:
        #    X[tr_num,feat_num] = float(feat)
        #    feat_num +=1
        #X[tr_num,feat_num] = 1

        data_num += 1

    X.astype(float)
    y.astype(float)

    return (X,y)





def main():
    f = open('./data_10k_100.tsv', encoding='utf8')
    output = open('./question_2_output', "w")

    #extract the lines of the tsv file and remove the end '\n'
    lines = [line.rstrip('\n') for line in f]

    #extract data into numpy arrays
    (X,y) = preprocess(lines)

    w = batch_gradient_descent(X,y)



    f.close()
    output.close()

if __name__ == "__main__":
    main()