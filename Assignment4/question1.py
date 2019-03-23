'''
Title: question1.py
Authors: Luke Rowe, Luo Dai
Date: Monday, March 25, 2019

This program factors a utility matrix into two matrices U and V.
'''

import numpy as np
import time
import math

def preprocess(lines,N, M):

    # reindex the user_ids from 0 to n-1. The key is the idx
    find_user_id = {}
    # reindex the user_ids from 0 to n-1. The key is the user_id
    find_user_idx = {}
    # reindex the movie_ids from 0 to m-1. The key is the idx
    find_movie_id = {}
    # reindex the movie_ids from 0 to m-1. The key is the movie_id
    find_movie_idx = {}

    # for each user we have a dictionary storing the users' movies and
    # associated ratings
    users_list = [dict() for x in range(N)]

    movies_list = [dict() for x in range(M)]

    user_counter = 0
    movie_counter = 0
    for line in lines:
        if len(line.split('\t')) == 4:
            (user_id, movie_id, rating, _) = tuple(map(int, line.split('\t')))

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

    return find_user_id,find_user_idx, find_movie_id, find_movie_idx, users_list, movies_list

def uv_decomp(users_list, movies_list, N, M, D):

    U = np.random.random_sample([N,D])
    V = np.random.random_sample([D,M])

    for T in range(20):
        print(T)
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
            # we will replace the k-th column of U with X
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

def RMSE(U,V,users_list, N):
    num = 0
    denom = 0
    for i in range(N):
        for j in users_list[i].keys():
            num += (np.dot(U[i,:], V[:,j]) - users_list[i][j]) ** 2
            denom += 1

    rmse = math.sqrt(num) / denom

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

    find_user_id, find_user_idx, find_movie_id, find_movie_idx, users_list, movies_list = preprocess(lines, N, M)

    # find U and V using UV-decomposition
    U, V = uv_decomp(users_list, movies_list, N, M, D)

    # RMSE of the UV-decomposition
    print(RMSE(U,V,users_list,N))

    row = ''
    for i in range(N):
        for j in range(D):
            row = row + str(U[i,j]) + '\t'
        outputU.write(row.rstrip('\t') + '\n')
        row = ''

    row = ''
    for i in range(D):
        for j in range(M):
            row = row + str(V[i,j]) + '\t'
        outputV.write(row.rstrip('\t') + '\n')
        row = ''

    f.close()
    outputU.close()
    outputV.close()

if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print("Run time:", time.perf_counter() - t0)