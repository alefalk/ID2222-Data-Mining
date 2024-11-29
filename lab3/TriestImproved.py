from collections import defaultdict
import random

class TriestImproved:
    """
        This class implements the TRIEST-Improved algorithm.

        Attributes:
            - M: an integer which determines the maximum reservoir size
            - neighbors: defaultdict of sets storing the neighbors of a node, used to find common neighbors between nodes
            - S: Reservoir which holds the sampled edges
            - tau_global: Global triangle counter
            - t: number of edges currently processed
            - tau_local: Local triangle counter
    """
    def __init__(self, M):
        self.M = M  
        self.neighbors = defaultdict(set)  
        self.S = set()  
        self.tau_global = 0  
        self.t = 0  
        self.tau_local = defaultdict(int)

    def sample_edge(self):
        """
        Decide whether to sample the edge (u, v) based on the algorithm.

        Returns:
            bool: True if the edge is sampled, False otherwise.
        """
        if self.t <= self.M:
            return True  # Reservoir not full, always sample
        else:
            # Biased coin
            if random.random() < self.M / self.t:
                # Replace a random edge from the reservoir
                random_edge = random.choice(list(self.S))
                self.S.remove(random_edge)
                random_u, random_v = random_edge
                self.neighbors[random_u].remove(random_v)
                self.neighbors[random_v].remove(random_u)
                return True
        return False

    def update_counters(self, u, v, increment):
        """
        Method for updating counters when adding or removing an edge.

        Args:
            u, v: Nodes forming the edge.
            increment (int): value of eta for increment of counters
        """
        # Common neighbors is the intersection of the node's neighbors
        common_neighbors = self.neighbors[u] & self.neighbors[v]

        # Update triangle counts
        for c in common_neighbors:
            self.tau_local[c] += increment
            self.tau_local[u] += increment
            self.tau_local[v] += increment
            self.tau_global += increment

    def process_edge(self, u, v):
        """
        Method for processing a new edge (u, v) in the graph.

        Args:
            u, v: Nodes forming the edge.
        """
        self.t += 1
        eta = max(1, (self.t - 1) * (self.t - 2) / (self.M * (self.M - 1)))
        self.update_counters(u, v, eta)

        if self.sample_edge():
            self.S.add((u, v))
            self.neighbors[u].add(v)
            self.neighbors[v].add(u)

