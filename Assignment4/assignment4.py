import numpy as np


def build(lines):
    rates = []
    users = {}
    movies = {}
    usercount = 0
    moviecount = 0
    for line in lines:
        if (int(line.split('\t')[0]) not in users.keys()):
            users[int(line.split('\t')[0])]=usercount
            usercount = usercount + 1
        if (int(line.split('\t')[1]) not in movies.keys()):
            movies[int(line.split('\t')[1])]=moviecount
            moviecount = moviecount + 1

        rates.append([int(line.split('\t')[0]), int(line.split('\t')[1]), int(line.split('\t')[2])])

    m = np.zeros((len(users), len(movies)))

    for rate in rates:
        m.itemset((users[rate[0]], movies[rate[1]]), rate[2])
    
    return m, users, movies, rates


def main():
    lines = [line.rstrip('\n') for line in open('./u.data')]
    m ,users, movies, rates = build(lines)
    u = np.random.randint(2, size=(len(users),len(movies)-1))
    v = np.random.randint(2, size=(len(users)-1,len(movies)))
    

main()
    