import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

  
def get_neighbours(A, current_node:int, explored_nodes:list):
    current_node_neighbours=np.copy(A[current_node]) #get list of neighbours of current_node
    current_node_neighbours[explored_nodes]=0 #setting visited nodes to 0
    return np.where(current_node_neighbours==1)[0].tolist()


def count_empty(l:list):
    """count empty sublists of l until one non-empty is found
    """
    c=0
    if len(l)>1:
        while True:
            if len(l[c])!=0 or c==len(l)-1:
                break
            c+=1
    return c


def reverse(neighbours_list:list, explored_nodes:list):
    """remove empty lists to come back K levels up
    """
    K=count_empty(neighbours_list)
    if K==len(neighbours_list):
        K=K-1
    for k in range(K):
        neighbours_list.pop(0)
    for k in range(K+1):
        explored_nodes.pop(-1)
    return neighbours_list, explored_nodes


def get_paths(adjacency_matrix, start_node=None, end_node=None, verbose=False):
    """returns all simple paths connecting vertices `start_node` and
    `end_node` in undirected graph of order n with adjacency matrix `adjacency_matrix`
    """
    if start_node is None:
        start_node=adjacency_matrix.shape[0]//2
    if end_node is None:
        if 0<=start_node<adjacency_matrix.shape[0]-1:
            end_node=start_node+1
        else:
            end_node=start_node-1
    assert 0<=start_node<adjacency_matrix.shape[0]
    assert 0<=end_node<adjacency_matrix.shape[0]
    if verbose:
        print('==> adjacency matrix:\n'+str(adjacency_matrix))
        print('==> node set: '+str(np.arange(adjacency_matrix.shape[0])))
        print('==> start/end: '+str(start_node)+'->'+str(end_node))

    explored_nodes=[start_node]
    children=get_neighbours(adjacency_matrix, start_node, explored_nodes)
    neighbours_list=[children]
    paths_list=[]
    while len(neighbours_list[-1])!=0 or len(neighbours_list)>1:
        current_node=neighbours_list[0][0]
        neighbours_list[0].pop(0) #remove current node
        explored_nodes.append(current_node)
        if current_node==end_node:
            paths_list.append(list(explored_nodes))
            #come back one (or more) level up
            neighbours_list, explored_nodes=reverse(neighbours_list, explored_nodes)
        else:
            children=get_neighbours(adjacency_matrix, current_node, explored_nodes)
            if len(children)==0:
                #come back up
                neighbours_list, explored_nodes=reverse(neighbours_list, explored_nodes)
            else:
                #go deeper
                neighbours_list.insert(0, children)
    return(paths_list)



def naive_path_generation(adjacency_matrix, start_node:int, end_node:int):
    """generates a path from `start_node` via randomly chosen connected vertices
    until one of those is either the `end_node` or a dead end (no more connected vertices available)
    """
    is_path=True
    g=1 #likelihood
    explored_nodes=[start_node]
    children=get_neighbours(adjacency_matrix, start_node, explored_nodes)
    idx=np.random.randint(0,len(children))
    next_valid=children[idx] #picks first next valid node
    g*=1/len(children) #update likelihood
    while next_valid!=end_node:
        explored_nodes.append(next_valid)
        children_deeper=get_neighbours(adjacency_matrix, next_valid, explored_nodes)
        if len(children_deeper)>0:
            g*=1/len(children_deeper)
            idx_deep=np.random.randint(0,len(children_deeper))
            next_valid=children_deeper[idx_deep]
            children_deeper=np.delete(children_deeper, idx_deep)
        else:
            is_path=False
            break
    if is_path:
        explored_nodes.append(next_valid)
        path=explored_nodes
        return path, g
    else:
        return [None]*2



#=== other utils
def vdegrees(n:int, eps:int):
    """returns the sequence of degrees of each vertex
    of our eps-connected n-vertex graph using convolution
    """
    g=np.ones(n)
    el=np.hstack(([1]*eps,[0],[1]*eps))
    return signal.convolve(g, el, 'same')


def our_adjacency_matrix(n:int, eps:int):
    """return the adjency matrix of our n-vertex 
    eps-connected undirected graph
    """
    A=np.zeros((n,n))
    dr,dc=np.diag_indices(n)
    for o in range(1,eps+1):
        upper_d=dc+o
        A[(dr[:-o],upper_d[:-o])]=1
    i_lower=np.tril_indices(n,-1)
    A[i_lower]=A.T[i_lower]
    return A.astype(int)



def random_adjacency_matrix(s=10, density=5, return_st=True):
    """
    Notes
    -----
    - density=sum(range(1,s)) does not ensure the graph is complete (without self-connections) as the same index 
    may be picked multiple times in `random_upper` (however it gets less likely to happen as `s` grows). 
    We can only say the graph is epsilon-connected with epsilon>=1.
    - there might be isolated vertices
    """
    assert 1<=density<=sum(range(1,s))
    A=np.zeros((s,s))
    l_upper=list(zip(*np.triu_indices_from(A, 1)))
    random_upper=[l_upper[k] for k in np.random.randint(0, sum(range(1,s)), density)] #same index may be picked multiple times
    for i in random_upper:
        A[i]=1
    i_lower = np.tril_indices(s, -1)
    A[i_lower]=A.T[i_lower]
    if return_st:
        l_ones=np.argwhere(A==1)
        s,e=l_ones[np.random.randint(0, len(l_ones))] #pick a random 1 location in A for start/end couple
        return A.astype(int), s, e
    else:
        return A.astype(int),None,None



if __name__=="__main__":
    #===0.ADJACENCY matrix
    #special case of our paper's graph
    # n=6                 #total number of vertices
    # eps=5               #number of jumps allowed
    # A=our_adjacency_matrix(n,eps)
    # start_node=3
    # end_node=2

    #random graph
    A, start_node, end_node=random_adjacency_matrix(12, density=40, return_st=True)

    #===1.EXHAUSTIVE list (and therefore exact number) of s-t paths 
    paths_list=get_paths(A, start_node, end_node, verbose=True)
    print('==> exact number of paths: '+str(len(paths_list)))
    # print('==> path list: '+str(paths_list))

    #===2a.NAIVE estimation of number of s-t paths
    paths_list=[]
    L=[]
    n_estimate=0
    iterations=100000
    for i in range(iterations):
        path,g=naive_path_generation(A,start_node,end_node)
        if path:
            L.append(len(path)) #lenghts of generated valid paths
            n_estimate+=1/g #eq.(1)
            if path not in paths_list:
                paths_list.append(path)
    print('==> [naive] estimated number of paths: '+str(n_estimate/iterations))
    #plots
    fig, ax= plt.subplots(nrows=1, ncols=1)
    binwidth=0.5
    plt.hist(L, bins=np.arange(2-binwidth/2, max(L)+1-binwidth/2, binwidth))
    plt.xlabel('path length')
    plt.ylabel('occurences')
    plt.show()


    #===2b.length-aware estimation of number of s-t paths

