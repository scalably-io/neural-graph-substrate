# Why we did this, and what we asked

**Why.** Today's networks compute by passing an input once through a fixed stack of layers. We wanted to know whether a different substrate could do more with the same weights: a persistent graph of neural nodes that keeps state, rewires itself from that state at every step, and computes by evolving until it halts. If the same weights can be reused across many graph configurations, capacity might come from time and topology rather than from more parameters.

**What we asked ourselves.**
1. Can such a recurrent, self-routing graph give more reasoning capacity per stored parameter than a fixed-depth Transformer?
2. Is that gain from the graph, or only from recurrence, which a looped Transformer already has?
3. Which parts of the design are already published, and is anything genuinely open?
4. What is the smallest matched experiment that would settle the open part, and how could it fail?

**Scope.** Ordinary digital hardware (GPU, TPU, CPU). Every claim had to be backed by a primary source with a quote, and the answer had to be allowed to come out negative.
