# Base of code taken from MDL_error https://github.com/GemsLab/VoG_Graph_Summarization
from math import log,factorial
import src.MDL as mdl
import src.graph_classification as gc

### Encoding the Error

def createSubAdjacencyMatrix(V, A):
	"""
	Given an initial adjacency matrix A and list of vertices V, returns a sub-adjacency matrix
	containing only the rows and columns in V.
	"""
	# Initialize a matrix
	# matrix = [[0 for j in range(len(V))]
	# 				for i in range(len(V))]
	matrix = []
	
	# need to sort V in order of vertex
	V.sort()
	V_set = set(V)
		
	for i in V:		
		temp = [] 
		for j in V: 
			if i in V_set and j in V_set: 
				if i == j:
					temp.append(0)
				else: 
					temp.append(A[i][j])
		matrix.append(temp)

	return matrix

def calculate_noise(A, V=None):
	"""
	Calculates the cost, in bits, of encoding the adjacency matrix with an empty model M.

	 case 'err'
        if E(1) ~= 0 && E(2) ~= 0
            MDLcost = Lnu_opt( E );
        elseif E(1) ~= 0 
            MDLcost = LN( E(1) );
        elseif E(2) ~= 0
            MDLcost = LN( E(2) );
        end
	
	 cost_notEnc = compute_encodingCost( 'err', 0, 0, [nnz(Asmall) n^2-nnz(Asmall)]);
	 noise: [nnz(Asmall) n^2-nnz(Asmall)]
	 E1 = nnz(Asmall)
	 E2 = n^2-nnz(Asmall)

	 
	% 0s in the error matrix  --- edges included in the structure (full clique)
	E(2) = nnz(Asmall);
	% 1s in the error matrix  --- edges excluded from the structure (full clique)
	E(1) = n^2 - n - E(2);

	
	"""
	included = set()
	for x in V:
		for y in V:
			if A[x][y] == 1:
				included.add((x, y))
	E1 = len(included)
	E2 = len(V)*len(V) - E1
	
	if E1 != 0 and E2 != 0:
		return lnu_opt(E1, E2)
	elif E1 != 0:
		mdl.LN(E1)
	elif E2 != 0:
		mdl.LN(E2)
	else:
		pass


def MDL_error_cost(model, A, excluded): # need to figure out what is being added to the model and detract that from error
	covered = set()
	ignored = set()
	modelledErrors = set()
	# By default, the number of unmodelled errors is the number of edges
	# and the number of modelled errors is 0.
	# Compute no. edges
	unmodelled = 0
	for i in range(len(A)):
		for j in range(i, len(A)):
			if A[i][j] == 1:
				unmodelled += 1 

	modelled = 0
	for subgraph in model: 
		approx = False
		for x in subgraph:
			for y in subgraph:  
				if (min(x, y), max(x, y)) in excluded:
					approx = True
		edges = gc.getEdges(subgraph, A)
		# NOTE: assuming that subgraph has property nodes, a list of its nodes, and property edges, a list of all its edges

		for x in subgraph:
			for y in subgraph:
				
				# Consider only edges in the subgraph. This allows us to create a 
				# blanket method for dealing with different types of subgraphs
				if (min(x, y), max(x, y)) not in edges and (min(x, y), max(x, y)) not in excluded:
					continue
				if (min(x, y), max(x, y)) in ignored:
					continue
				# If edge is not yet covered:
				if (min(x, y), max(x, y)) not in covered:

					# Then, if the edge (x, y) exists in A, remove an unmodelled error:
					if A[x][y] == 1:

						unmodelled -= 1

					# If the edge doesn't exist in A, we've introduced a modelling error:
					else:

						modelled += 1
						modelledErrors.add((min(x, y), max(x, y)))
					# Add (x, y) to the list of covered edges
					# Edges are added as (smallest node, largest node) because we assume the graph
					# is undirected, and this method makes things easier.
					covered.add((min(x, y), max(x, y)))
					if approx:
						ignored.add((min(x, y), max(x, y)))

				# If the edge has been covered:
				else:

					# If the edge exists in A, but the model does not contain it, remove a modelling error
					if A[x][y] == 1 and (min(x, y), max(x, y)) in modelledErrors:

						modelled -= 1

					# Otherwise, if the edge does not exist, but the model says it does, add a modelling error
					elif A[x][y] == 0 and (min(x, y), max(x, y)) not in modelledErrors:

						modelled += 1

					if approx:
						ignored.add((min(x, y), max(x, y)))

	# Once the number of modelled and unmodelled errors have been computed, compute the error cost

	# Error cost computed using typed prefix method from paper (see function LErrorTypedPrefix(G, M, E))

	return ErrorPrefix(len(A), len(covered), len(excluded), modelled, unmodelled) # TODO: The 0 here should technically be the count of 'excluded' edges, needs to be handled later

