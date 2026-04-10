---
tags:
  - protein-folding/misc
created: "2024-10-18T07:05:52"
modified: "2026-04-10T14:30:55"
---
#### Summary
**Monte Carlo Tree Search** is an iterative [[Reinforcement learning]] algorithm that finds optimal solutions in a highly multidimensional search space. It is a heuristic in that it does not require any knowledge beyond the "rules of the game".

#### Details
The algorithm proceeds in four steps:

1. **Selection:** a child node is selected with the highest upper confidence bound applied to trees ($UCT$):
$$UCT=\frac{w_{i}}{n_{i}}+C \sqrt{\frac{\ln{N_{i}}}{n_{i}}}$$
$w_{i}$: Score, or number of wins from this node
$n_{i}$: Number of simulations from this node
$N_{i}$: Total number of simulations
$C$: A constant that is chosen empirically (usually set to $\sqrt{2}$)

2. **Expansion:** a new child node is added to the tree at this optimally reached point
3. **Simulation** (AKA rollout): the remainder of the process or game is played out
4. **Backpropagation:** updating score of all nodes to the top of the tree with the result

#### Figures
\![[Repeated-X-times.png]]
*Figure from [geeksforgeeks.com](https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/)*
