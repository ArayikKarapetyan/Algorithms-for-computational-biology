# Square Root Decomposition for Range Minimum Query (RMQ)

## 📌 Overview

**Square Root Decomposition** is a simple yet powerful technique for solving Range Minimum Query problems with a beautiful balance between:
* ⚡ **Query time:** O(√n)
* 🔄 **Update time:** O(√n)
* 🧠 **Simplicity:** Easy to understand and implement

It's the perfect middle ground between brute force and complex tree structures.

---

## 🎯 Main Idea

Instead of building a full tree (like Segment Tree) or a huge table (like Sparse Table), we:

1. Split the array into blocks of size ≈ √n
2. Precompute the minimum of each block
3. During a query:
   * Scan small partial blocks manually
   * Use precomputed minimums for full blocks

It's a **middle ground** between brute force and advanced trees.

---

## 🧠 Why √n?

If:

```
block_size ≈ √n
```

Then:
* Number of blocks ≈ √n
* Each block size ≈ √n

So:
* Query takes at most **√n work**
* Update takes at most **√n work**

Nice balance ⚖️

---

## 📦 Initialization

### Step 1: Calculate Block Size

```python
self.block_size = int(math.sqrt(self.n)) + 1
```

**For example:**

```
n = 8
√8 ≈ 2.8 → block_size = 3
```

### Step 2: Partition the Array

So array:

```
Index:  0 1 2 | 3 4 5 | 6 7
Value:  5 2 8 | 1 9 3 | 7 4
```

Blocks:

```
Block 0: [5,2,8]   → min = 2
Block 1: [1,9,3]   → min = 1
Block 2: [7,4]     → min = 4
```

### Step 3: Precompute Block Minimums

We store:

```python
block_min = [2, 1, 4]
```

### Complete Initialization Code

```python
import math

class SqrtDecompositionRMQ:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr[:]
        self.block_size = int(math.sqrt(self.n)) + 1
        self.num_blocks = (self.n + self.block_size - 1) // self.block_size
        self.block_min = [float('inf')] * self.num_blocks
        
        # Precompute block minimums
        for i in range(self.n):
            block_idx = i // self.block_size
            self.block_min[block_idx] = min(self.block_min[block_idx], arr[i])
```

**Time Complexity:** O(n)

---

## 🔎 Query(l, r)

Let's query:

```python
query(1, 6)
Range = [2, 8, 1, 9, 3, 7]
```

### Steps:

#### Step 1: Identify blocks

```python
left_block  = l // block_size
right_block = r // block_size
```

If block_size = 3:

```
left_block  = 1 // 3 = 0
right_block = 6 // 3 = 2
```

So we span blocks **0 → 2**.

---

### 🧩 Case 1: Same Block

If both indices are inside same block:

```python
query(1, 2)
```

We just **scan manually**.

```python
if left_block == right_block:
    for i in range(l, r + 1):
        res = min(res, self.arr[i])
```

---

### 🧩 Case 2: Different Blocks

We split into 3 parts:

```
| left partial | full blocks | right partial |
```

For `query(1, 6)`:

#### 1️⃣ Left Partial Block

From index 1 to end of block 0:

```
[2, 8]
```

Scan manually.

```python
end_left = (left_block + 1) * self.block_size
for i in range(l, min(end_left, self.n)):
    res = min(res, self.arr[i])
```

#### 2️⃣ Full Middle Blocks

Block 1 is completely inside:

```
Use block_min[1] = 1
```

```python
for b in range(left_block + 1, right_block):
    res = min(res, self.block_min[b])
```

#### 3️⃣ Right Partial Block

From start of block 2 to index 6:

```
[7]
```

Scan manually.

```python
start_right = right_block * self.block_size
for i in range(start_right, r + 1):
    res = min(res, self.arr[i])
```

#### Combine All:

```
min(left_scan, middle_blocks, right_scan)
= min(2, 1, 7)
= 1
```

Done!

---

## 📊 Visual Breakdown

```
Array:   [5  2  8  1  9  3  7  4]
Indices:  0  1  2  3  4  5  6  7

Query(1, 6) range: [2  8  1  9  3  7]

Blocks:
┌─────────┬─────────┬─────────┐
│ Block 0 │ Block 1 │ Block 2 │
│ [5,2,8] │ [1,9,3] │ [7,4]   │
│  min=2  │  min=1  │  min=4  │
└─────────┴─────────┴─────────┘
     ↑         ↑         ↑
   partial   FULL    partial
    [2,8]   min=1     [7]
```

---

