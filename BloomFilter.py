import hashlib
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size, hash_functions):
        """
        Initialize the Bloom Filter with a given size and number of hash functions.

        :param size: Size of the Bloom Filter (number of bits in the bit array).
        :param hash_functions: Number of hash functions to use.
        """
        self.size = size
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        self.hash_functions = hash_functions

    def add(self, item):
        """
        Add an element to the Bloom Filter.

        :param item: The item to be added to the Bloom Filter.
        """
        for i in range(self.hash_functions):
            # Calculate the index using the hash function and update the corresponding bit to 1.
            index = self._hash_function(item, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        """
        Check if an element is likely to be in the Bloom Filter.

        :param item: The item to check for presence in the Bloom Filter.

        :return: True if the element is likely present, False otherwise.
        """
        for i in range(self.hash_functions):
            # Calculate the index using the hash function.
            index = self._hash_function(item, i) % self.size
            # If any corresponding bit is 0, the item is definitely not in the set.
            if not self.bit_array[index]:
                return False
        # If all corresponding bits are 1, the item is likely in the set.
        return True

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
size = 10  # Size of the Bloom Filter
hash_functions = 3  # Number of hash functions

bloom_filter = BloomFilter(size, hash_functions)

# Add elements to the Bloom Filter
bloom_filter.add("apple")
bloom_filter.add("banana")
bloom_filter.add("orange")

# Check if elements are present in the Bloom Filter
print(bloom_filter.contains("apple"))    # True
print(bloom_filter.contains("grape"))    # False (not added)