def ErrorPrefix(num_nodes, num_covered, num_excluded, modelled, unmodelled):
	posNumEdges = (num_nodes * num_nodes - num_nodes) / 2
	# if (num_covered - num_excluded) - modelled < 0  or (num_covered - num_excluded) - unmodelled< 0:
	# 	print(f"num_covered: {num_covered}, num_excluded: {num_excluded}, modelled: {modelled}, unmodelled: {unmodelled}")
	costM = LnU(num_covered - num_excluded, modelled)
	costU = LnU(posNumEdges - num_covered, unmodelled)
	return costM + costU


def LnU(n,k): 
	if n==0 or k==0 or k==n:
		return 0
	# if n < k:
	# 		return 0 

	x = -log(k / float(n),2)
	y = -log((n-k)/float(n),2)
	return (k * x + (n-k) * y)

    # Encoded length of `n` 0/1 entries with `k` 1s (aka, Uniform)

# def getChainPath(start, end, V, A):
# 	"""
# 	Given a starting and ending node (and adjacency matrix), reconstructs the path found 
# 	from getChainEndpoints.
# 	""" 
# 	stack = [start]
# 	path = [start]
# 	visited = set()
# 	visited.add(start)

# 	while stack: 
# 		current = stack.pop()
# 		num_neighbors = 0
# 		for neighbor in V: 
# 			if neighbor == end and A[current][neighbor] == 1 and neighbor not in visited:
# 				path.append(end)
# 				break
# 			elif A[current][neighbor] == 1 and neighbor not in visited: 
# 				num_neighbors += 1
# 				visited.add(neighbor) 
# 				stack.append(neighbor)
# 				path.append(neighbor) 
# 		# if there were no neighbors, reset path
# 		if num_neighbors == 0:
# 			path = [start]
	
# 	return path


# def getChainEndpoints(V, A):
# 	"""
# 	Used to find the endpoints of the longest chain in a subgraph that is a near-chain.
# 	This is the heuristic mentioned by the paper in Section 4.2.2.
# 	NOTE: If the graph contains a loop, this algorithm will pick the shortest possible path between two nodes. 
# 	This essentially picks the longest shortest path between any two nodes.
# 	""" 
# 	max_start = 0
# 	max_end = 0
# 	# V.sort()
	
# 	for v in V:
# 		visited = set()
# 		queue = [v] 
# 		start = v
# 		end = start 
# 		# Set source as visited
# 		visited.add(v)
# 		# count the number of pops from the stack (number of levels)
# 		num_pops = 0 
# 		longest_path = 0 
# 		# this keeps track of the number of nodes in each level
# 		nodes_by_level = []
# 		# temp queue for neighbors
# 		q_neighbors = []
# 		# only get neighbors of first vertex
# 		for neighbor in V:
# 			if A[v][neighbor] == 1 and neighbor not in visited:  
# 				# Push the adjacent node in the queue
# 				q_neighbors.append(neighbor) 
# 				# mark as visited
# 				visited.add(neighbor) 
# 				end = neighbor 
 
# 		while queue or q_neighbors: 
# 			# if queue is empty, we've hit the next level and can replace it with q_neighbors
# 			if not queue:
# 				nodes_by_level.append(len(q_neighbors))
# 				queue = q_neighbors.copy()
# 				q_neighbors.clear()  

# 			current = queue.pop(0)

