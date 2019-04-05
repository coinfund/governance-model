# A relative value model for governance tokens

Author: [Jake Brukhman](mailto:jake@coinfund.io), [CoinFund](http://coinfund.io)

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
3. Voting is binary (yea and nay) instead of trinary (yea, nay, and abstain). (However, the model herein is easily extensible to trinary voting or other schemes.)
4. There is some majority threshold, *M*, which a proposal needs to achieve in voting in order to pass. (Typically *M* = 50%.)

In our [formal description](https://github.com/coinfund/governance-model/blob/master/Relative_Governance.pdf), we formalize the notion of a "decisive stake" with respect to a token distribution and a vote. A decisive stake is one upon which the outcome of a particular vote hinges: if the voter doesn't participate, the proposal fails to pass; and otherwise, it passes.

Similarly, we formalize the notion of the "decisiveness" of a stake with respect to a token distribution. The decisiveness of a stake is a measure of the expected percent of the time that the stake is decisive to a vote. By calculating decisiveness, we are able to understand the relationship between the size of the stake and the influence that it can exert upon the outcomes of proposals. 

## Conclusions

1. Through our formalization and implementation, we demonstrate how the decisiveness metric might be computed.
2. We demonstrate that stake size and decisiveness are positively correlated, and in some cases result in an exponential relationship.
3. The relationship between stake size and decisiveness is similar to a step function and is not differentiable. Therefore, sometimes adding marginal stake to a position disproportionally increases its decisiveness.
4. Our work suggests that under certain distributions, small stakes have infinitessimally small or zero decisiveness, rendering them valueless. This presents challenges for the liquidity of governance tokens as then having positive price of individual tokens makes sense only in the context of an aggregate lot of tokens.

## Example: Uniform token distribution

In this basic example, we consider a governance system with four equal token holders possessing 100 tokens each. Each token holder then owns 25% of network stake, and the distribution is uniform. The decisiveness of each token holder is equal and is 37.5% -- meaning, that each token holder expects to be able to overturn 37.5% of possible voting scenarios.
```
$ ./model.py 100 100 100 100
   tokens  stake  decisiveness
0   100.0   0.25         0.375
1   100.0   0.25         0.375
2   100.0   0.25         0.375
3   100.0   0.25         0.375
```

## Example: Dictatorship scenario

In this scenario, we demonstrate the case that a token holder who holds more than the majority threshold (50%) worth of stake becomes the dictator of the system and is able to block or uphold proposals 100% of the time. In such a system, small token holders have literally lost all power in the system and their individual tokens are worthless.

```
$ ./model.py 10 1 1 1 1 1 1 1 1 1
   tokens     stake  decisiveness
0    10.0  0.526316           1.0
1     1.0  0.052632           0.0
2     1.0  0.052632           0.0
3     1.0  0.052632           0.0
4     1.0  0.052632           0.0
5     1.0  0.052632           0.0
6     1.0  0.052632           0.0
7     1.0  0.052632           0.0
8     1.0  0.052632           0.0
9     1.0  0.052632           0.0
```

Even when there is a group of token holders than can collectively outvote whales, their decisiveness is still infinitessimally small and the system closely approximates a dictatorship.

```
$ ./model.py 10 1 1 1 1 1 1 1 1 1 1 1
    tokens     stake  decisiveness
0     10.0  0.476190      0.999023
1      1.0  0.047619      0.000977
2      1.0  0.047619      0.000977
3      1.0  0.047619      0.000977
4      1.0  0.047619      0.000977
5      1.0  0.047619      0.000977
6      1.0  0.047619      0.000977
7      1.0  0.047619      0.000977
8      1.0  0.047619      0.000977
9      1.0  0.047619      0.000977
10     1.0  0.047619      0.000977
11     1.0  0.047619      0.000977
```

## Example: Marginal increases in stake

Marginal increases in stake can lead to dramatic increases in decisiveness. The following example shows one case where a uniform distribution is heavily skewed toward a particular token holder by a increase in her stake of a single token.

```
$ ./model.py 50 50 50 50
   tokens  stake  decisiveness
0    50.0   0.25         0.375
1    50.0   0.25         0.375
2    50.0   0.25         0.375
3    50.0   0.25         0.375

$ ./model.py 51 50 50 50
   tokens     stake  decisiveness
0    51.0  0.253731          0.75
1    50.0  0.248756          0.25
2    50.0  0.248756          0.25
3    50.0  0.248756          0.25
```

## Example: Decisiveness as a function of stake

In the following examples, we take uniform token distributions on 3, 4, 10, and 25 token holders and we show what happens when a marginal token holder begins to accumulate stake and uniformly dilute the others. The result is an approximation of an exponential function, where the decisiveness of the accumulating token holder grows as a function of her stake.

### n = 3

![](https://i.imgur.com/6lLRAc2.png)

### n = 4

![](https://i.imgur.com/BkfrxdK.png)

### n = 10

![](https://i.imgur.com/gIHaSRl.png)

### n = 25

![](https://i.imgur.com/2OltqJR.png)
