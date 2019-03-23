'''
Title: question1.py
Authors: Luke Rowe, Luo Dai
Date: Monday, March 25, 2019

This program factors a utility matrix into two matrices U and V.
'''

import numpy as np
import time


def preprocess(lines):

    # reindex the user_ids from 0 to n-1
    users_idx = {}
    # reindex the nove_ids from 0 to m-1
    movies_idx = {}
    # for each user we have a dictionary storing the users' movies and
    # associated ratings
    users_list = []

    user_counter = 0
    movie_counter = 0
    counter = 0
    for line in lines:
        if len(line.split('\t')) == 4:
            (user_id, movie_id, rating, _) = tuple(map(int, line.split('\t')))
            if user_id not in users_idx.values():
                users_idx[user_counter] = user_id
                user_counter += 1

            if movie_id not in movies_idx.values():
                movies_idx[movie_counter] = movie_id
                movie_counter += 1

        if counter % 10000 == 0:
            print(counter)

        counter += 1

    print("Number of users:", user_counter)
    print("Numbers of movies:", movie_counter)


    return users_idx, movies_idx, users_list


def main():
    f = open("./u.data", "r")
    outputU = open("./UT.tsv", "w")
    outputV = open("./VT.tsv", "w")
    # list of lines of the u.data input file
    lines = [line.rstrip('\n') for line in f]



    preprocess(lines)

    f.close()
    outputU.close()
    outputV.close()

if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(time.perf_counter() - t0)