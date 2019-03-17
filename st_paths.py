import numpy as np
from scipy import signal


  
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



#=== other utils
def vdegrees(n:int, eps:int):
    """returns the sequence of degrees of each vertex
    of our eps-connected n-vertex graph using convolution
    """
    g=np.ones(n)
    el=np.hstack(([1]*eps,[0],[1]*eps))
    return signal.convolve(g, el, 'same')


def get_adjacency_matrix(n:int, eps:int):
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



if __name__=="__main__":
    #special case: our graph
    n=6                 #total number of vertices
    eps=2               #number of jumps allowed
    A=get_adjacency_matrix(n,eps) #our graph
    
    #test with random graph
    A=np.array([[0,1,0,1,0],
                [1,0,0,1,1],
                [0,0,0,1,1],
                [1,1,1,0,0],
                [0,1,1,0,0]])

    start_node=4
    end_node=5
    paths_list=get_paths(A, start_node, end_node, verbose=True)
    print('==> path list: '+str(paths_list))
