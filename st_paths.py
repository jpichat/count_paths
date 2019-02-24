import numpy as np


def graph_vdegrees(n:int, eps:int):
    """returns the sequence of degrees of each vertex
    of our eps-connected n-vertex graph
    """
    g=np.ones(n)
    el=np.hstack(([1]*eps,[0],[1]*eps))
    return signal.convolve(g, el, 'same')


def get_neighbours(current_node:int, n:int, eps:int, explored_nodes:list):
    """nodes that can be reached from current_node
    """
    return list(filter(lambda a: (a!=current_node) &
                                 (a not in explored_nodes) &
                                 (a>=0) &
                                 (a<n), range(current_node-eps,current_node+(eps+1))) )

    
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


def get_paths(n:int, eps:int, start_node=None, end_node=None, verbose=False):
    """returns all simple paths connecting vertices `start_node` and
        `end_node` in an eps-connected undirected graph, G with n vertices
        
        Parameters:
        -----------
        :n:         total number of vertices
        :eps:       number of hops allowed (max(eps)=n-1)
        
        USAGE:
        ------
        n=6     #total number of vertices
        eps=2   #number of jumps allowed
        paths_list=get_paths(eta, eps, verbose=True)
    """
    if start_node is None:
        start_node=int(np.ceil(n/2))
    if end_node is None:
        end_node=start_node-1
    assert n>=2
    assert 0<=start_node<n
    assert 0<=end_node<n
    if verbose:
        print('start/end: '+str(start_node)+'->'+str(end_node)+' - set: '+str(list(range(n))))
        print('n:'+str(n)+' - eps:'+str(eps))

    explored_nodes=[start_node]
    children=get_neighbours(start_node, n, eps, explored_nodes)
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
            children=get_neighbours(current_node, n, eps, explored_nodes)
            if len(children)==0:
                #come back up
                neighbours_list, explored_nodes=reverse(neighbours_list, explored_nodes)
            else:
                #go deeper
                neighbours_list.insert(0, children)
    return(paths_list)


def adjency_matrix(n:int, eps:int):
    """return the adjency matrix of our n-vertex 
    eps-connected undirected graph
    """
    A=np.zeros((n,n))
    dr,dc=np.diag_indices(n)
    for o in range(1,eps+1):
        upper_d=dc+o
        A[[dr[:-o],upper_d[:-o]]]=1
    i_lower=np.tril_indices(n,-1)
    A[i_lower]=A.T[i_lower]
    return A


if __name__=="__main__":
    n=6                 #total number of vertices
    eps=2               #number of jumps allowed
    start_node=None
    end_node=None

    paths_list=get_paths(n, eps, start_node, end_node, verbose=True)
    print(paths_list)
