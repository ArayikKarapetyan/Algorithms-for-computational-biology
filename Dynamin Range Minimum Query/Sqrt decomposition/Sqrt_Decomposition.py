import math

class SqrtDecompositionRMQ:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr[:]
        self.block_size = int(math.sqrt(self.n)) + 1
        self.num_blocks = (self.n + self.block_size - 1) // self.block_size
        
        # Precompute min for each block
        self.block_min = [float('inf')] * self.num_blocks
        for i in range(self.n):
            block_idx = i // self.block_size
            self.block_min[block_idx] = min(self.block_min[block_idx], arr[i])
    
    def update(self, pos, value):
        """Update element at position pos - O(√n) worst case"""
        self.arr[pos] = value
        
        # Recompute entire block's minimum
        block_idx = pos // self.block_size
        start = block_idx * self.block_size
        end = min(start + self.block_size, self.n)
        
        self.block_min[block_idx] = float('inf')
        for i in range(start, end):
            self.block_min[block_idx] = min(self.block_min[block_idx], self.arr[i])
    
    def query(self, l, r):
        """Query minimum in range [l, r] - O(√n)"""
        left_block = l // self.block_size
        right_block = r // self.block_size
        res = float('inf')
        
        if left_block == right_block:
            # Same block - scan directly
            for i in range(l, r + 1):
                res = min(res, self.arr[i])
        else:
            # Left partial block
            end_left = (left_block + 1) * self.block_size
            for i in range(l, min(end_left, self.n)):
                res = min(res, self.arr[i])
            
            # Middle complete blocks
            for b in range(left_block + 1, right_block):
                res = min(res, self.block_min[b])
            
            # Right partial block
            start_right = right_block * self.block_size
            for i in range(start_right, r + 1):
                res = min(res, self.arr[i])
        
        return res

# Usage
arr = [5, 2, 8, 1, 9, 3, 7, 4]
rmq = SqrtDecompositionRMQ(arr)
print(rmq.query(1, 4))  # Output: 1
rmq.update(3, 10)
print(rmq.query(1, 4))  # Output: 2