'''
Title: question1.py
Authors: Luke Rowe, Luo Dai
Date: Monday, March 25, 2019

This program factors a utility matrix into two matrices U and V.
'''

import numpy as np
import time

def preprocess(lines,N):

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

    print("Number of users:", len(find_user_id.keys()), len(find_user_idx.keys()))
    print("Numbers of movies:", len(find_movie_id.keys()), len(find_movie_idx.keys()))

    return find_user_id,find_user_idx, find_movie_id, find_movie_idx, users_list


def main():
    f = open("./u.data", "r")
    outputU = open("./UT.tsv", "w")
    outputV = open("./VT.tsv", "w")
    # list of lines of the u.data input file
    lines = [line.rstrip('\n') for line in f]

    N = 943
    M = 1682
    D = 20

    find_user_id, find_user_idx, find_movie_id, find_movie_idx, users_list = preprocess(lines, N)

    f.close()
    outputU.close()
    outputV.close()

if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(time.perf_counter() - t0)