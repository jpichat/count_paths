This is part of the code for the paper [(Pichat, 2015)](http://discovery.ucl.ac.uk/1468614/3/ISBI2015_tig.pdf) A multipath approach to histology volume reconstruction

## counting (s,t)-paths in a graph

We look for all the simple paths that connect vertices `s` and `t` in an undirected graph of order n.

`get_paths` takes an adjacency matrix, a `start` and `end` nodes as inputs and returns an exhaustive list of all the s-t paths.

The adjacency matrix may refer to a random graph, using `random_adjacency_matrix`, or to the graph used in (Pichat, 2015), using `our_adjacency_matrix`, where vertices are of degrees:
 - at least &epsilon; and at most 2&epsilon; if 1&le;&epsilon;&le;floor(n/2) 
 - at least &epsilon; and at most n-1 if floor(n/2)&lt;&epsilon;&lt;n-1
 - min(deg)=max(deg)=n-1 otherwise. 

&epsilon; is a parameter that tells how many adjacent nodes one node is connected with "above" and "below" (assuming the set of vertices is a sequence of increasing integers [0,1,...,n]).

All vertices are connected with up to &epsilon; neighbours above and below (when possible: degrees at both ends are less than 2&epsilon;). The sequence of vertex degrees, S, can be obtained (1) by convolution: 
 - S=f&lowast;g where f=[1,1,...,1]&isin;&Ropf;<sup>n</sup> and g=[1,..,1,0,1,..,1]&isin;&Ropf;<sup>2&epsilon;+1</sup> (there are &epsilon; ones on each side of the central zero; that zero is used so that no vertex is self-connected). 
 - One easily verifies that if &epsilon;&ge;n-1, then S=[n-1,n-1,...,n-1]&isin;&Ropf;<sup>n</sup> (i.e., the graph is complete).
 - ex: for n=6 vertices, &epsilon;=2, the sequence of degrees is: S=[2,3,4,4,3,2].

A more straighforward way to get S consists of (2) summing the elements of each row (or column) of the adjacency matrix. Using the same parameters, we have A:
<table>
  <tr> <td bgcolor="#ff9999">0</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#ff9999">0</td> <td bgcolor="#ff9999">0</td> <td bgcolor="#ff9999">0</td> </tr>
  <tr> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#ff9999">0</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#ff9999">0</td> <td bgcolor="#ff9999">0</td> </tr>
  <tr> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#ff9999">0</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#ff9999">0</td> </tr>
  <tr> <td bgcolor="#ff9999">0</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#ff9999">0</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#b3ffb3">1</td> </tr>
  <tr> <td bgcolor="#ff9999">0</td> <td bgcolor="#ff9999">0</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#ff9999">0</td> <td bgcolor="#b3ffb3">1</td>  </tr>
  <tr> <td bgcolor="#ff9999">0</td> <td bgcolor="#ff9999">0</td> <td bgcolor="#ff9999">0</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#b3ffb3">1</td> <td bgcolor="#ff9999">0</td> </tr>
</table> 

which yields the same sequence, S=[2,3,4,4,3,2].

_NB2_: the number of diagonals of ones above (resp. below) the main diagonal is &epsilon; (and it is bounded by n-1, in which case the graph is complete--without self-connections).

__Question:__ What are all the (3,2)-paths in the graph with the adjacency matrix A (above)? (the case &epsilon;=1 is trivial and gives only `[3, 2]`)

__Answer:__ `[[3, 1, 0, 2], [3, 1, 2], [3, 2], [3, 4, 2], [3, 5, 4, 2]]`

_NB3_: choosing n=12 and &epsilon;=n-1 gives 9,864,101 different paths.

The problem of finding the number (or a formula/procedure to obtain/estimate that number) of `(s,t)`-paths of a certain length in a graph is complicated (it is \#P-complete)...Answers are given in [(Roberts and Kroese, 2007)](https://people.smp.uq.edu.au/DirkKroese/ps/robkro_rev.pdf). Also check [here](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=EC4731136167A4EB6D39E68680065D4B?doi=10.1.1.156.345&rep=rep1&type=pdf).

`naive_path_generation` implements algorith 1 in (Roberts and Kroese, 2007) and estimates that number. However, as pointed out by the authors, it is biased toward short paths.
