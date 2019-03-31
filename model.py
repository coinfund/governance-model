#!/usr/bin/env python

import numpy as np
import itertools
import sys
import math
import pandas as pd

"""
bit_not is a binary not operation.
"""
def bit_not(n, bit_length):
    return (1 << bit_length) - 1 - n

"""
Given a normalized token distribution, distro, and a
majority threshold, majority (0 <= majority <= .50),
and an index j (0 <= j < len(distro)), this method
will calculate the decisiveness of the j-th token holder.
"""
def get_decisiveness(distro, majority, j, memo = {}, verbose=False):
    length = len(distro)
    bit_length = length
    memo[0] = 0.0
    memo[1] = distro[0]

    """
    Returns the amount of stake that voted yea given
    a particular vote outcome. The vote is an integer
    whose binary representation is interpreted as yea
    or nea votes of individual token holders, with 1
    being interpreted as yea votes.
    """
    def get_vote(vote):
        if vote in memo:
            return memo[vote]
        else:
            places = vote.bit_length()
            prev = vote & (2**(places - 1) - 1)
            result = get_vote(prev) + distro[places - 1]
            memo[vote] = result
            return result

    """
    is_decisive returns True if and only if the j-th token holder
    is decisive in the vote.
    """
    def is_decisive(vote, j):
        # set j-th bit to 0
        j_zero = (2**(bit_length)-1) ^ (1 << j)
        vote1 = vote & j_zero
        result1 = get_vote(vote1)
     

        # true if and only if the j-th token holder overturns
        # the vote
        return ((result1 <= majority) and (result1 > majority - distro[j]))
        
    count = 0
    vote = 0
    while vote < 2**length:
      decisive = is_decisive(vote, j)
      if decisive:
        if verbose:
            print('vote: %s *' % bin(vote))
        count += 1
      else:
        if verbose:
            print('vote: %s' % bin(vote))
      vote += 1
    
    return float(count) / float(2**length)

if __name__ == '__main__':
    args = [float(a) for a in sys.argv[1:]]
    distro = np.array(args) / np.sum(args)
    majority = 0.50
    memo = {}

    df = pd.DataFrame(columns=['tokens', 'stake', 'decisiveness'])
    df['tokens'] = args
    df['stake'] = distro
    df['decisiveness'] = [get_decisiveness(distro, majority, j, memo) for j in range(0, len(distro))]
    
    print(df) 