# 			# for every adjacent vertex to the current vertex
# 			for neighbor in V:
# 				if A[current][neighbor] == 1 and neighbor not in visited:   
# 					# Push the adjacent node in the queue
# 					q_neighbors.append(neighbor) 
# 					# mark as visited
# 					visited.add(neighbor)
# 					end = neighbor 
 
# 		path_length = len(nodes_by_level) 
# 		if path_length > longest_path:
# 			longest_path = path_length
# 			max_start = start
# 			max_end = end
	
# 	return (max_start, max_end) 

def chainError(V, A, start, end, excluded):
	
	# sub = createSubAdjacencyMatrix(V, A)
	# for i in range(len(sub)):
	# 	print(sub[i])

	modelled = 0
	unmodelled = len(V) - 1
	covered = set()
	modelledErrors = set()
	ignored = set()

	visited = set() 
	# if start > end:
	# 	temp = start
	# 	start = end
	# 	end = temp
		
	current = start
	while current != end:
		
		for neighbor in V: 
			if (min(current, neighbor), max(current, neighbor)) in excluded:
				continue
			if (min(neighbor, current), max(neighbor, current)) in ignored:
				continue
			if A[current][neighbor] == 1 and neighbor not in visited:
				visited.add(current)

				# Update errors:
				if (min(neighbor, current), max(neighbor, current)) not in covered:

					if A[neighbor][current] == 1:

						unmodelled -= 1
					else:

						modelled += 1
						modelledErrors.add((min(neighbor, current), max(neighbor, current)))

					covered.add((min(neighbor, current), max(neighbor, current)))
					ignored.add((min(neighbor, current), max(neighbor, current)))
					
				else:
					if A[current][neighbor] == 1 and (min(neighbor, current), max(neighbor, current)) in modelledErrors:

						modelled -= 1
					elif A[current][neighbor] == 0 and ((min(neighbor, current), max(neighbor, current))) not in modelledErrors:

						modelled += 1

					ignored.add((min(neighbor, current), max(neighbor, current)))

				current = neighbor
				break
			
	return ErrorPrefix(len(A), len(covered), len(ignored), modelled, unmodelled)
		
	
def starError(V, A, hub):
	"""
	case 'st'
        if E(1) == 0 || E(2) == 0 %if sum(sum(E)) == 0
            MDLcost = LN( n_sub-1 ) + log2( N_tot ) +  l2cnk(N_tot-1, n_sub-1); %log2( nchoosek( vpi(N_tot-1), n_sub-1 ) );
        else
            MDLcost = LN( n_sub-1 ) + log2( N_tot ) + ...
                l2cnk(N_tot-1, n_sub-1) + ...  %log2( nchoosek( vpi(N_tot-1), n_sub-1 ) ) + ...
                Lnu_opt( E );
        end

	% missing edges in star + extra edges not in star
	E(1) = 2* (n-1-nnz(Asmall(idxMaxDeg,:))) + nnz(Asmall(satellitesIdx, satellitesIdx));
	% 0s in the error matrix
	%wrong_edges_in_star = 2*(n-nnz(Asmall(idxMaxDeg,:)));
	E(2) = n^2 - E(1);
	"""
	missing_and_extra = set()

	for x in V:
		for y in V:
			# if edge is connected to hub, but not in graph, edge is missing from star; add to set
			if x == hub or y == hub:
				if A[x][y] == 0:
					missing_and_extra.add((x, y))
			# if edge is in graph but not part of star, edge is an extra not in star; add to set
			if A[x][y] == 1:
				if x != hub and y != hub:
					missing_and_extra.add((x, y))
	E1 = len(missing_and_extra)
	E2 = len(V)*len(V) - E1


	return lnu_opt(E1, E2)

def cliqueError (V, A):
	"""
	% 0s in the error matrix  --- edges included in the structure (full clique)
	E(2) = nnz(Asmall);
	% 1s in the error matrix  --- edges excluded from the structure (full clique)
	E(1) = n^2 - n - E(2);

	"""
	included = set()
	for x in V:
		for y in V:
			
			if A[x][y] == 1:
				# edge is included
				included.add((x, y))

	E2 = len(included)
	E1 = len(V)*len(V) - len(V) - E2
	return lnu_opt(E1, E2)


