import hashlib

def hashing(s):
    return int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)

class Shingling:
    """
    This class constructs k-shingles of a specified length (k) from a given document.
    In this project, we used k = 5. It then computes a hash value for each unique 
    shingle, representing the document as a set of these hashed k-shingles.
    
    Attributes:
    - document: The input document (e.g., an SMS message).
    - k: The length of each shingle.
    - shingle_hashes: The set of unique hashed shingles for the document.
    
    Methods:
    - compute_shingle_hashes: Creates the set of hashed k-shingles for the document.
    """
    def __init__(self, document, k):
        self.document = document
        self.k = k
        self.shingle_hashes = self.compute_shingle_hashes()

    def compute_shingle_hashes(self):
        """Creates a set of k-shingles from the document."""
        #set() only stores unique values
        shingle_hashes = set()
        # Loop over the document to create k-shingles
        for i in range(len(self.document) - self.k + 1):
            shingle = self.document[i:i + self.k]
            hashed_shingle = hashing(shingle)
            shingle_hashes.add(hashed_shingle)
        return shingle_hashes
    
        