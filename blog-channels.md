This post explores the question, what is possible to do in a channel, and what is not?

## Introduction

To review some relevant definitions from the paper: channels work by locking up some portion of blockchain state and modifying ownership of the locked state. Unanimous consent is required in order to update the ownership.

The locked blockchain state, known as the "state deposit" of a channel, is an arbitrary right to modify blockchain state. This includes modifying ether balance and ERC20 balances. Modifying of ownership includes simply changing who owns the state (like in a payment channel) but also includes placing the state under a complex "contract". An example contract is that the winner of a chess game gets the state. Another example is that some ERC20 tokens may be placed in a swap option contract, where a certain party has the right but not the obligation to exchange one token for another. These are used for hedging.

## State Deposits

However, state deposits don't just have to be monetary. An example I like to use is ELO score in chess. I love playing chess on lichess.org and ELO scores serve both as a motivator and as a means of making sure you play with people roughly at your level. Another example is reputation, whether formally tokenized or not. If you are interacting with a well-known semi-trusted entity on the blockchain (e.g. a bank), you could say that either the bank honours some contract, or you get to post evidence of their malfeseance to the blockchain, harming their reputation.

## Defined Participant Sets

The security of channels comes from the fact that changes to the state proceed by unanimous consent. If an action violates the rights of some participant, that participant will simply not sign off on it, and the action will not happen.

The biggest consequence of this mechanism is that state channels must have a defined participant set. By this we mean that the set of "interested parties" must be known beforehand and should be channel participants.

An example of a dapp that does not satisfy this criteria is a sha3 bounty dapp. What is a sha3 bounty dapp? Lots of cryptography depends on the existence of collision-resistent hash functions, functions for which it is computationally infeasible to explicitly find two preimages that hash to the same value. However the existence of such functions is an open question, much less whether existing constructions like SHA3 are collision-resistent. People may be concerned that the NSA have already broken SHA3, but are just hiding it. We can't prevent that, but we could offer a trustless incentive for anyone who knows a collision to disclose it via a smart contract. The contract would lock up some ether that anyone who submits a collision to it could claim. This way, at least we know that either

1. No one in the world knows of a collision, or
2. The people that do have an incentive greater than the bounty to keep their knowledge secret.

The nature of this dapp is that the set of interested parties is not defined at any point before the bounty is claimed; someone observing an uncollected bounty and forming the conclusion that "either no one knows of a collision, or ..." is only allowed to reason as such if it were true that if there were a person without an incentive greater than the bounty amount, that person could actually claim it. But the set of such people is not defined.

What happens if we actually host such a contract in a channel network? TBD.

## Small Participant Sets

Another consequence of the unanimous consent process for making state transitions in channels is that channels with very large numbers of participants are not robust, because any single participant could refuse to sign off on legitimate state transitions, forcing the rest to go on-chain and losing any scalability benefits. The specifics for why someone would refuse to sign off on legitimate states deserves another post, but for now it is worth noting that even at a very small base rate of unintentional actions such as network disconnections, the problem becomes exponentially worse as the number of participants increases.

One example of something that is affected by this constraint is an interactive auction. An auction can be thought of as a way to allocate a scarce resource to whoever would get the most utility out of it. It is perfectly fine to restrict an auction to an existing set of people already in a channel network, or to have a "registration phase" where interested parties not already in a channel network join it. Afterwards, there are many auction designs for which there participants may need to interact a large number of times, for which we can use channels. However, auctions typically attract a moderately large number of participants, which is a problem.

## Small State

The mechanism by which state in a state channel is finalized is that the state could be withdrawn to chain by any member of the channel. This places a constraint that the state must be withdrawable to chain.

We can proble these limits by trying to find games which won't work in channels. For instance, playing a game in a channel where the amount of information needed to describe the current game state is big enough that it cannot fit onto ethereum (e.g. it goes over the block size limit) is not safe, since the fallback mechanism of withdrawing the state to chain doesn't actually work. The line between "small enough to be safe" and "too big as to be unsafe" is a blurry one; if the state is big enough to fit into the block size limit but costs a lot of money, and one player can't actually afford to spend that money, it's not safe.

Furthermore, in a game, the concept of "state" as something enforceable on-chain also encompasses the set of rules by which a game state can advance further. The security mechanism is that the game state must be placed on chain and then some set of action taken. For instance, if we were playing a game where the game state could be withdrawn to chain but then the rules for determining if a next move is valid (or if a given game state is won for some player) costs too much to execute, this is unsafe as well.

In addition, the scalability benefits of channels comes from the fact that off-chain updates to the state do not need to be performed on-chain; hence dapps which update a small state with a large number of state transitions benefit the most. A good example is chess, where the game state is simply the chessboard, and the number of state transitions (moves) is typically large compared to the game state.

We can analyse the scalability benefits of channels for particular dapps within this framework. In the auction example, for a normal first-price auction where there is only one round of bidding, the scalability benefit we get is that the bid revelations take place off-chain and the actual transaction (wherein the highest bidder buys the item) takes place on-chain. The more complicated or interactive the auction mechanism is (e.g. multi-round auction), the more benefits we get.

In payment channels, a similar situation happens. The state here is the ownership of tokens, and the state transitions consists of updating this ownership. If balance changes are infrequent, we do not get much benefits from a payment channel network. Similarly, when using smart contracts to implement trustless derivative contracts, channelization provides a scalability benefit to the extent that these derivative contracts either are not often used (e.g. options that expire out-of-the-money) or where the collateral for them can be re-used within the same channel network.

## Nonexistence (TBD)

In a channelized chess-for-ELO network, if the results of games are not written on-chain, to prove that I have a certain ELO score would require me to disclose the set of all games I've won; however this implies proving nonexistence of certain signed messages (i.e. undisclosed losing games), which is impossible.

## Restructuring Apps (TBD)

These things place a lot of constraints on which dapps can be channelized. However, even if your entire dapp is not channelizable, you can sometimes redesign your dapp to have a channelizable part. An example is Augur. The core market functionality relies on anyone being able to interact with a market in order to provide liquidity and price discovery, and the core resolution / dispute functionality relies on anyone being able to stake REP to challenge a dispute. Both are properties that cannot be channelized directly. However, one can run a market maker in a channel that allows users to take positions in a market, with the market maker acting as a counterparty.

## Summary (TBD)

To summarize: channels are good for a large modification to a small state that affect a small number of players, but we can sometimes re-structure our apps to introduce this property.
