import hashlib

class CountMinSketch:
    def __init__(self, m, k):
        """
        Initialize the Count-Min Sketch with specified width and depth.

        :param width: Number of counters in each hash function's array.
        :param depth: Number of hash functions.
        """
        self.width = m
        self.depth = k
        self.counters = [[0] * m for _ in range(k)]

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
m = 100
k = 5

count_min_sketch = CountMinSketch(m, k)

# Update the sketch with occurrences of items
count_min_sketch.update("apple", 3)
count_min_sketch.update("banana", 5)
count_min_sketch.update("orange", 2)

# Estimate counts for items
print(count_min_sketch.estimate("apple"))    # Estimated count for "apple"
print(count_min_sketch.estimate("grape"))    # Estimated count for "grape" (not updated)
