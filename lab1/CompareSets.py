def CompareSets(A, B):
    #Computes Jaccard similarity between 2 sets of hashed shinglings
    return len(A.intersection(B)) / len(A.union(B)) if len(A.union(B)) != 0 else 0