from Shingling import hashing
from CompareSignatures import compare_signatures
from collections import defaultdict

class lsh:
    """
    This class finds pairs of similar documents based on their MinHash signatures using the LSH technique

    Attributes:
        - minhash_signatures: List of MinHash signatures for each document
        - threshold: The similarity threshold used to filter candidate pairs
        - band: The number of bands to split the signatures into
        - rows_per_band: The number of rows per band.
        - buckets: list of defaultdicts where each band has a dictionary mapping bands to document IDs

    Methods:
        - get_buckets(): Divides MinHash signatures into band and hashes each band into a bucket, grouping similar signatures
        - find_candidate_pairs(): Finds candidate pairs by finding documents that hash to the same bucket in at least one band
        - filter_candidate_pairs(): Filters candidate pairs based on the similarity threshold
    """
    def __init__ (self, minhash_signatures, threshold, bands, rows_per_band):
        self.minhash_signatures = minhash_signatures
        self.threshold = threshold
        self.bands = bands
        self.rows_per_band = rows_per_band
        self.buckets = self.get_buckets()

    def get_buckets(self):
        buckets = [defaultdict(list) for _ in range(self.bands)]

        for id, minhash_signature in enumerate(self.minhash_signatures):
            for band in range(self.bands):
                start = band * self.rows_per_band
                end = self.rows_per_band * (1 + band)
                band_tup = tuple(minhash_signature[start:end])
                hashkey_bucket = hashing(str(band_tup))
                buckets[band][hashkey_bucket].append(id)

        return buckets
    
    def find_candidate_pairs(self):
        candidate_pairs = set()
        for bucket in self.buckets:
            for id in bucket.values():
                # for a candidate pair we want them to hash to at least 1 common bucket
                if len(id) > 1:
                    # if so, add unique pairs of document IDs in this bucket as a candidate pair
                    for i in range(len(id)):
                        for j in range(i+1, len(id)):
                            candidate_pairs.add((id[i], id[j]))

        return list(candidate_pairs)
    
    def filter_candidate_pairs(self):
        filtered_candidates = []
        candidate_pairs = self.find_candidate_pairs()

        for i,j in candidate_pairs:
            similarity = compare_signatures(self.minhash_signatures[i], self.minhash_signatures[j])
            if similarity > self.threshold:
                filtered_candidates.append((i, j, similarity))
                
        return filtered_candidates