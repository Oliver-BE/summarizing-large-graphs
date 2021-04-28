# all code below adapted from https://github.com/GemsLab/VoG_Graph_Summarization/blob/master/MDL/model.py

class Model:
    strucTypes = []
    numStrucTypes = 0
    structs = []
    numStructs = 0
    
    numFullCliques = 0
    numNearCliques = 0
    numFullBiPartiteCores = 0
    numNearBiPartiteCores = 0 
    numStars = 0
    numChains = 0
    
    def __init__(self):
        self.strucTypes = ["fc", "nc", "bc", "nb", "st", "ch"] 
        self.numStrucTypes = len(self.strucTypes)
        self.structs = []        
        self.numStructs = 0

    def setStrucTypes(self, st):
        self.strucTypes = st
        self.numStrucTypes = len(self.strucTypes)
        
    # struct of type Struct
    def addStructure(self, struct):
        self.structs.append(struct)
        self.numStructs += 1
        
        if struct.getType() not in self.strucTypes:
            print("structure type not declared")
            
        if struct.isFullClique():
            self.numFullCliques += 1
        elif struct.isNearClique():
            self.numNearCliques += 1  
        elif struct.isFullBiPartiteCore():
            self.numBiPartiteCores += 1        
        elif struct.isNearBiPartiteCore():
            self.numNearBiPartiteCores += 1
        elif struct.isStar():
            self.numStars += 1
                  
        elif struct.isChain():
            self.numChains += 1

    # remove structure struct
    def rmStructure(self, struct) :
        self.structs.remove(struct)
        self.numStructs -= 1
        
        if struct.getType() not in self.strucTypes :
            print "structure type not declared"
            
        if struct.isFullClique() :
            self.numFullCliques -= 1
        elif struct.isNearClique() :
            self.numNearCliques -= 1            
        if struct.isFullOffDiagonal() :
            self.numFullOffDiagonals-= 1
        elif struct.isNearOffDiagonal() :
            self.numNearOffDiagonals -= 1            
        elif struct.isChain() :
            self.numChains -= 1
        elif struct.isStar() :
            self.numStars -= 1
        elif struct.isFullBiPartiteCore() :
            self.numBiPartiteCores -= 1        
        elif struct.isNearBiPartiteCore() :
            self.numNearBiPartiteCores -= 1
        elif struct.isCorePeriphery() :
            self.numCorePeripheries -= 1        
        elif struct.isJellyFish() :
            self.numJellyFishes -= 1        

    def load(self, fullpath):
        fg = open(fullpath)
        for line in fg :
            if len(line) < 4 or line[0] == "#" :
                continue
            struct = Structure.load(line)
            if struct != 0 :
                self.addStructure(struct)
        return
     
    def loadLine(self, content, lineNo):
        line = content[lineNo] # line of the model to be added
        if len(line) < 4 or line[0] == "#":
            return -1
        struct = Structure.load(line)
        if struct != 0 :
            self.addStructure(struct)
	return struct

    def loadLines(self, fullpath, lineList):
        fg = open(fullpath)
        lineNo = 0
        for line in fg :
            lineNo = lineNo + 1
            if lineNo > lineList[len(lineList) - 1] :
                break
            if lineNo in lineList :
            	if len(line) < 4 or line[0] == "#":
                	continue
            	struct = Structure.load(line)
            	if struct != 0 :
                	self.addStructure(struct)
        return

class Structure:
    @staticmethod
    def getType(self):
        return "?" 
        
    def isFullClique(self):
        return False
    def isNearClique(self):
        return False

    def isFullOffDiagonal(self):
        return False
    def isNearOffDiagonal(self):
        return False

    def isChain(self):
        return False
    def isStar(self):
        return False

    def isFullBiPartiteCore(self):
        return False

    def isNearBiPartiteCore(self):
        return False

    def isCorePeriphery(self):
        return False

    def isJellyFish(self):
        return False

    @staticmethod
    def load(line) :
        if line[:2] == FullClique.getType() :
            return FullClique.load(line)
        elif line[:2] == NearClique.getType() :
            return NearClique.load(line)
        if line[:3] == FullOffDiagonal.getType() :
            return FullOffDiagonal.load(line)
        elif line[:3] == NearOffDiagonal.getType() :
            return NearOffDiagonal.load(line)
        elif line[:2] == Chain.getType() :
            return Chain.load(line)
        elif line[:2] == Star.getType() :
            return Star.load(line)
        elif line[:2] == BiPartiteCore.getType() :
            return BiPartiteCore.load(line)
        elif line[:2] == NearBiPartiteCore.getType() :
            return NearBiPartiteCore.load(line)
        elif line[:2] == CorePeriphery.getType() :
            return CorePeriphery.load(line)
        elif line[:2] == JellyFish.getType() :
            return JellyFish.load(line) 

class Clique(Structure) :
    nodes = []
    numNodes = 0


class FullClique(Clique) :
    def __init__(self, nodes):
        self.nodes = nodes
        self.numNodes = len(nodes)
    
    @staticmethod
    def getType():
        return "fc" 

    def isFullClique(self):
        return True
    
    @staticmethod
    def load(line) :
        # "fc 1 2 3 4 ..
        if line[:2] != FullClique.getType() :
            return 0
        parts = line[3:].strip().split(' ')
        nodes = []
        for x in parts :
            if x.find('-') > 0 :
                y = x.strip().split('-')
                nodes.extend([z for z in range(int(y[0]),int(y[1])+1)])
            else :
                nodes.append(int(x))
        return FullClique(sorted(nodes))   


