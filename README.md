`get_paths` looks for all the simple paths that connect vertices `s` and `t` in an undirected graph with n vertices (each of degree at least \epsilon;). 

In the case &epsilon;=1, the graph is a path graph. For &epsilon;>1, it becomes an &epsilon;-connected graph and in our case, only the first and last nodes have degree \epsilon; while all other (intermediate) vertices have degree \epsilon;+1.

__Question:__ How many (3,2)-paths are there in a 2-connected graph with n=6 vertices? (the case &epsilon;=1 is trivial and gives only `[3, 2]`)

__Answer:__ `[[3, 1, 0, 2], [3, 1, 2], [3, 2], [3, 4, 2], [3, 5, 4, 2]]`

_NB1_: The problem of finding the number (or a formula/procedure to obtain/estimate that number) of `(s,t)`-paths of a certain length in a graph is complicated (it is \#P-complete)...Promising answers can be found [here](https://people.smp.uq.edu.au/DirkKroese/ps/robkro_rev.pdf) or [here](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=EC4731136167A4EB6D39E68680065D4B?doi=10.1.1.156.345&rep=rep1&type=pdf).

_NB2_: choosing n=12 and &epsilon;=n-1 gives 9,864,101 different paths.