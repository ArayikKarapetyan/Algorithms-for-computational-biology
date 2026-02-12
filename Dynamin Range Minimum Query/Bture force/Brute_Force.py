class BruteForceRMQ:
    def __init__(self, arr):
        self.arr = arr
    
    def query(self, l, r):
        """Query minimum in range [l, r] - O(n) per query"""
        return min(self.arr[l:r+1])

# Usage
arr = [5, 2, 8, 1, 9, 3, 7, 4]
rmq = BruteForceRMQ(arr)
print(rmq.query(1, 4))  # Output: 1 (min of [2, 8, 1, 9])
print(rmq.query(0, 7))  # Output: 1