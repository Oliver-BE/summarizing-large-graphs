
quality = dict()

def Plain (A, candidates):
    # Returns a summary of all candidates M = C
    for candidate in candidates:
        Model += candidate
    return Model

def Top_k (A, candidates, k):
    count = 0
    for key in qualitySort(candidates):
          if (count < k):
              Model += quality[key] # not sure how to 'add' to the model
              count+=1
   
    # Sorts candidate structures decreasing by quality (encoding cost), then selects top k structures
    return Model

def GreedyNForget (A, candidates):
    # Sorts candidate structures decreasing by quality, and iterates sequentially through them
    # If total encoded cost of graph M does not increase, keep; otherwise remove.
    totalCost = 0
    for key in qualitySort(candidates):
        pass #DO something, not sure what

    

def qualitySort(candidates):
    for candidate in candidates:
        quality[getCost(candidate)].append(candidate) #need to create, basically just adds error cost and encoding cost
    return sorted(quality, reverse = True)
