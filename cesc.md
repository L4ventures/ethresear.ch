cesc talk

# scalability via layer 2: open questions

This document is centered around this question: in the very long term, is there a place for layer 2 as a scalability solution?

NB: even if the answer is "no", still, we would like state channels for instant finality!

We will pose 5 open questions

1. in what circumstances are payment channel networks useful?
2. what's not possible in channels?
3. what is the expected outcome of a system with targetted griefing vectors?
4. what is the layer 2 design space?
5. how do we pay for layer 2 security?

## Payment Channel Networks

Payment channels allow participants to modify the ownership of locked blockchain state. Payment channel networks allow trustless payment through intermediaries.

How do we characterise the scalability benefits of payment channels? Well, normally people tend to measure it with TPS, so let's imagine that we try to do that. A transaction in a payment updates the balances, and is achieved by an exchange of messages (hence the instant finality), hence in a channel where two people just send 1 eth back and forth, TPS is bounded by network latency

Obviously this is not a very useful observation. Any scalability benefits channels bring must come with two caveats:

1. They are subject to collateral constraints. In a PCN, sometimes a route just won't exist between two people.
2. Channel networks by themselves are not open enrollment; you have to pay an onchain fee to join.

Open Question 1: How do we model these constraints? How will they affect real-world scalability benefits?

In the case that two people in fact update a balance many times, we get a benefit. Generalizing a bit, in the case that people pay each other in a ring, we get a benefit. The most general claim seems to be that we get a benefit if there is a set of nodes for which the net transfer of ownership across the group boundary is small compared to transfers within the group, and that this constraint is known in advance. How often does this happen? I think to properly answer this, we need to model the reason people send each other money, something like a time-dependent per-person utility function dependent on the balance ownership of everyone in the network, and a per-person time-dependent expectation on how the utility function will evolve over time.

## State Channels

State channels allow participants to modify the ownership of locked blockchain state, including placing them under certain kinds of contracts.

The caveats from payment channels also apply to state channels. For instance, someone could try to make a trustless SHA3 bounty dapp that awards some amount of ETH for anyone producing a collision. On ethereum, this is easy enough; assuming the chain is censorship-resistant, the existence of an unclaimed bounty provides some evidence that no one has produced a collision (or that someone who has has some incentive above the bounty amount to not reveal it, etc). But this guarantee seems impossible to get in a channel network.

Open Question 2: How do we precisely characterise the set of things possible and not possible in a state channel network?

Another thing possible in state channel networks is unavailability griefing. In a chess game, even if I make a legal move, my opponent could refuse to countersign it. I am forced to go on chain, and transaction fees must be paid. The chain can't distinguish between the cases where:

1. My opponent was unavailable
2. I claim my opponent was unavailable, but he actually was available

hence we can't punish a single person. From this point of view the best we can do is split the transaction fees. Hence this becomes a griefing attack where an attacker pays money to cause the victim to lose money.

Why would someone do this kind of griefing attack? In a chess game, perhaps the attacker is losing, and TBD.

Open Question 3: In the presence of targetted griefing vectors, what is the expected outcome?

With equilibrium analysis, we get an answer that's too optimistic; with griefing analysis we get a huge gap.

## Other Layer 2 Solutions

This title is a catch-all category to capture things that are layer 2, and then exclude channels. Plasma MVP and Plasma Cash are two elements of this set. Briefly speaking, in these two designs, users use an on-chain transaction to deposit money into a SC to "enter" the plasma chain, and an on-chain transaction to withdraw money to "exit" the plasma chain. In between, there are periodic small on-chain commitment to a large amount of transaction data (transactions change ownership of ether), which is where you get a TPS improvement. On exit, both designs use an enforced "challenge period" which contains an interactive game to determine if the exiter is the rightful owner.

The most insidious attack against such architectures is data unavailability, i.e., committing an on-chain root for which the body is unavailable (not downloadable). A malicious operator can somehow try to hide an invalid state transition among lots of unavailable ones, so an interactive game can't efficiently find the invalid state transition. The most general attack is the operator hiding an invalid txn that mints plasma tokens and awards it to themselves.

MVP solves this by allowing users to withdraw cheaply from the last available block, and to get their money before the fake money is withdrawn. Cash enforces some constraints on the allowed state transition (no splitting or merging of coins) so that this "operator-mints-money" attack is not possible, and an interactive game can efficiently resolve all exit disputes.

The optimally cheapest way to exit costs 1 bit per exiting user/coin, and this is optimal by information theory, since if there are $N$ users, there are $2^N$ exiting subsets. However, we can compress some parts of the space (eg almost-full subsets) by increasing the size of others.

// As before, a failed attack of this kind is a griefing attack; a successful attack is stolen money.

An open question is can we generalise these two designs to run smart contracts? Problems include is

- no clear ownership of contracts
- many contracts presume data availability and censorship resistance
- the plasma cash restriction on the STF seems hard to generalize
- state size restriction

Open Question 4: What is in the rest of the design space?

Note that we know many mechanisms that are not used in current designs! These include

- Exiting to uncle chains, still subject to the 1-bit restriction
- Using a plasma staking token whose value is tied to the future expected revenue. Subjective attacks like "is the plasma chain chain censored or unavailable" gets priced into the token.
- App-specific plasma chains, which let you group transactions together. If you do this recursively you get mapreduce, although basically no-one knows how this is supposed to work

So q4 is open-ended and leads to lots of small questions, probably because less people have thought about it? For instance, here's a small but interesting question: assuming we only care about payments, and assuming we are "not allowed" to rely on a separate consensus strength, what is the design space? Other small questions: TBD.

Describe Vitalik's definition of L2.

Describe JDMBLA - imposes some cost on users but...viable or not?

## Security

There is an argument that L2 scalability increases the reward of attacking L1 and hence reduces L1 security. This argument is sound; however, interesting to note that since L2 scaling is permisionless, this is a problem with L1 fee structre in some sense! Indeed, any dapp running on eth increases the reward of attacking L1.

Open Question 5: How do we solve this?

Maybe look at the problem economically. We can view a basic non-sharded non-L2 blockchain as some decentralized enforcement of property rights (and maybe contract law). Users demand this for various reasons, and block producers supply this by marginally increasing security. When sharding comes, they can also marginally increase capacity. The fee market + issuance + slashing matches supply and demand in a weird way.

In this light, a normal dapp consumes the good by making an attack more lucrative, but pays for it partially with fees. An L2 dapp consumes the good but does not pay for it with fees! There is a tradgedy of the commons where a single L2 dapp decreases everyone's security but consumes all the benefits.

In a post-sharding world there's another problem: there must be enough rewards to BPs to sustain many of them (especially with superquadratic sharding). There could be a similar situation where the equilibrium is everyone moving to L2, no rewards to L1, leading to reduced L1 capacity, which is weird because you need "counterfactual L1 capacity" to enforce L2 capacity.
