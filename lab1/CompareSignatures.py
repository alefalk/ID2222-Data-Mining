import numpy as np

# Function to compute approximate Jaccard similarity between MinHash signatures
def compare_signatures(sig1, sig2):
    return np.sum(np.array(sig1) == np.array(sig2)) / len(sig1)