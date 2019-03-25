This is part of the code of the paper [(Pichat, 2015) A multipath approach to histology volume reconstruction](http://discovery.ucl.ac.uk/1468614/3/ISBI2015_tig.pdf)

Counting (s,t)-paths in a graph
==================
Problem: We look for (all) the simple paths that connect vertices `s` and `t` (i.e., the (s,t)-paths) in an undirected graph of order n. This may consist of listing those paths ([see A](#headingI)), in which case the count is a by-product; or deriving a method that estimates the count without having to go through all the possible paths ([see B](#headingB)); note that the latter has little interest when one seeks the actual paths (but this is limited to rather small graphs).


## A. Get the list of (s,t)-paths<a name="headingA"></a>
`get_paths` takes as input (i) the adjacency matrix of a graph, (ii) a `start` and (iii) `end` vertices, and returns an exhaustive list of all the (s,t)-paths.

Note that the adjacency matrix may be that of a random graph, generated using `random_adjacency_matrix`, or more specifically that of the graph G in (Pichat, 2015), generated using `our_adjacency_matrix`.

In the following, we briefly comment on the latter case, for which G has vertices of degrees:
 - at least &epsilon; and at most 2&epsilon; if 1&le;&epsilon;&le;floor(n/2) 
 - at least &epsilon; and at most n-1 if floor(n/2)&lt;&epsilon;&lt;n-1
 - min(deg)=max(deg)=n-1 otherwise. 

&epsilon; is a parameter that tells up to how many adjacent vertices one vertex is connected with "above" and "below" (assuming the set of vertices is a sequence of increasing integers [0,1,...,n], such that "above" and "below" refer to greater or smaller vertex values). Note that degrees of vertices at both ends must be less than 2&epsilon;.

_NB1_: 
 - if &epsilon;=1, G is a path graph,
 - if 1&lt;&epsilon;&lt;n-2, G is &epsilon;-connected,
 - if &epsilon;=n-1, G is a complete graph.

The sequence of vertex degrees, S, can be obtained (1) by convolution: 
 - S=f&lowast;g where f=[1,1,...,1]&isin;&Ropf;<sup>n</sup> and g=[1,..,1,0,1,..,1]&isin;&Ropf;<sup>2&epsilon;+1</sup> (there are &epsilon; ones on each side of the central zero; that zero is used so that no vertex is self-connected). 
 - One easily verifies that if &epsilon;&ge;n-1, then S=[n-1,n-1,...,n-1]&isin;&Ropf;<sup>n</sup> (i.e., the graph is complete).
 - ex: for n=6 vertices, &epsilon;=2, the sequence of degrees is: S=[2,3,4,4,3,2].

A more straightforward way consists of (2) summing the elements of each row (or column) of its adjacency matrix. Using the same parameters, we have A:
```python
A=
[[0 1 1 0 0 0]
 [1 0 1 1 0 0]
 [1 1 0 1 1 0]
 [0 1 1 0 1 1]
 [0 0 1 1 0 1]
 [0 0 0 1 1 0]]
```
which yields the same sequence, S=[2,3,4,4,3,2].

_NB2_: the number of diagonals of ones above (resp. below) the main diagonal is &epsilon; (and it is bounded by n-1, in which case the graph is complete--without self-connections).

__Question:__ What are all the (3,2)-paths in G (adjacency matrix is A)? (the case &epsilon;=1 is trivial and gives only `[3, 2]`)

__Answer:__ `[[3, 1, 0, 2], [3, 1, 2], [3, 2], [3, 4, 2], [3, 5, 4, 2]]`

_NB3_: choosing n=12 and &epsilon;=n-1 gives 9,864,101 different paths using `get_paths`; and although complete, this is still a rather small graph.


## B. Back to the general case: estimating the count in random graphs<a name="headingB"></a>
The problem of estimating the number of `(s,t)`-paths in random graphs is complicated (it is \#P-complete), as listing them all in order to get their exact count is computationally intensive for large graphs...This is where sequential Monte Carlo methods are useful and interesting answers are proposed in [(Roberts and Kroese, 2007)](https://people.smp.uq.edu.au/DirkKroese/ps/robkro_rev.pdf). Also check [here](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=EC4731136167A4EB6D39E68680065D4B?doi=10.1.1.156.345&rep=rep1&type=pdf).

`naive_path_generation` implements algorithm 1 in (Roberts and Kroese, 2007) and estimates that number.

For example, given the following adjacency matrix:
```python
==> adjacency matrix:
[[0 0 1 0 1 1 1 1 1 1 1 1]
 [0 0 1 1 1 1 1 1 1 0 0 1]
 [1 1 0 1 0 0 0 0 1 0 1 1]
 [0 1 1 0 0 1 1 1 1 1 1 1]
 [1 1 0 0 0 0 1 0 1 1 1 1]
 [1 1 0 1 0 0 1 1 0 1 0 1]
 [1 1 0 1 1 1 0 1 1 1 1 0]
 [1 1 0 1 0 1 1 0 0 0 0 1]
 [1 1 1 1 1 0 1 0 0 1 1 0]
 [1 0 0 1 1 1 1 0 1 0 1 1]
 [1 0 1 1 1 0 1 0 1 1 0 1]
 [1 1 1 1 1 1 0 1 0 1 1 0]]
==> node set: [0  1  2  3  4  5  6  7  8  9 10 11]
==> start/end: 7/3
==> exact number of paths: 301402
==> [naive] estimated number of paths: 298952.9808
```

We can first observe that the estimated number of paths--calculated using eq.(1)--is rather close to the actual number, using 5000 randomly generated valid paths (from `naive_path_generation`). Second, the distribution of generated paths lengths is shown below; we can clearly observe the bias toward shorter paths (as pointed out by the authors), since longer paths are more likely to reach "dead ends" along the way.

One should also note that different valid (s,t)-paths may have the same length, which makes such a histogram tricky to interpret; as opposed to the direct path of length 2 (here [7,3]), which is the only one of length 2.

![histo_naive](figures/histo_naive2.png)
