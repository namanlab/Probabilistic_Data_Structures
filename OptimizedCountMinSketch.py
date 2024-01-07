import hashlib
import math

class OptimizedCountMinSketch:
    def __init__(self, epsilon, delta):
        """
        Initialize the Count-Min Sketch with specified width and depth.

        :param epsilon: Quantifies the max deviation from true count (epsilon * n)
        :param delta: To compute the probabilistic guarantee
        """
        self.epsilon = epsilon
        self.delta = delta
        self.width, self.depth = self._calculate_parameters(epsilon, delta)
        self.counters = [[0] * self.width for _ in range(self.depth)]

    def update(self, item, count=1):
        """
        Update the Count-Min Sketch with the occurrence of an item.

        :param item: The item to be counted.
        :param count: The count or frequency of the item (default is 1).
        """
        for i in range(self.depth):
            index = self._hash_function(item, i) % self.width
            self.counters[i][index] += count

    def estimate(self, item):
        """
        Estimate the count or frequency of an item in the Count-Min Sketch.

        :param item: The item to estimate the count for.

        :return: The estimated count of the item.
        """
        min_count = float('inf')
        for i in range(self.depth):
            index = self._hash_function(item, i) % self.width
            min_count = min(min_count, self.counters[i][index])
        return min_count

    def _calculate_parameters(self, epsilon, delta):
        """
        To calculate the optimal parameters m and k based on s and e.

        :param epsilon: Quantifies the max deviation from true count (epsilon * n)
        :param delta: To compute the probabilistic guarantee

        :return: Tuple (m, k) representing the optimal parameters.
        """
        m = math.ceil(math.e/epsilon)
        k = math.ceil(math.log(1/delta))
        return m, k

    def _hash_function(self, item, index):
        """
        To compute the hash function for a given item and index.

        :param item: The item to be hashed.
        :param index: The index used to vary the input to the hash function.

        :return: An integer value obtained by hashing the concatenated string of item and index.
        """
        hash_object = hashlib.sha256()
        hash_object.update((str(item) + str(index)).encode('utf-8'))
        return int.from_bytes(hash_object.digest(), byteorder='big')

# Example usage:
eps = 0.01
delta = 0.05

optimized_count_min_sketch = OptimizedCountMinSketch(eps, delta)

# Update the sketch with occurrences of items
optimized_count_min_sketch.update("apple", 3)
optimized_count_min_sketch.update("banana", 5)
optimized_count_min_sketch.update("orange", 2)

# Estimate counts for items
print(count_min_sketch.estimate("apple"))    # Estimated count for "apple"
print(count_min_sketch.estimate("grape"))    # Estimated count for "grape" (not updated)
