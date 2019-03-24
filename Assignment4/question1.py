'''
Title: question1.py
Authors: Luke Rowe, Luo Dai
Date: Monday, March 25, 2019

This program factors a utility matrix into two matrices U and V.
'''

import numpy as np
import time
import math

'''
This function takes the lines from the input file, and reindexes the 
user_id and movie_id from 0 to N-1 and 0 to M-1, respectively. Then,
the movies rated for each user are put into a users_list array and 
the users that rate each movie into the movies_list array

param(s): lines: list: list of lines(strings) from the .data file
          N: int: number of users
          M: int: number of movies
ret: find_user_idx: dict: dictionary that maps a userid to an array index from 0 to N-1
     find_movie_idx: dict: dictionary that maps a movieid to an array index from 0 to M-1
     find_user_id: dict: dictionary that maps a array index to a user_id
     find_movie_id: dict: dictionary that maps an array index to a movie_id
     users_list: list: list indexed by user which contains dictionary of the movies and 
                      ratings that each user rated
     movies_list: list: indexed by movie which contains dictionary of the users and their
                       rating for each movie
'''
def preprocess(lines,N, M):
    # reindex the user_ids from 0 to n-1. The key is the user_id
    find_user_idx = {}
    # reindex the movie_ids from 0 to m-1. The key is the movie_id
    find_movie_idx = {}
    # reindex the user_ids from 0 to n-1. The key is the idx
    find_user_id = {}
    # reindex the movie_ids from 0 to m-1. The key is the idx
    find_movie_id = {}

    # for each user we have a dictionary storing the users' movies and
    # associated ratings
    users_list = [dict() for x in range(N)]

    # for each movie we have a dictionary storing users that rated the movie, along with the rating
    movies_list = [dict() for x in range(M)]

    user_counter = 0
    movie_counter = 0
    for line in lines:
        if len(line.split('\t')) == 4:
            (user_id, movie_id, rating, _) = tuple(map(int, line.split('\t')))

            #only assign new user index if user_id has not been assigned before
            if user_id not in find_user_idx.keys():
                find_user_id[user_counter] = user_id
                find_user_idx[user_id] = user_counter
                user_counter += 1

            if movie_id not in find_movie_idx.keys():
                find_movie_id[movie_counter] = movie_id
                find_movie_idx[movie_id] = movie_counter
                movie_counter += 1

            users_list[find_user_idx[user_id]][find_movie_idx[movie_id]] = rating
            movies_list[find_movie_idx[movie_id]][find_user_idx[user_id]] = rating

    return find_user_idx, find_movie_idx, find_user_id, find_movie_id, users_list, movies_list

'''
This function performs UV decomposition for 20 epochs on randomly initialized matrices U and V

param(s): users_list: list: list indexed by user which contains dictionary of the movies and 
                      ratings that each user rated
          movies_list: list: indexed by movie which contains dictionary of the users and their
                       rating for each movie
          N: int: number of users
          M: int: number of movies
          D: int: number of columns of U (and hence, number of rows of V)
return: U: ndarray (size NxD): U matrix after UV-decomposition
        V: ndarray (size DxM): V matrix after UV-decomposition 
'''
def uv_decomp(users_list, movies_list, N, M, D):

    U = np.random.random_sample([N,D])
    V = np.random.random_sample([D,M])

    for T in range(20):
        print("Epoch:", T)
        for k in range(D):
            # we will replace the k-th column of U with X
            X = np.zeros(N)
            for i in range(N):
                num = 0
                denom = 0
                for j in users_list[i].keys():
                    num += (np.dot(U[i,:], V[:,j]) - U[i,k]*V[k,j] - users_list[i][j]) * V[k,j]
                    denom += V[k,j] ** 2

                X[i] = -1 * (num/denom)

            U[:,k] = X

        for k in range(D):
            # we will replace the k-th column of V with Y
            Y = np.zeros(M)
            for j in range(M):
                num = 0
                denom = 0
                for i in movies_list[j].keys():
                    num += (np.dot(U[i,:], V[:,j]) - U[i,k]*V[k,j] - users_list[i][j]) * U[i,k]
                    denom += U[i,k] ** 2

                Y[j] = -1 * (num/denom)

            V[k,:] = Y

    return U, V

'''
This function computes the RMSE of the UV-decomposition.

param(s): U: ndarray (size NxD): U matrix in UV-decomposition
          V: ndarray (size DxM): V matrix in UV-decomposition
          users_list: list: list indexed by user which contains dictionary of the movies and 
                      ratings that each user rated
          N: int: number of users
return: rmse: float: the rmse of the UV-decomposition      
'''
def RMSE(U,V,users_list, N):
    num = 0
    denom = 0
    for i in range(N):
        for j in users_list[i].keys():
            num += (np.dot(U[i,:], V[:,j]) - users_list[i][j]) ** 2
            denom += 1

    rmse = math.sqrt(num/denom)

    return rmse

def main():
    f = open("./u.data", "r")
    outputU = open("./UT.tsv", "w")
    outputV = open("./VT.tsv", "w")
    # list of lines of the u.data input file
    lines = [line.rstrip('\n') for line in f]

    N = 943
    M = 1682
    D = 20

    find_user_idx, find_movie_idx, find_user_id, find_movie_id, users_list, movies_list = preprocess(lines, N, M)

    # find U and V using UV-decomposition
    U, V = uv_decomp(users_list, movies_list, N, M, D)

    # RMSE of the UV-decomposition
    print("RMSE:" , RMSE(U,V,users_list,N))

    #output to UT.tsv
    row = ''
    for i in range(N):
        for j in range(D):
            row = row + str(U[i,j]) + '\t'
        outputU.write(str(find_user_id[i]) + '\t' + row.rstrip('\t') + '\n')
        row = ''

    #output to VT.tsv
    row = ''
    for j in range(M):
        for i in range(D):
            row = row + str(V[i,j]) + '\t'
        outputV.write(str(find_movie_id[j]) + '\t' + row.rstrip('\t') + '\n')
        row = ''

    f.close()
    outputU.close()
    outputV.close()

if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print("Run time:", time.perf_counter() - t0)