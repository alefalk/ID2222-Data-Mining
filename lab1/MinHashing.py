import random

class MinHashing:
    def __init__(self, num_hashes):
        """
        This class build a MinHash signature in the form of a vector of length num_hashes, which
        is set to 100 for this project. For a given set of hashed shingles. 

        Attirbutes:
            - num_hashes: The desired length of the signature, i.e. the number of hash functions to use when creating the signature
            - c: A large prime number to use for modulo in the hash functions, to reduce hash collisions
            - coefficients: Tuples (a, b), coefficients to use in the hash functions

        Methods:
            - hash(x, a, b): Computes the hash value of a shingle
            - get_signature(shingle_hashes): Computes MinHash signature for a given set of hashed shingles
        """
        self.num_hashes = num_hashes
        self.c = 109345121  # A large prime number for modulo
        # Generate random (a, b) pairs to create num_hashes independent hash functions
        self.coefficients = [(random.randint(1, self.c - 1), random.randint(0, self.c - 1)) for _ in range(num_hashes)]

    def hash(self, x, a, b):
        # Hash function: (a * x + b) % c
        return (a * x + b) % self.c

    def get_signature(self, shingle_hashes):
        signature = []
        # For each of the k hash functions
        for a, b in self.coefficients:
            # Calculate min hash value for the current hash function across all shingles
            min_hash = min(self.hash(shingle, a, b) for shingle in shingle_hashes)
            signature.append(min_hash)
        return signature
