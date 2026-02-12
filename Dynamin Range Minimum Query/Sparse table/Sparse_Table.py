import math

class SparseTableRMQ:
    def __init__(self, arr):
        self.n = len(arr)
        self.log = [0] * (self.n + 1)
        
        # Precompute logarithms
        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1
        
        # Build sparse table: st[j][i] = min of arr[i..i+2^j-1]
        self.K = self.log[self.n] + 1
        self.st = [[0] * self.n for _ in range(self.K)]
        
        # Initialize for intervals of length 1
        for i in range(self.n):
            self.st[0][i] = arr[i]
        
        # Build table for larger intervals
        for j in range(1, self.K):
            for i in range(self.n - (1 << j) + 1):
                # Min of two overlapping halves
                self.st[j][i] = min(self.st[j-1][i], 
                                   self.st[j-1][i + (1 << (j-1))])
    
    def query(self, l, r):
        """Query minimum in range [l, r] - O(1)"""
        j = self.log[r - l + 1]
        # Overlapping intervals (works because min is idempotent)
        return min(self.st[j][l], self.st[j][r - (1 << j) + 1])

# Usage
arr = [5, 2, 8, 1, 9, 3, 7, 4]
rmq = SparseTableRMQ(arr)
print(rmq.query(1, 4))  # Output: 1
print(rmq.query(0, 7))  # Output: 1