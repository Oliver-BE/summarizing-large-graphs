import src.MDL_error as mdle

class Error:
    size = 0
    covered = set()
    excluded = set()
    modelledErrors = set()
    unmodelled = 0

    oldCovered = set()
    oldExcluded = set()
    oldModelledErrors = set()
    oldUnmodelled = 0

    def __init__(self, A):
        self.graph = A
        self.size = len(A)
        for i in range(len(A)):
            for j in range(i, len(A)):
                if A[i][j] == 1:
                    self.unmodelled += 1
        self.oldUnmodelled = self.unmodelled

    def cover (self, x, y):
        self.covered.add((min(x, y), max(x, y)))

    def isCovered(self, x, y):
        return ((min(x, y), max(x, y))) in self.covered
    
    def exclude (self, x, y):
        self.excluded.add((min(x, y), max(x, y)))

    def isExcluded(self, x, y):
        return ((min(x, y), max(x, y))) in self.excluded

    def modelledError (self, x, y):
        self.modelledErrors.add((min(x, y), max(x, y)))

    def isModelledError(self, x, y):
        return ((min(x, y), max(x, y))) in self.modelledErrors

    def revert(self):
        self.covered = self.oldCovered
        self.excluded = self.oldExcluded
        self.modelledErrors = self.oldModelledErrors
        self.unmodelled = self.oldUnmodelled

    def update(self):
        self.oldCovered = self.covered
        self.oldExcluded = self.excluded
        self.oldModelledErrors = self.modelledErrors
        self.oldUnmodelled = self.unmodelled

    def currentErrorCost(self):
        return mdle.ErrorPrefix(self.size, len(self.covered), len(self.excluded), len(self.modelledErrors), self.unmodelled)
    
    def add(self, V, A, hub):
        if hub == -1:
            self.addPerfectSubgraph(V, A)
        elif hub == -2:
            self.addClique(V, A)
        elif hub == -3:
            # chain stuff
            pass
        else:
            self.addStar(V, A, hub)
    
    def errorAfterAdd(self, V, A, hub):
        if hub == -1:
            return self.errorAfterPS(V, A)
        elif hub == -2:
            return self.errorAfterClique(V, A)
        elif hub == -3:
            # chain stuff
            pass
        else:
            return self.errorAfterStar(V, A, hub)

    
    def addPerfectSubgraph(self, V, A):
        for x in V:
            for y in V:
                if A[x][y] == 1 and not self.isExcluded(x, y):
                    if not self.isCovered(x, y):
                        self.unmodelled -= 1
                        self.cover(x, y)

        self.update()
    
    def errorAfterPS(self, V, A):
        for x in V:
            for y in V:
                if A[x][y] == 1 and not self.isExcluded(x, y):
                    if not self.isCovered(x, y):
                        self.unmodelled -= 1
                        self.cover(x, y)

        cost = mdle.ErrorPrefix(self.size, len(self.covered), len(self.excluded), len(self.modelledErrors), self.unmodelled)
        
        self.revert()
        return cost

    def addClique(self, V, A):
        for x in V:
            for y in V:
                if not self.isExcluded(x, y):

                    if not self.isCovered(x, y):

                        if A[x][y] == 1:
                            self.unmodelled -= 1
                        else: 
                            self.modelledError(x, y)

                        self.cover(x, y)
                        self.exclude(x, y)

                    else:
                        if A[x][y] == 1 and self.isModelledError(x, y):
                            self.unmodelled -= 1
                        elif A[x][y] == 0 and not self.isModelledError(x, y):
                            self.modelledError(x, y)

        self.update()

    def errorAfterClique(self, V, A):
        for x in V:
            for y in V:
                if not self.isExcluded(x, y):

                    if not self.isCovered(x, y):

                        if A[x][y] == 1:
                            self.unmodelled -= 1
                        else: 
                            self.modelledError(x, y)

                        self.cover(x, y)
                        self.exclude(x, y)

                    else:
                        if A[x][y] == 1 and self.isModelledError(x, y):
                            self.unmodelled -= 1
                        elif A[x][y] == 0 and not self.isModelledError(x, y):
                            self.modelledError(x, y)
        
        cost = mdle.ErrorPrefix(self.size, len(self.covered), len(self.excluded), len(self.modelledErrors), self.unmodelled)

        self.revert()
        return cost
    
    def addStar(self, V, A, hub):
        for x in V:
            if not self.isExcluded(x, hub):

                if not self.isCovered(x, hub):

                    if A[x][hub] == 1:
                        self.unmodelled -= 1
                    else:
                        self.modelledError(x, hub)

                    self.cover(x, hub)
                
                else:
                    if A[x][hub] == 1 and self.isModelledError(x, hub):
                        self.unmodelled -=1
                    elif A[x][hub] == 0 and not self.isModelledError(x, hub):
                        self.modelledError(x, hub)
        self.update()

    def errorAfterStar(self, V, A, hub):
        for x in V:
            if not self.isExcluded(x, hub):

                if not self.isCovered(x, hub):

                    if A[x][hub] == 1:
                        self.unmodelled -= 1
                    else:
                        self.modelledError(x, hub)

                    self.cover(x, hub)
                
                else:
                    if A[x][hub] == 1 and self.isModelledError(x, hub):
                        self.unmodelled -=1
                    elif A[x][hub] == 0 and not self.isModelledError(x, hub):
                        self.modelledError(x, hub)

        cost = mdle.ErrorPrefix(self.size, len(self.covered), len(self.excluded), len(self.modelledErrors), self.unmodelled)
        self.revert()
        return cost

    """
    def addChain(self, V, A, start, end):
        visited = set()
        x = start
        while x != end:

            for y in V:
                if not isExcluded(x, y):

                    if A[x][y] == 1 and y not in visited:
                        visited.add(y)
    """




        

                        
