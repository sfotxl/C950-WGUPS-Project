# HashTable class
class HashTable:
    # Constructor with initial capacity parameter.
    # Assigns 40 buckets with empty list.
    def __init__(self, initial_size=40):
        self.size = initial_size
        self.table = []
        for i in range (initial_size):
            self.table.append([])

    # Hash function to generate an index for the key using modulo
    def _hash(self, key):
        return int(key) % self.size

    # Insert a new item into the hash table.
    def insert(self, key, item):
        # Determine the bucket for the key
        index = self._hash(key)
        bucket = self.table[index]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                bucket[i] = (key, item)
                return
        # Insert the new key-value pair
        bucket.append((key, item))

    # Lookup function tha returns the package for a given key
    def get(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                return v
        return None

    # Prints all buckets of the hashtable - this is for debugging
    def print_all_buckets(self):
        for i in self.table:
            print(f'BUCKET {i[0][0]}:\n'
                  f'{i[0][1]}')
