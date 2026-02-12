# Dynamic Range Minimum Query (RMQ) Algorithms

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Algorithms](https://img.shields.io/badge/Category-Algorithms-orange.svg)]()
[![Complexity](https://img.shields.io/badge/Complexity-Analysis-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

**A comprehensive collection of Range Minimum Query algorithms with detailed implementations, complexity analysis, and comparative benchmarks.**


</div>

---

## 📋 Table of Contents

- [Introduction](#Introduction)
- [Getting Started](#getting-started)
- [Algorithms Overview](#algorithms-overview)
  - [1. Brute Force](#1-brute-force)
  - [2. Sparse Table](#2-sparse-table)
  - [3. Segment Tree](#3-segment-tree)
  - [4. Square Root Decomposition](#5-square-root-decomposition)
  - [5. Cartesian Tree + LCA](#6-cartesian-tree--lca-schieber-vishkin)

- [Complexity Comparison](#complexity-comparison)
- [Usage Examples](#usage-examples)
- [When to Use Which](#when-to-use-which)
- [Mathematical Foundations](#mathematical-foundations)
- [Contributing](#contributing)

---

## Introduction

The **Range Minimum Query (RMQ)** problem is a fundamental algorithmic challenge in computer science with applications in:

- **Bioinformatics**: Finding lowest common ancestors in phylogenetic trees
- **Text Processing**: Longest common prefix queries in suffix arrays
- **Computational Geometry**: Range searching and proximity queries
- **Database Systems**: Efficient range aggregation operations

> **Problem Statement**: Given a static array $A$ of size $n$, preprocess the data to answer multiple queries of the form $\text{RMQ}(l, r) = \min\{A[l], A[l+1], \ldots, A[r]\}$ efficiently.

---

## Getting Started

### Prerequisites

```bash
python >= 3.8
```


### Quick Start

```python
from implementations import SparseTableRMQ, SegmentTreeRMQ

# Initialize with your array
arr = [5, 2, 8, 1, 9, 3, 7, 4]

# Static queries - O(1) per query
rmq = SparseTableRMQ(arr)
print(rmq.query(1, 4))  # Output: 1

# Dynamic updates needed - O(log n) per operation
dynamic_rmq = SegmentTreeRMQ(arr)
dynamic_rmq.update(3, 10)
print(dynamic_rmq.query(1, 4))  # Output: 2
```

---

## Algorithms Overview

### 1. Brute Force

The naive approach without any preprocessing. Suitable only for educational purposes or when query count is extremely small.

**Algorithm:**
```
Query(l, r):
    min_val ← ∞
    for i from l to r:
        min_val ← min(min_val, A[i])
    return min_val
```

**Characteristics:**
- ✅ No preprocessing overhead
- ✅ O(1) memory usage
- ❌ Impractical for multiple queries
- ❌ O(n) per query makes it O(n·q) for q queries

**Use Case:** Single or very few queries on small datasets.

```python
class BruteForceRMQ:
    def __init__(self, arr):
        self.arr = arr
    
    def query(self, l, r):
        return min(self.arr[l:r+1])
```

---

### 2. Sparse Table

The gold standard for static RMQ problems. Utilizes the idempotent property of the minimum operation (min(x,x) = x) to enable overlapping intervals.

**Key Insight:**

For any range [l,r], let k = ⌊log₂(r−l+1)⌋. The range can be covered by two overlapping intervals of length 2^k:
- [l, l+2^k−1]
- [r−2^k+1, r]

RMQ(l,r) = min(st[k][l], st[k][r−2^k+1])

**Precomputation:**
```
st[j][i] = min of A[i..i+2^j-1]
st[0][i] = A[i]
st[j][i] = min(st[j-1][i], st[j-1][i+2^(j-1)])
```

**Characteristics:**
- ✅ O(1) query time - optimal for static data
- ✅ Simple implementation
- ✅ Cache-friendly memory layout
- ❌ No updates possible - requires full rebuild
- ❌ O(n log n) space complexity

**Space-Time Tradeoff:**

Space = n·⌈log₂ n⌉ integers. For n=10⁶, this is approximately 20MB (assuming 4-byte integers).

```python
import math

class SparseTableRMQ:
    def __init__(self, arr):
        self.n = len(arr)
        self.log = [0] * (self.n + 1)
        
        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1
        
        self.K = self.log[self.n] + 1
        self.st = [[0] * self.n for _ in range(self.K)]
        
        for i in range(self.n):
            self.st[0][i] = arr[i]
        
        for j in range(1, self.K):
            for i in range(self.n - (1 << j) + 1):
                self.st[j][i] = min(self.st[j-1][i], 
                                   self.st[j-1][i + (1 << (j-1))])
    
    def query(self, l, r):
        j = self.log[r - l + 1]
        return min(self.st[j][l], self.st[j][r - (1 << j) + 1])
```

---

### 3. Segment Tree

A complete binary tree where each node represents an interval of the array. The most versatile RMQ structure, supporting both queries and updates in logarithmic time.

**Tree Structure:**
- Leaf nodes: Individual array elements
- Internal nodes: Minimum of their two children
- Height: ⌈log₂ n⌉

**Operations:**

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Build | O(n) | Bottom-up construction |
| Query | O(log n) | Traverse tree, combine relevant nodes |
| Update | O(log n) | Update leaf, propagate changes upward |

**Query Algorithm:**
```
Query(node, node_l, node_r, query_l, query_r):
    if query_l > node_r or query_r < node_l:
        return ∞                           # No overlap
    if query_l <= node_l and node_r <= query_r:
        return tree[node]                  # Total overlap
    mid ← (node_l + node_r) // 2          # Partial overlap
    return min(Query(left_child, ...), Query(right_child, ...))
```

**Characteristics:**
- ✅ O(log n) query and update
- ✅ Flexible and extensible (supports sum, max, etc.)
- ✅ Optimal for dynamic scenarios
- ❌ Higher constant factors than Sparse Table
- ❌ ~4n space requirement

```python
class SegmentTreeRMQ:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        
        self.tree = [float('inf')] * (2 * self.size)
        
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = min(self.tree[2*i], self.tree[2*i + 1])
    
    def update(self, pos, value):
        pos += self.size
        self.tree[pos] = value
        pos //= 2
        while pos >= 1:
            self.tree[pos] = min(self.tree[2*pos], self.tree[2*pos + 1])
            pos //= 2
    
    def query(self, l, r):
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
```

---


### 4. Square Root Decomposition

A hybrid approach combining the simplicity of brute force with the efficiency of block preprocessing. The array is divided into blocks of size ≈ √n.

**Structure:**
- Block size: b = ⌈√n⌉
- Number of blocks: ⌈n/b⌉ ≈ √n
- Precompute minimum for each block

**Query Processing:**
1. Left partial block: Scan elements from l to end of its block
2. Middle complete blocks: Use precomputed block minima
3. Right partial block: Scan elements from start of block to r

Query time = O(b) + O(n/b) + O(b) = O(√n)

**Characteristics:**
- ✅ Simple implementation
- ✅ Cache-efficient for small arrays
- ✅ Updates in O(√n)
- ❌ O(√n) query slower than O(log n) alternatives
- ❌ Tuning block size required for optimal performance

**Optimization:**

Block size can be tuned based on query vs. update frequency. More updates → smaller blocks; more queries → larger blocks.

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
        self.arr[pos] = value
        block_idx = pos // self.block_size
        start = block_idx * self.block_size
        end = min(start + self.block_size, self.n)
        
        self.block_min[block_idx] = float('inf')
        for i in range(start, end):
            self.block_min[block_idx] = min(self.block_min[block_idx], self.arr[i])
    
    def query(self, l, r):
        left_block = l // self.block_size
        right_block = r // self.block_size
        res = float('inf')
        
        if left_block == right_block:
            for i in range(l, r + 1):
                res = min(res, self.arr[i])
        else:
            end_left = (left_block + 1) * self.block_size
            for i in range(l, min(end_left, self.n)):
                res = min(res, self.arr[i])
            
            for b in range(left_block + 1, right_block):
                res = min(res, self.block_min[b])
            
            start_right = right_block * self.block_size
            for i in range(start_right, r + 1):
                res = min(res, self.arr[i])
        
        return res
```

---

### 5. Cartesian Tree + LCA (Schieber-Vishkin)

The theoretically optimal solution achieving O(n) preprocessing and O(1) query time. Reduces RMQ to Lowest Common Ancestor (LCA) on a specially constructed tree.

**Cartesian Tree Properties:**
- Heap property: Parent value < Children values (min-heap)
- Inorder traversal: Yields the original array sequence
- Root: Minimum element of the entire array

**Key Theorem:**

For indices i < j in the original array:

RMQ(i,j) = value[LCA(node_i, node_j)]

**Algorithm Steps:**
1. Build Cartesian Tree: O(n) using monotonic stack
2. Euler Tour: Generate tour of tree with depths
3. ±1 RMQ: Apply specialized O(1) RMQ on the Euler tour (adjacent depths differ by ±1)

**The ±1 RMQ Optimization:**

Since adjacent elements in the Euler tour depth array differ by exactly 1, we can use:
- Indirection: Divide into blocks of size ½log n
- Precompute all possible ±1 sequences (only 2^(½log n) = √n possibilities)
- Block queries: O(1) using lookup tables

**Characteristics:**
- ✅ Optimal O(n) preprocessing, O(1) query
- ✅ O(n) space complexity
- ❌ Complex implementation
- ❌ No updates (tree structure depends on values)
- ❌ High constant factors (practical only for very large n)

```python
class CartesianTreeLCA_RMQ:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr
        self._build_cartesian_tree()
        self._euler_tour()
        self._build_sparse_table_on_euler()
    
    def _build_cartesian_tree(self):
        self.parent = [-1] * self.n
        self.left = [-1] * self.n
        self.right = [-1] * self.n
        stack = []
        
        for i in range(self.n):
            last = -1
            while stack and self.arr[stack[-1]] > self.arr[i]:
                last = stack.pop()
            
            if stack:
                self.parent[i] = stack[-1]
                self.right[stack[-1]] = i
            if last != -1:
                self.parent[last] = i
                self.left[i] = last
            stack.append(i)
        
        self.root = next(i for i in range(self.n) if self.parent[i] == -1)
    
    def _euler_tour(self):
        self.euler = []
        self.depth = []
        self.first = [-1] * self.n
        
        def dfs(node, d):
            if node == -1:
                return
            if self.first[node] == -1:
                self.first[node] = len(self.euler)
            self.euler.append(node)
            self.depth.append(d)
            
            if self.left[node] != -1:
                dfs(self.left[node], d + 1)
                self.euler.append(node)
                self.depth.append(d)
            if self.right[node] != -1:
                dfs(self.right[node], d + 1)
                self.euler.append(node)
                self.depth.append(d)
        
        dfs(self.root, 0)
        self.euler_size = len(self.euler)
    
    def _build_sparse_table_on_euler(self):
        self.log = [0] * (self.euler_size + 1)
        for i in range(2, self.euler_size + 1):
            self.log[i] = self.log[i // 2] + 1
        
        K = self.log[self.euler_size] + 1
        self.st = [[0] * self.euler_size for _ in range(K)]
        self.st_idx = [[0] * self.euler_size for _ in range(K)]
        
        for i in range(self.euler_size):
            self.st[0][i] = self.depth[i]
            self.st_idx[0][i] = i
        
        for j in range(1, K):
            for i in range(self.euler_size - (1 << j) + 1):
                if self.st[j-1][i] <= self.st[j-1][i + (1 << (j-1))]:
                    self.st[j][i] = self.st[j-1][i]
                    self.st_idx[j][i] = self.st_idx[j-1][i]
                else:
                    self.st[j][i] = self.st[j-1][i + (1 << (j-1))]
                    self.st_idx[j][i] = self.st_idx[j-1][i + (1 << (j-1))]
    
    def _lca_query(self, u, v):
        if self.first[u] > self.first[v]:
            u, v = v, u
        l, r = self.first[u], self.first[v]
        j = self.log[r - l + 1]
        
        if self.st[j][l] <= self.st[j][r - (1 << j) + 1]:
            return self.euler[self.st_idx[j][l]]
        else:
            return self.euler[self.st_idx[j][r - (1 << j) + 1]]
    
    def query(self, l, r):
        lca_node = self._lca_query(l, r)
        return self.arr[lca_node]
```

---


## 📊 Complexity Comparison

| Algorithm | Preprocessing | Query | Update | Space | Static/Dynamic |
|-----------|---------------|-------|--------|-------|----------------|
| Brute Force | O(1) | O(n) | O(1) | O(1) | Dynamic |
| Sparse Table | O(n log n) | O(1) | ❌ | O(n log n) | Static |
| Segment Tree | O(n) | O(log n) | O(log n) | O(n) | Dynamic |
| Sqrt Decomposition | O(n) | O(√n) | O(√n) | O(n) | Dynamic |
| Cartesian Tree + LCA | O(n) | O(1) | ❌ | O(n) | Static |

*Limited to prefix queries with standard implementation  
†Expected time, randomized

### Theoretical Limits

- **Static RMQ**: ⟨O(n), O(1)⟩ is optimal (achieved by Cartesian Tree + LCA)
- **Dynamic RMQ**: ⟨O(n), O(log n), O(log n)⟩ is optimal for comparison-based algorithms

---

## 💡 When to Use Which

### Decision Tree

```
Is the array static (no updates)?
├── YES → Is code simplicity priority?
│   ├── YES → Sparse Table
│   └── NO → Cartesian Tree + LCA (very large n)
└── NO → Are updates frequent?
    ├── YES → Segment Tree
    └── NO → Sqrt Decomposition (simple, cache-friendly)
```

### Practical Recommendations

| Scenario | Recommended Algorithm | Reason |
|----------|----------------------|--------|
| Competitive Programming (static) | Sparse Table | O(1) query, easy to code |
| Production System (dynamic) | Segment Tree | Balanced performance, well-tested |
| Very large n, few queries | Brute Force | Avoid preprocessing overhead |
| Educational purposes | All | Compare and understand tradeoffs |
| Cache-sensitive environment | Sqrt Decomposition | Better locality than pointer-based trees |
| Theoretical analysis | Cartesian Tree + LCA | Demonstrates optimal bounds |

---

## 🧮 Mathematical Foundations

### Idempotent Operations

Sparse Table works because minimum is idempotent:

min(x, x) = x

This allows overlapping intervals. For non-idempotent operations (e.g., sum), use Segment Trees.

### Reduction from LCA to RMQ

The Euler Tour of a tree creates an array where:

LCA(u,v) corresponds to RMQ(first[u], first[v]) on the depth array

This establishes the equivalence:

LCA ≡ RMQ (with ±1 property)

### The ±1 RMQ Technique

For an array where adjacent elements differ by exactly 1:
- Number of distinct blocks of size b = ½log n: 2^b = √n
- Precompute all √n × √n possibilities
- Query time: O(1) via table lookup

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📚 References

1. Bender, M. A., & Farach-Colton, M. (2000). The LCA problem revisited. LATIN 2000.
2. Fischer, J., & Heun, V. (2006). Theoretical and practical improvements on the RMQ-problem. SPIRE 2006.
3. Schieber, B., & Vishkin, U. (1988). On finding lowest common ancestors. SIAM Journal on Computing.
4. Cormen, T. H., et al. (2009). Introduction to Algorithms (3rd ed.). MIT Press. (Chapter 14: Augmenting Data Structures)


<div align="center">

⭐ **Star this repository if you found it helpful!** ⭐

</div>