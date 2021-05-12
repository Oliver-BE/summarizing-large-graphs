class error: 

    def __init__(self, graph, err = None):
        if err is None :
            self.numNodes = graph.numNodes

            self.unmodelled = [set(x) for x in graph.edges]
            self.numUnmodelledErrors = graph.numEdges

            self.modelled = [set() for x in range(len(graph.edges))]
            self.numModellingErrors = 0
        
            self.covered = [set() for i in range(self.numNodes)]
            self.numCellsCovered = 0

            self.excluded = [set() for i in range(self.numNodes)]
            self.numCellsExcluded = 0
        else :
            self.numNodes = err.numNodes
            self.unmodelled = [set(x) for x in err.unmodelled]

       

    # checks whether edge (i,j) is covered
    def isModelled(self, i, j) :
        return (max(i,j)-1 in self.covered[min(i,j)-1]);
    def isCovered(self, i, j) :
        return self.isModelled(i,j);
        
    # annotates edge (i,j) as covered
    # ! (i,j) does not have to be in E of G(V,E)
    def cover(self, i, j) :
        self.covered[min(i,j)-1].add(max(i,j)-1);
        self.numCellsCovered += 1;
        return;

    # annotates edge (i,j) as both covered, and error-free
    # ! (i,j) does not have to be in E of G(V,E)
    def coverAndExclude(self, i, j) :
        self.cover(i,j)
        self.exclude(i,j);
        return;
        
    def exclude(self, i, j) :
        self.excluded[min(i,j)-1].add(max(i,j)-1);
        self.numCellsExcluded += 1;
        return;
        
    def isError(self, i, j):
        return max(i,j)-1 in self.unmodelled[min(i,j)-1] or max(i,j)-1 in self.modelled[min(i,j)-1];
        
    def isExcluded(self, i, j):
        return max(i,j)-1 in self.excluded[min(i,j)-1];
        
    def isUnmodelledError(self, i, j):
        return max(i,j)-1 in self.unmodelled[min(i,j)-1];
    def isUnmodelledEdge(self, i, j):
        return self.isUnmodelledError(i,j);

    def isModellingError(self, i, j):
        return max(i,j)-1 in self.modelled[min(i,j)-1];

    # annotates edge (i,j) as correct
    def delError(self, i, j) :
        if self.isUnmodelledError(i,j) :
            self.delUnmodelledError(i,j);
        else :
            self.delModellingError(i,j);      

    # annotates edge (i,j) as not-modelled
    def addUnmodelledError(self, i, j) :
        self.unmodelled[min(i,j)-1].add(max(i,j)-1);
        self.numUnmodelledErrors += 1;
        
    # annotates edge (i,j) as correctly modelled
    def delUnmodelledError(self, i, j) :
        self.unmodelled[min(i,j)-1].remove(max(i,j)-1);
        self.numUnmodelledErrors -= 1;

    # annotates edge (i,j) as erronously modelled
    def addModellingError(self, i, j) :
        self.modelled[min(i,j)-1].add(max(i,j)-1);
        self.numModellingErrors += 1;

    # annotates edge (i,j) as incorrectly modelled
    def delModellingError(self, i, j) :
        self.modelled[min(i,j)-1].remove(max(i,j)-1);
        self.numModellingErrors -= 1;

"""
def coverFullClique(G, E, c):
    # c.nodes is ordered
    for i_idx in range(c.numNodes) :
        i = c.nodes[i_idx];
        for j_idx in range(i_idx+1,c.numNodes) :
            j = c.nodes[j_idx];
            
            if not E.isExcluded(i,j) :
                # only if (i,j) is not modelled perfectly
                
                if not E.isCovered(i,j) :
                    # edge is not modelled yet
                    if G.hasEdge(i,j) :
                        # yet there is a real edge, so now we undo an error
                        E.delUnmodelledError(i,j);
                    else :
                        # there is no real edge, but now we say there is, so we introduce error
                        E.addModellingError(i,j);
                    E.cover(i,j);

                else :
                    # edge is already modelled
                    if G.hasEdge(i,j) and E.isModellingError(i,j) :
                        # edge exists, but model denied
                        E.delModellingError(i,j);
                    elif not G.hasEdge(i,j) and not E.isModellingError(i,j) :
                        # edge does not exist, but now we say it does
                        E.addModellingError(i,j);
    return;
"""


# Next step: implement functionality for adding subgraphs to model; calculating encoding error comes with that