## 🔄 Update(pos, value)

If we update:

```python
update(3, 10)
```

**Original:**

```
Block 1: [1, 9, 3]
```

**After update:**

```
Block 1: [10, 9, 3]
```

Now minimum changes!

### Steps:

#### 1. Update value in array

```python
self.arr[pos] = value
```

#### 2. Recompute entire block

```python
block_idx = pos // self.block_size
start = block_idx * self.block_size
end = min(start + self.block_size, self.n)

self.block_min[block_idx] = float('inf')
for i in range(start, end):
    self.block_min[block_idx] = min(self.block_min[block_idx], self.arr[i])
```

### Why recompute whole block?

Because we don't know if we removed the old minimum.

**Worst case cost:** O(√n)

---

## 💻 Complete Implementation

```python
import math

class SqrtDecompositionRMQ:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr[:]
        self.block_size = int(math.sqrt(self.n)) + 1
        self.num_blocks = (self.n + self.block_size - 1) // self.block_size
        self.block_min = [float('inf')] * self.num_blocks
        
        for i in range(self.n):
            block_idx = i // self.block_size
            self.block_min[block_idx] = min(self.block_min[block_idx], arr[i])
    
    def update(self, pos, value):
        """Update element at position pos to value"""
        self.arr[pos] = value
        block_idx = pos // self.block_size
        start = block_idx * self.block_size
        end = min(start + self.block_size, self.n)
        
        self.block_min[block_idx] = float('inf')
        for i in range(start, end):
            self.block_min[block_idx] = min(self.block_min[block_idx], self.arr[i])
    
    def query(self, l, r):
        """Query minimum in range [l, r]"""
        left_block = l // self.block_size
        right_block = r // self.block_size
        res = float('inf')
        
        if left_block == right_block:
            # Same block - scan manually
            for i in range(l, r + 1):
                res = min(res, self.arr[i])
        else:
            # Left partial block
            end_left = (left_block + 1) * self.block_size
            for i in range(l, min(end_left, self.n)):
                res = min(res, self.arr[i])
            
            # Full middle blocks
            for b in range(left_block + 1, right_block):
                res = min(res, self.block_min[b])
            
            # Right partial block
            start_right = right_block * self.block_size
            for i in range(start_right, r + 1):
                res = min(res, self.arr[i])
        
        return res
```

---

## 📊 Complexity

| Operation | Time |
|-----------|------|
| Preprocessing | O(n) |
| Query | O(√n) |
| Update | O(√n) |
| Space | O(n) |

---

## 🆚 Compared to Others

| Method | Query | Update | Notes |
|--------|-------|--------|-------|
| Brute Force | O(n) | O(1) | Simple |
| Sqrt Decomp | O(√n) | O(√n) | Easy + good |
| Segment Tree | O(log n) | O(log n) | Best practical |
| Sparse Table | O(1) | ❌ No updates | Static only |
| Cartesian + LCA | O(1) | ❌ No updates | Theoretical optimal static |

---

## 🧪 Example Execution

```python
# Initialize
arr = [5, 2, 8, 1, 9, 3, 7, 4]
rmq = SqrtDecompositionRMQ(arr)

# Query
print(rmq.query(1, 6))  # Output: 1
# Range [2, 8, 1, 9, 3, 7] → min = 1

# Update
rmq.update(3, 10)
# Array becomes [5, 2, 8, 10, 9, 3, 7, 4]

# Query again
print(rmq.query(1, 6))  # Output: 2
# Range [2, 8, 10, 9, 3, 7] → min = 2
```

---

## 🎯 When to Use Square Root Decomposition

### ✅ Use when:

* You need **both queries and updates**
* You want **simple, easy-to-code** solution
* You're in a **competitive programming** contest
* **Segment Tree** feels too complex
* Block-based algorithms are more intuitive to you

### ❌ Don't use when:

* You need **O(log n)** performance → use Segment Tree
* Array is **static** → use Sparse Table for O(1) queries
* You want **theoretically optimal** → use Cartesian Tree + LCA

---

## 🔧 Optimization: Tuning Block Size

### The Formula

```python
block_size = int(math.sqrt(self.n)) + 1
```

### But you can adjust!

#### For more queries, fewer updates:

```python
block_size = int(2 * math.sqrt(self.n))  # Larger blocks
```

* Queries: O(√n) → still good
* Updates: O(2√n) → slightly worse

#### For more updates, fewer queries:

```python
block_size = int(0.5 * math.sqrt(self.n))  # Smaller blocks
```

* Queries: O(2√n) → slightly worse
* Updates: O(√n/2) → better