class NearClique(Clique) :
    numEdges = 0
    
    def __init__(self, nodes, numEdges):
        self.nodes = nodes
        self.numNodes = len(nodes)
        self.numEdges = numEdges

    @staticmethod
    def getType():
        return "nc" 

    def isNearClique(self):
        return True

    @staticmethod
    def load(line) :
        # "nc <edge count>, 1 2 3 4 ..
        if line[:2] != NearClique.getType() :
            return 0
        cParts = line[3:].strip().split(',')
        numEdges = int(float(cParts[0].strip()))
        
        sParts = cParts[1].strip().split(' ')
        
        nodes = []
        for x in sParts :
            if x.find('-') > 0 :
                y = x.strip().split('-')
                nodes.extend([x for x in range(int(y[0]),int(y[1])+1)])
            else :
                nodes.append(int(x))
        return NearClique(sorted(nodes), numEdges)    

class FullBiPartiteCore(Structure) :
    lNodes = []
    numNodesLeft = 0
    rNodes = []
    numNodesRight = 0
    
    def __init__(self, left, right):
        self.lNodes = left
        self.numNodesLeft = len(left)
        self.rNodes = right
        self.numNodesRight = len(right)

    @staticmethod
    def getType(self):
        return "bc" 

    def isFullBiPartiteCore(self):
        return True

    @staticmethod
    def load(self, line) :
        # "bc [left ids], [right ids]
        if line[:2] != FullBiPartiteCore.getType() :
            return 0
        parts = line[3:].strip().split(',')
        lParts = parts[0].strip().split(' ')
        lNodes = []
        for x in lParts :
            if x.find('-') > 0 :
                y = x.strip().split('-')
                lNodes.extend([z for z in range(int(y[0]),int(y[1])+1)])
            else :
                lNodes.append(int(x))
        rParts = parts[1].strip().split(' ')
        rNodes = []
        for x in rParts :
            if x.find('-') > 0 :
                y = x.strip().split('-')
                rNodes.extend([z for z in range(int(y[0]),int(y[1])+1)])
            else :
                rNodes.append(int(x))
        return FullBiPartiteCore(sorted(lNodes),sorted(rNodes)) 
   

class NearBiPartiteCore(Structure) :
    lNodes = []
    numNodesLeft = 0
    rNodes = []
    numNodesRight = 0
    
    def __init__(self, left, right):
        self.lNodes = left
        self.numNodesLeft = len(left)
        self.rNodes = right
        self.numRightNodes = len(right)

    @staticmethod
    def getType(self):
        return "nb" 

    def isNearBiPartiteCore(self):
        return True

    @staticmethod
    def load(self, line) :
        # "nb [left ids], [right ids]
        if line[:2] != NearBiPartiteCore.getType() :
            return 0
        parts = line[3:].strip().split(',')
        lParts = parts[0].strip().split(' ')
        lNodes = []
        for x in lParts :
            if x.find('-') > 0 :
                y = x.strip().split('-')
                lNodes.extend([z for z in range(int(y[0]),int(y[1])+1)])
            else :
                lNodes.append(int(x))
        rParts = parts[1].strip().split(' ')
        rNodes = []
        for x in rParts :
            if x.find('-') > 0 :
                y = x.strip().split('-')
                rNodes.extend([z for z in range(int(y[0]),int(y[1])+1)])
            else :
                rNodes.append(int(x))
        return NearBiPartiteCore(sorted(lNodes),sorted(rNodes)) 


class Star(Structure) :
    cNode = -1
    sNodes = []
    numSpokes = 0
    
    def __init__(self, hub, spokes):
        self.cNode = hub
        self.sNodes = spokes
        self.numSpokes = len(spokes)

    @staticmethod
    def getType(self):
        return "st" 
        
    def isStar(self):
        return True

    @staticmethod
    def load(self, line) :
        # "st <hubid> [spoke ids ...]
        if line[:2] != Star.getType() :
            return 0
        parts = line[3:].strip().split(',')
        cParts = parts[0].strip().split(' ')
        cNodes = []
        for x in cParts :
            if x.find('-') > 0 :
                y = x.split('-')
                cNodes.extend([x for x in range(int(y[0]),int(y[1])+1)])
            else :
                cNodes.append(int(x))
        sParts = parts[1].strip().split(' ')
        sNodes = []
        for x in sParts :
            
            if x.find('-') > 0 :
                y = x.split('-')
                sNodes.extend([x for x in range(int(y[0]),int(y[1])+1)])
            else :
                sNodes.append(int(x))
        return Star(cNodes[0],sorted(sNodes)) 


class Chain(Structure) :
    nodes = []
    numNodes = 0
    
    def __init__(self, nodes):
        self.nodes = nodes
        self.numNodes = len(nodes)

    @staticmethod
    def getType(self):
        return "ch" 

    def isChain(self):
        return True

    @staticmethod
    def load(self, line) :
        # "ch 1 2 3 4 ..
        if line[:2] != Chain.getType() :
            return 0
        parts = line[3:].strip().split(' ')
        nodes = []
        for x in parts :
            if x.find('-') > 0 :
                y = x.strip().split('-')
                nodes.extend([x for x in range(int(y[0]),int(y[1])+1)])
            else :
                nodes.append(int(x))
        return Chain(nodes) 
