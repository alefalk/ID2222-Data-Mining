import numpy as np
from collections import Counter
from itertools import combinations
class apriori():
    def __init__(self, baskets, s):
        self.baskets = baskets
        self.s = s

    def get_frequent_itemsets(self):
        """
            This method finds frequent itemsets of size k. We set k to 1 from the start in order to find frequent singletons,
            k is then incremented for each iteration of the while loop. Making it able to find itemsets of all sizes.
            If the length of frequent_itemsets is 0 for a value k after filtering on the support threshold, 
            we can deduce that no higher value of k will find frequent itemsets that meet the threshold. 

            Returns:
                A list, all_frequent_itemsets, of dictionaries where each dictionary contains frequent itemsets
                of a particular size and their counts
        """
        
        # initialize k
        k = 1
        # arbitrary initial value in order to start the loop
        frequent_itemsets = {1}
        all_frequent_itemsets = []
        
        while len(frequent_itemsets) != 0:
            itemset_counts = Counter()
            
            for basket in self.baskets:
                # Generate all possible k-item combinations from the basket
                for itemset in combinations(basket, k):
                    itemset_counts[itemset] += 1

            # Filter itemsets that meet the minimum support threshold
            frequent_itemsets = {itemset: count for itemset, count in itemset_counts.items() if count >= self.s}
            all_frequent_itemsets.append(frequent_itemsets) if len(frequent_itemsets) != 0 else None
            k += 1
        
        return all_frequent_itemsets
    
    def get_association_rules(self):
        all_frequent_itemsets = self.get_frequent_itemsets()
        rules = []
        min_confidence = 0.6
        for itemsets_of_size_k in all_frequent_itemsets:
            for itemset, itemset_count in itemsets_of_size_k.items():
                # Skip singletons (itemsets of size 1) as rules cannot be generated from them
                if len(itemset) < 2:
                    continue  

                # Generate association rules for itemsets of size >= 2
                for i in range(1, len(itemset)):
                    for antecedent in combinations(itemset, i):
                        consequent = tuple(sorted(set(itemset) - set(antecedent)))

                        # Calculate metrics
                        antecedent_count = all_frequent_itemsets[len(antecedent) - 1].get(antecedent, 0)
                        if antecedent_count == 0:
                            continue  # Avoid division by zero

                        support = itemset_count / len(self.baskets)
                        confidence = itemset_count / antecedent_count

                        # Apply thresholds
                        if confidence >= min_confidence:
                            rules.append({
                                'antecedent': antecedent,
                                'consequent': consequent,
                                'support': support,
                                'confidence': confidence,
                            })
        return rules
