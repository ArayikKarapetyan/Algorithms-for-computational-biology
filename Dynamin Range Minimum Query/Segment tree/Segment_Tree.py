class SegmentTreeRMQ:
    def __init__(self, arr):
        self.n = len(arr)
        # Size: next power of 2 * 2, or 4*n for safety
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        
        self.tree = [float('inf')] * (2 * self.size)
        
        # Fill leaves
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        
        # Build internal nodes
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = min(self.tree[2*i], self.tree[2*i + 1])
    
    def update(self, pos, value):
        """Update element at position pos - O(log n)"""
        pos += self.size
        self.tree[pos] = value
        pos //= 2
        
        while pos >= 1:
            self.tree[pos] = min(self.tree[2*pos], self.tree[2*pos + 1])
            pos //= 2
    
    def query(self, l, r):
        """Query minimum in range [l, r] - O(log n)"""
        l += self.size
        r += self.size
        res = float('inf')
        
        while l <= r:
            if l % 2 == 1:
                res = min(res, self.tree[l])
                l += 1
            if r % 2 == 0:
                res = min(res, self.tree[r])
                r -= 1
            l //= 2
            r //= 2
        
        return res

# Usage
arr = [5, 2, 8, 1, 9, 3, 7, 4]
rmq = SegmentTreeRMQ(arr)
print(rmq.query(1, 4))  # Output: 1
rmq.update(3, 10)       # Change arr[3] from 1 to 10
print(rmq.query(1, 4))  # Output: 2