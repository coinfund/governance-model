#!/usr/bin/env python

import numpy as np
import itertools
import sys
import math

"""
hat will filp a binary digit
"""
def hat(v):
    return v % 2


class Vote():

    def __init__(self, distro, vote, majority):
        self.distro = np.array(distro) / np.sum(distro)
        self.vote = np.array(vote)
        self.majority = majority
    
    def outcome(self):
        return np.dot(self.distro, self.vote)

    def is_decisive(self, j):
        outcome1 = self.outcome()
        self.vote[j] = (self.vote[j]+1) % 2
        outcome2 = Vote(self.distro, self.vote, self.majority).outcome()
        return (outcome1 > self.majority and outcome2 <= self.majority) or (outcome1 <= self.majority and outcome2 > self.majority)



def get_decisiveness(distro, majority, j):
    length = len(distro)
    memo = {}
    memo[0] = 0.0
    memo[1] = distro[0]

    def bit_not(n):
        return (1 << n.bit_length()) - 1 - n

    def get_vote(vote):
        if vote in memo:
            # print('returning memo: ', vote, memo[vote])
            return memo[vote]
        else:
            places = vote.bit_length()
            prev = vote & (2**(places - 1) - 1)
            # print(vote, places, prev)
            result = get_vote(prev) + distro[places - 1]
            memo[vote] = result
            # print('calculating memo: ', vote, memo[vote])
            return result

    def is_decisive(vote, j):
        # set j-th bit to 0
        j_zero = (2**(vote.bit_length())-1) ^ (1 << j)
        vote1 = vote & j_zero
        # print('vote1: ', vote1)
        result1 = get_vote(vote1)
        vote2 = vote | bit_not(j_zero)
        # print('vote2: ', vote2)
        result2 = get_vote(vote2)
        should_stop = (result1 > majority)
        return (((result1 <= majority) and (result2 > majority)), should_stop)
        
    count = 0
    vote = 0
    while vote < 2**length:
       
       decisive, stop = is_decisive(vote, j)
       # print(decisive, stop)
       if decisive:
           count += 1
       if stop: 
           break
       vote += 1
       
    
    return float(count) / float(2**length)


def model(distro, majority):
    l = len(distro)
    for i in range(0, 52, 1):
        pct = float(i) / 100.0
        s = [a - (pct / float(l)) for a in distro]
        s = np.append(pct, s)   
        print("%s,%s" % (s[0], get_decisiveness(s, majority, 0)))


if __name__ == '__main__':
    d = [float(a) for a in sys.argv[1:]]
    m = 0.50

    model(d, m)
    # print("distribution: ", np.array(d) / np.sum(d))    
    # print("decisiveness: ", decisiveness(d, m))