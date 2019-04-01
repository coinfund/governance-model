# A relative value model for governance tokens

## Abstract

In blockchain networks, and more broadly in decentralized technology, tokens are often used to implement governance processes. So-called "governance tokens" are used to perform on-chain voting functions, allow or disallow protocol upgrades, and signal community sentiment around various network proposals. However, other than \[Bonello, 2018\], no quantitative valuation frameworks for governance tokens have been suggested. In this work, we describe a relative value model for governance tokens based on a concept called "decisiveness" of a particular token holder's stake relative to a token distribution. The idea of decisive stakes allows us to impose an ordering on token stakes and therefore value one stake versus another. This subsequently paves the way for valuation in absolute terms.

\[Bonello, 2018\] [A Framework for Valuing Governance Tokens: 0x](https://hackernoon.com/a-framework-for-valuing-governance-tokens-0x-49d2cf2ef5bc)

## Contents

1. A formal description of the model may be found [here](https://github.com/coinfund/governance-model/blob/master/Relative_Governance.pdf). 
2. A Python implementation of the model is found in the repository. The code was tested on Python 3.6.3+.
3. To run the model, try giving it a token distribution:

```
$ ./model.py 100 100 50 50
   tokens     stake  decisiveness
0   100.0  0.333333          0.50
1   100.0  0.333333          0.50
2    50.0  0.166667          0.25
3    50.0  0.166667          0.25
```

## Relative value of governance

In decentralized governance systems, governance is typically implemented as a voting system that considers proposals. Token holders with large stakes, known as "whales", exercise more influence over governance. In order to quantify the influence of a stake with respect to some token distribution, we would like to formalize the notion of a particular voter being able to "overturn the vote". 

We make the following assumptions, for simplicity:

1. There is a token distribution, which measures the number of participants and each of their relative stakes.
2. The quorum of either stake or participants required to pass a proposal is 0.
3. Voting is binary (yea and nea) instead of trinary (yea, nea, and abstain).
4. There is some majority threshold, *M*, which a proposal needs to achieve in voting in order to pass. (Typically *M* = .50.)

In our [formal description](https://github.com/coinfund/governance-model/blob/master/Relative_Governance.pdf), we formalize the notion of a "decisive stake" with respect to a token distribution and a vote. A decisive stake is one upon which the outcome of a particular vote hinges: if the voter doesn't participate, the proposal fails to pass; and otherwise, it passes.

Similarly, we formalize the notion of the "decisiveness" of a stake with respect to a token distribution. The decisiveness of a stake is a meaure of the expected percent of the time that the stake is decisive to a vote. By calculating decisiveness


So we have a natural mapping between the size of a stake and its "decisiveness", and this allows us to show that some stakes are worth more or less than others. The results are surprising!

## Example: Uniformly-distributed token distribution

```
$ ./model.py 100 100 100 100
   tokens  stake  decisiveness
0   100.0   0.25         0.375
1   100.0   0.25         0.375
2   100.0   0.25         0.375
3   100.0   0.25         0.375
```
