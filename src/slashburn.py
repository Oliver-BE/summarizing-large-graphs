# all code below from: https://github.com/theeluwin/bear/blob/master/utils.py
import csv
import numpy as np

from collections import defaultdict
from scipy.sparse import coo_matrix


def scc(nodes=[], edges=[]):
    """
    Checks subgraphs (strongly connected means every vertex is reachable from every other vertex)
    A function that computes strongly connected components using Kosaraju's algorithm. Returns list of components, which are list of nodes.
    Args:
        nodes (list): List of nodes of any type.
        edges (list): List of edges, where each edge is a pair of nodes (ex: (0, 1)).
    Returns:
        List of strongly connected components. Each component is just a list of nodes.
    """
    alists = defaultdict(lambda: [])
    rlists = defaultdict(lambda: [])
    avisited = defaultdict(lambda: False)
    rvisited = defaultdict(lambda: False)
    leader = defaultdict(lambda: None)
    components = defaultdict(lambda: [])
    f = {}
    r = {}
    nodes = nodes
    edges = edges
    n = len(nodes)
    for u, v in edges:
        alists[u].append(v)
        rlists[v].append(u)
    t = 0
    for s in nodes:
        if rvisited[s]:
            continue
        rvisited[s] = True
        stack = [s]
        while len(stack):
            i = stack[-1]
            sink = True
            for j in rlists[i]:
                if not rvisited[j]:
                    rvisited[j] = True
                    stack.append(j)
                    sink = False
                    break
            if sink:
                t += 1
                f[i] = t
                stack.pop()
    for key in f:
        r[f[key]] = key
    for t in range(n, 0, -1):
        s = r[t]
        if avisited[s]:
            continue
        avisited[s] = True
        stack = [s]
        while len(stack):
            i = stack.pop()
            leader[i] = s
            components[s].append(i)
            for j in alists[i]:
                if not avisited[j]:
                    avisited[j] = True
                    stack.append(j)
    return [components[leader] for leader in components]

def verbose_matrix(A):
    """Stringfies matrix, considering only non-zero entries. Used for debugging."""
    n, m = A.shape
    A = A.toarray()
    return '\n'.join([' '.join(['1' if A[i][j] else ' ' for j in range(m)]) for i in range(n)])

def reorder_matrix(A, perm, fix_row=False, fix_col=False):
    """
    Reorders given coo matrix with given permutation. You can fix either row or column.
    Args:
        A (coo_matrix): Given coo matrix.
        perm (list): List of node indicies denoting permutation.
        fix_row (bool): If True, reorders column only.
        fix_col (bool): If True, reorders row only.
    Returns:
        A coo matrix.
    """
    A = A.tocoo()
    if not fix_row:
        row = [perm[i] for i in A.row]
    else:
        row = A.row
    if not fix_col:
        col = [perm[j] for j in A.col]
    else:
        col = A.col
    A = coo_matrix((A.data, (row, col)), shape=A.shape, dtype=A.dtype)
    del row, col
    return A


def slashburn(A, k=None, greedy=True):
    """
    Computes SlashBurn of given coo matrix. Currently, only size-ordering works for CCs.
    Args:
        A (coo_matrix): Given coo matrix. It should be an valid adjacency matrix. It considers non-zero entries as edges, and ignores self-loops.
        k (int): For hub selection. There is known rule of thumb, though. `k` = 1 produces (perfectly) optimal solution, but it will be slow.
        greedy (bool): If True, it uses greedy algorithm for hub selection. Slightly slow but slightly more accurate.
    Returns:
        (perm, wing): Permutation of node indicies and size of wing (int).
    """
    n, _ = A.shape
    if k is None:
        k = max(1, int(0.001 * n))
    head = []
    tail = []
    degree = {i: 0 for i in range(n)}
    alists = {i: [] for i in range(n)}
    for i, j in zip(A.row, A.col):
        if i == j:
            continue
        degree[j] += 1  # calculate degrees of each vertex
        alists[i].append(j) # Generate adjacency lists
    iteration = 0
    while True:
        iteration += 1
        if greedy:
            for _ in range(k): # remove highest degree vertex k times
                if not len(degree):
                    break
                top = max(degree, key=degree.get)
                head.append(top)
                alist = alists[top]
                del degree[top]
                del alists[top] #modify?
                for target in alist:
                    if target in degree:
                        degree[target] -= 1
        else:
            tops = sorted(degree, key=degree.get, reverse=True)[:k]
            head.extend(tops)
            for top in tops:
                alist = alists[top]
                del degree[top]
                del alists[top]
                for target in alist:
                    if target in degree:
                        degree[target] -= 1
        if not len(degree):
            break
        nodes = list(degree.keys())
        edges = []
        for source in alists: #create edges from nodes remaining after removing hub nodes
            for target in alists[source]:
                if target in alists:
                    edges.append((source, target))
        ccs = scc(nodes, edges) # Generates list of subgraphs left after hub removal
        m = len(ccs)
        sizes = {i: len(ccs[i]) for i in range(m)}
        ordering = sorted(sizes, key=sizes.get)
        ccs = [ccs[ordering[i]] for i in range(m)]
        # todo: implement hub-ordering
        for cc in ccs:
            size = len(cc)
            if size == 1 or size < k:
                tail.extend(cc)
                for bottom in cc:
                    alist = alists[bottom]
                    del degree[bottom]
                    del alists[bottom]
                    for target in alist:
                        if target in degree:
                            degree[target] -= 1
        assert len(head) + len(tail) + len(degree) == n
        if not len(degree):
            break
    tops = tail + head[::-1]
    perm = [0 for _ in range(n)]
    for i in range(n):
        perm[tops[i]] = i
    return perm, iteration * k

# Test Graph 
A = np.array([[1, 1, 0, 0], [1, 1, 1, 1], [0, 1, 1, 0], [0, 1, 0, 1]], dtype=np.int32)
A = coo_matrix(A)
print(verbose_matrix(A))
"""
1 1
1 1 1 1
  1 1
  1   1
"""
perm, wing = slashburn(A)
print(wing)  # 1
A = reorder_matrix(A, perm)
print(verbose_matrix(A))
"""
1     1
  1   1
    1 1
1 1 1 1
"""