---

## 📐 Mathematical Analysis

### Query Complexity

In worst case, we:
1. Scan **√n** elements in left partial block
2. Check **√n** full blocks
3. Scan **√n** elements in right partial block

Total: **O(3√n) = O(√n)**

### Update Complexity

We recompute one block of size **√n**.

Total: **O(√n)**

### Space Complexity

```
Array: n elements
Block minimums: √n elements
Total: O(n)
```

---

## 🧠 Key Insights

### 1. The Sweet Spot

√n is the **optimal balance** for block size:
* Too small → too many blocks
* Too large → scanning takes too long

### 2. Cache-Friendly

Sequential scanning of blocks is **cache-efficient**.

### 3. Easy to Extend

Can easily modify for:
* Range sum
* Range maximum
* Range GCD
* Any associative operation

---

## 🔄 Variations

### Range Sum Query

```python
# In __init__
self.block_sum = [0] * self.num_blocks

# In query
# Use sum instead of min
```

### Range Maximum Query

```python
# In __init__
self.block_max = [float('-inf')] * self.num_blocks

# In query
# Use max instead of min
```

### Range GCD Query

```python
import math

# In __init__
self.block_gcd = [0] * self.num_blocks

# In query
# Use math.gcd
```

---

## 🎓 Learning Path

1. **Understand** the block partitioning concept
2. **Implement** basic version
3. **Test** with small examples
4. **Optimize** block size for your use case
5. **Compare** with Segment Tree

---

## 📚 Further Reading

* [CP-Algorithms: Square Root Decomposition](https://cp-algorithms.com/data_structures/sqrt_decomposition.html)
* [Codeforces Tutorial](https://codeforces.com/blog/entry/20489)
* [HackerEarth Guide](https://www.hackerearth.com/practice/notes/square-root-decomposition/)

---

## 🧪 Testing Suite

```python
def test_sqrt_decomposition():
    arr = [5, 2, 8, 1, 9, 3, 7, 4]
    rmq = SqrtDecompositionRMQ(arr)
    
    # Test queries
    assert rmq.query(0, 0) == 5
    assert rmq.query(1, 4) == 1
    assert rmq.query(0, 7) == 1
    assert rmq.query(4, 6) == 3
    assert rmq.query(2, 3) == 1
    
    # Test updates
    rmq.update(3, 10)
    assert rmq.query(1, 4) == 2
    assert rmq.query(3, 5) == 3
    
    rmq.update(1, 0)
    assert rmq.query(0, 7) == 0
    
    print("All tests passed! ✅")

test_sqrt_decomposition()
```

---

## 💡 Practical Tips

### 1. Block Size Calculation

Always add **+1** to handle edge cases:

```python
block_size = int(math.sqrt(n)) + 1
```

### 2. Index Calculations

Be careful with:
```python
end_left = (left_block + 1) * block_size
# Don't forget min(end_left, n)
```

### 3. Initialization

Initialize with **infinity** for min queries:

```python
block_min = [float('inf')] * num_blocks
```

### 4. Edge Cases

Test with:
* n = 1 (single element)
* n = 2 (two elements)
* Query entire array
* Query single element

---

## ⭐ Key Takeaways

1. **√n decomposition** balances simplicity and performance
2. **O(√n)** for both queries and updates
3. **Easy to code** - great for contests
4. **Cache-friendly** - sequential scanning
5. **Flexible** - works for many operations
6. **Middle ground** - between brute force and trees

---

## 🏆 Competitive Programming Tips

### When to use in contests:

✅ Time limit is generous  
✅ You need quick implementation  
✅ Segment Tree seems overkill  
✅ You're comfortable with sqrt decomp  

### Template for contests:

```python
import math

def solve_rmq(arr, queries):
    n = len(arr)
    b = int(math.sqrt(n)) + 1
    blocks = (n + b - 1) // b
    bmin = [float('inf')] * blocks
    
    for i in range(n):
        bmin[i // b] = min(bmin[i // b], arr[i])
    
    results = []
    for l, r in queries:
        lb, rb = l // b, r // b
        res = float('inf')
        
        if lb == rb:
            res = min(arr[l:r+1])
        else:
            res = min(res, min(arr[l:(lb+1)*b]))
            res = min(res, min(bmin[lb+1:rb]))
            res = min(res, min(arr[rb*b:r+1]))
        
        results.append(res)
    
    return results
```

---

<div align="center">

**⚡ Simple, Elegant, Effective ⚡**

*The perfect balance between complexity and performance*

</div>