def lnu_opt(inc, exc):
	error = mdl.LN(inc) + (inc * nll(inc, exc, 1)) + (exc * nll(inc, exc, 0))
	return error

def nll(inc, exc, sub):
	l = 0
	if sub == 0:
		l = -log(exc/(inc+exc), 2)
	elif sub == 1:
		l = -log(inc/(inc+exc), 2)
	else:
		pass
	return l


# def cliqueApproxError(V, A, excluded):
# 	modelled = 0
# 	unmodelled = len(V)*len(V)/2
# 	covered = set()
# 	modelledErrors = set()
# 	ignored = set()
# 	for x in V:
# 		for y in V:
			
# 			if (min(x, y), max(x, y)) in ignored:
# 				continue
# 			# If edge is not yet covered:
# 			if (min(x, y), max(x, y)) not in covered:

# 				# Then, if the edge (x, y) exists in A, remove an unmodelled error:
# 				if A[x][y] == 1:

# 					unmodelled -= 1

# 				# If the edge doesn't exist in A, we've introduced a modelling error:
# 				else:

# 					modelled += 1
# 					modelledErrors.add((min(x, y), max(x, y)))
# 				# Add (x, y) to the list of covered edges
# 				# Edges are added as (smallest node, largest node) because we assume the graph
# 				# is undirected, and this method makes things easier.
# 				covered.add((min(x, y), max(x, y)))
				
# 				if (min(x, y), max(x, y)) in excluded:
# 					ignored.add((min(x, y), max(x, y)))

# 			# If the edge has been covered:
# 			else:

# 				# If the edge exists in A, but the model does not contain it, remove a modelling error
# 				if A[x][y] == 1 and (min(x, y), max(x, y)) in modelledErrors:

# 					modelled -= 1

# 				# Otherwise, if the edge does not exist, but the model says it does, add a modelling error
# 				elif A[x][y] == 0 and (min(x, y), max(x, y)) not in modelledErrors:

# 					modelled += 1

# 				if (min(x, y), max(x, y)) in excluded:
# 					ignored.add((min(x, y), max(x, y)))

# 	return ErrorPrefix(len(A), len(covered), len(ignored), modelled, unmodelled)

# def starApproxError(V, A, excluded, hub):
# 	modelled = 0
# 	unmodelled = len(V) - 1
# 	covered = set()
# 	modelledErrors = set()
# 	ignored = set()

# 	for x in V:
# 		# If edge is not yet covered:
# 		if (min(x, hub), max(x, hub)) in ignored:
# 				continue

# 		if (min(x, hub), max(x, hub)) not in covered:

# 			# Then, if the edge (x, y) exists in A, remove an unmodelled error:
# 			if A[x][hub] == 1:

# 				unmodelled -= 1

# 			# If the edge doesn't exist in A, we've introduced a modelling error:
# 			else:

# 				modelled += 1
# 				modelledErrors.add((min(x, hub), max(x, hub)))
# 			# Add (x, y) to the list of covered edges
# 			# Edges are added as (smallest node, largest node) because we assume the graph
# 			# is undirected, and this method makes things easier.
# 			covered.add((min(x, hub), max(x, hub)))

# 			if (min(x, hub), max(x, hub)) in excluded:
# 					ignored.add((min(x, hub), max(x, hub)))

# 		# If the edge has been covered:
# 		else:

# 			# If the edge exists in A, but the model does not contain it, remove a modelling error
# 			if A[x][hub] == 1 and (min(x, hub), max(x, hub)) in modelledErrors:

# 				modelled -= 1

# 			# Otherwise, if the edge does not exist, but the model says it does, add a modelling error
# 			elif A[x][hub] == 0 and (min(x, hub), max(x, hub)) not in modelledErrors:

# 				modelled += 1

# 			if (min(x, hub), max(x, hub)) in excluded:
# 					ignored.add((min(x, hub), max(x, hub)))

# 	return ErrorPrefix(len(A), len(covered), len(ignored), modelled, unmodelled)