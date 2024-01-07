import math
import hashlib
from bitarray import bitarray

class OptimizedBloomFilter:
    def __init__(self, n=10000, p=0.05):
        """
        Initialize the Optimized Bloom Filter with dynamically calculated parameters.

        :param n: Expected number of elements to be added.
        :param p: Acceptable false positive rate.
        """
        self.n = n
        self.p = p
        self.m, self.k = self._calculate_parameters(n, p)

        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)

    def add(self, item):
        """
        Add an element to the Optimized Bloom Filter.

        :param item: The item to be added to the Bloom Filter.
        """
        for i in range(self.k):
            index = self._hash_function(item, i) % self.m
            self.bit_array[index] = 1

    def contains(self, item):
        """
        Check if an element is likely to be in the Optimized Bloom Filter.

        :param item: The item to check for presence in the Bloom Filter.

        :return: True if the element is likely present, False otherwise.
        """
        for i in range(self.k):
            index = self._hash_function(item, i) % self.m
            if not self.bit_array[index]:
                return False
        return True

    def _calculate_parameters(self, n, p):
        """
        To calculate the optimal parameters m and k based on n and p.

        :param n: Expected number of elements.
        :param p: Acceptable false positive rate.

        :return: Tuple (m, k) representing the optimal parameters.
        """
        m = - (n * math.log(p)) / (math.log(2) ** 2)
        k = (m / n) * math.log(2)
        return round(m), round(k)

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
expected_elements = 2000000
false_positive_rate = 0.01

optimized_bloom_filter = OptimizedBloomFilter(expected_elements, false_positive_rate)

# Add elements to the Optimized Bloom Filter
optimized_bloom_filter.add("apple")
optimized_bloom_filter.add("banana")
optimized_bloom_filter.add("orange")

# Check if elements are present in the Optimized Bloom Filter
print(optimized_bloom_filter.contains("apple"))    # True
print(optimized_bloom_filter.contains("grape"))    # False (not added)
