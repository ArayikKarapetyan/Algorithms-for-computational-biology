# BitVectorRank: Fast Rank Queries on a Bit Vector

## 📌 Overview

This is a simple Python implementation of **rank operations** on a bit vector. It allows you to quickly count the number of `1`s or `0`s up to a given position in a bit vector.

**Key Features:**
* ⚡ **O(1) query time** - Constant time rank queries
* 🏗️ **O(n) preprocessing** - Linear time setup
* 💾 **O(n) space** - Linear space complexity
* 🎯 **Simple implementation** - Easy to understand and use

---

## 🧠 What is a Bit Vector?

A **bit vector** is just a list of bits (`0`s and `1`s). 

**Example:**

```python
bit_vector = [1, 0, 1, 1, 0, 0, 1]
```

---

## 🔍 What is a Rank Operation?

* **`rank1(i)`** → Number of `1`s in the first `i` bits of the bit vector.
* **`rank0(i)`** → Number of `0`s in the first `i` bits.

### Example:

```python
bit_vector = [1, 0, 1, 1, 0, 0, 1]

rank1(4)  # Count 1s in first 4 bits [1,0,1,1] → 3
rank0(5)  # Count 0s in first 5 bits [1,0,1,1,0] → 2
```

---

## 💻 Code Explanation

```python
class BitVectorRank:
    def __init__(self, bit_vector):
        self.bit_vector = bit_vector
        self.n = len(bit_vector)
        # Precompute rank1 up to each position
        self.rank1_prefix = [0] * (self.n + 1)  # rank1_prefix[0] = 0
        for i in range(1, self.n + 1):
            self.rank1_prefix[i] = self.rank1_prefix[i - 1] + bit_vector[i - 1]
```

---

## 1️⃣ Initialization

### What happens:

* **`bit_vector`** → the input list of 0s and 1s.
* **`n`** → the length of the bit vector.
* **`rank1_prefix`** → a precomputed array to store the number of `1`s up to each position.

### The Loop:

```python
for i in range(1, self.n + 1):
    self.rank1_prefix[i] = self.rank1_prefix[i - 1] + bit_vector[i - 1]
```

This means:
> **"number of 1s up to position i = number of 1s up to i-1 + current bit."**

### Example:

For `bit_vector = [1, 0, 1]`:

| i | bit_vector[i-1] | rank1_prefix[i] |
|---|-----------------|-----------------|
| 1 | 1 | 0 + 1 = 1 |
| 2 | 0 | 1 + 0 = 1 |
| 3 | 1 | 1 + 1 = 2 |

So `rank1_prefix = [0, 1, 1, 2]`.

---

## 2️⃣ rank1 Method

```python
def rank1(self, i):
    """Number of 1s in the first i bits (1-indexed)"""
    return self.rank1_prefix[i]
```

* Simply **looks up** the precomputed number of 1s in the `rank1_prefix` array.
* **Time Complexity:** O(1) → very fast!

### Example:

```python
bit_vector = [1, 0, 1, 1, 0]
ranker = BitVectorRank(bit_vector)
ranker.rank1(4)  # Output: 3
```

**Explanation:**
```
First 4 bits: [1, 0, 1, 1]
Count of 1s: 3
```

---

## 3️⃣ rank0 Method

```python
def rank0(self, i):
    """Number of 0s in the first i bits (1-indexed)"""
    return i - self.rank1_prefix[i]
```

* Counts 0s by subtracting the number of 1s from the total bits considered:

```
rank0(i) = i - rank1(i)
```

### Example:

```python
ranker.rank0(5)  # Output: 2 (5 bits total - 3 ones = 2 zeros)
```

**Explanation:**
```
First 5 bits: [1, 0, 1, 1, 0]
Total bits: 5
Count of 1s: 3
Count of 0s: 5 - 3 = 2
```

---

## 📊 Complete Implementation

```python
class BitVectorRank:
    def __init__(self, bit_vector):
        """
        Initialize the rank data structure.
        
        Args:
            bit_vector: List of 0s and 1s
        """
        self.bit_vector = bit_vector
        self.n = len(bit_vector)
        
        # Precompute rank1 up to each position
        self.rank1_prefix = [0] * (self.n + 1)
        for i in range(1, self.n + 1):
            self.rank1_prefix[i] = self.rank1_prefix[i - 1] + bit_vector[i - 1]
    
    def rank1(self, i):
        """
        Count number of 1s in the first i bits (1-indexed).
        
        Args:
            i: Position (1-indexed)
        
        Returns:
            Number of 1s in bit_vector[0:i]
        """
        if i < 0 or i > self.n:
            raise ValueError(f"Position {i} out of range [0, {self.n}]")
        return self.rank1_prefix[i]
    
    def rank0(self, i):
        """
        Count number of 0s in the first i bits (1-indexed).
        
        Args:
            i: Position (1-indexed)
        
        Returns:
            Number of 0s in bit_vector[0:i]
        """
        if i < 0 or i > self.n:
            raise ValueError(f"Position {i} out of range [0, {self.n}]")
        return i - self.rank1_prefix[i]
```

---

## 🧪 Example Usage

```python
# Create a bit vector
bit_vector = [1, 0, 1, 1, 0, 0, 1]

# Initialize rank structure
ranker = BitVectorRank(bit_vector)

# Query rank1
print(ranker.rank1(0))  # Output: 0 (no bits)
print(ranker.rank1(1))  # Output: 1 (first bit is 1)
print(ranker.rank1(4))  # Output: 3 ([1,0,1,1] has 3 ones)
print(ranker.rank1(7))  # Output: 4 (all bits: 4 ones)

# Query rank0
print(ranker.rank0(0))  # Output: 0 (no bits)
print(ranker.rank0(1))  # Output: 0 (first bit is 1)
print(ranker.rank0(4))  # Output: 1 ([1,0,1,1] has 1 zero)
print(ranker.rank0(7))  # Output: 3 (all bits: 3 zeros)
```

---

## 📊 Visual Example

```
Bit Vector: [1, 0, 1, 1, 0, 0, 1]
Indices:     1  2  3  4  5  6  7

rank1_prefix = [0, 1, 1, 2, 3, 3, 3, 4]
                ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑
Position:       0  1  2  3  4  5  6  7

Queries:
rank1(4) = 3  (positions 1,3,4 have 1s)
rank0(4) = 1  (position 2 has 0)
rank1(7) = 4  (positions 1,3,4,7 have 1s)
rank0(7) = 3  (positions 2,5,6 have 0s)
```

---

## ⏱️ Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Preprocessing | O(n) | O(n) |
| rank1(i) | O(1) | - |
| rank0(i) | O(1) | - |

Where **n** is the length of the bit vector.

---

## ✅ Advantages

* ⚡ **Very fast:** Each query is O(1)
* 🧠 **Simple to understand:** Uses basic prefix sums
* 🎯 **Good for small to medium bit vectors**
* 🔧 **Easy to implement:** Minimal code required

---

## ❌ Disadvantages

* 💾 **Uses O(n) extra memory** to store the prefix sum array
* 📏 **For very large bit vectors**, more memory-efficient techniques are preferred:
  - Jacobson's three-level rank structure (O(n/log²n) extra space)
  - Wavelet trees
  - RRR compressed bit vectors

---

## 🎯 Applications

### 1. Succinct Data Structures

Bit vectors with rank/select are fundamental building blocks for:
* Compressed suffix arrays
* Wavelet trees
* FM-index for text search

### 2. Bioinformatics

* DNA sequence analysis
* Genome compression
* Pattern matching in biological sequences

### 3. Information Retrieval

* Inverted indices
* Document ranking
* Compressed databases

### 4. Graph Algorithms

* Succinct graph representations
* Adjacency matrix compression
* Tree navigation

---

## 🔄 Extensions

### 1. Select Operation

```python
def select1(self, k):
    """
    Find position of k-th 1 (1-indexed).
    
    Args:
        k: Which 1 to find
    
    Returns:
        Position of k-th 1
    """
    # Binary search on rank1_prefix
    left, right = 0, self.n
    while left < right:
        mid = (left + right) // 2
        if self.rank1_prefix[mid] < k:
            left = mid + 1
        else:
            right = mid
    return left if left <= self.n and self.rank1_prefix[left] == k else -1
```

### 2. Range Rank

```python
def range_rank1(self, l, r):
    """Count 1s in range [l, r] (1-indexed, inclusive)"""
    return self.rank1(r) - self.rank1(l - 1)
```

### 3. Access Operation

```python
def access(self, i):
    """Get bit at position i (1-indexed)"""
    return self.bit_vector[i - 1]
```

---

## 🧮 Mathematical Foundation

### Prefix Sum Formula

For any position `i`:

```
rank1(i) = Σ(j=0 to i-1) bit_vector[j]
```

### Rank0 Derivation

Since each position is either 0 or 1:

```
rank0(i) + rank1(i) = i
Therefore:
rank0(i) = i - rank1(i)
```

### Range Rank

For range [l, r]:

```
range_rank1(l, r) = rank1(r) - rank1(l-1)
```

This uses the **inclusion-exclusion principle**.

---

## 🧪 Testing Suite

```python
def test_bit_vector_rank():
    # Test case 1: Simple bit vector
    bv = [1, 0, 1, 1, 0, 0, 1]
    ranker = BitVectorRank(bv)
    
    assert ranker.rank1(0) == 0
    assert ranker.rank1(1) == 1
    assert ranker.rank1(4) == 3
    assert ranker.rank1(7) == 4
    
    assert ranker.rank0(0) == 0
    assert ranker.rank0(4) == 1
    assert ranker.rank0(7) == 3
    
    # Test case 2: All ones
    bv_ones = [1, 1, 1, 1]
    ranker_ones = BitVectorRank(bv_ones)
    
    assert ranker_ones.rank1(4) == 4
    assert ranker_ones.rank0(4) == 0
    
    # Test case 3: All zeros
    bv_zeros = [0, 0, 0, 0]
    ranker_zeros = BitVectorRank(bv_zeros)
    
    assert ranker_zeros.rank1(4) == 0
    assert ranker_zeros.rank0(4) == 4
    
    print("All tests passed! ✅")

test_bit_vector_rank()
```

---

## 📚 Further Reading

* [Jacobson, G. (1989). "Space-efficient static trees and graphs"](https://dl.acm.org/doi/10.1109/SFCS.1989.63533)
* [Navarro, G., & Mäkinen, V. (2007). "Compressed full-text indexes"](https://www.cambridge.org/core/journals/combinatorics-probability-and-computing/article/abs/compressed-fulltext-indexes/0F04B01B8A38F8B0E05F7A5F849CE6A8)
* [Wavelet Trees - CP-Algorithms](https://cp-algorithms.com/data_structures/wavelet.html)

---

## 💡 Performance Tips

### 1. Use Arrays Instead of Lists

For better performance with large bit vectors:

```python
import array
self.rank1_prefix = array.array('I', [0] * (self.n + 1))
```

### 2. Memory-Efficient for Large Vectors

For very large bit vectors, use block-based approach:

```python
# Store only every k-th prefix sum
# Scan at most k bits per query
```

### 3. Bit Packing

Store multiple bits per integer:

```python
# Use bitwise operations
# 64 bits per 64-bit integer
```

---

## 🔑 Key Takeaways

1. **Prefix sums** enable O(1) rank queries
2. **rank0** derived from **rank1** using simple arithmetic
3. **Trade-off:** O(n) space for O(1) queries
4. **Foundation** for succinct data structures
5. **Simple** but powerful technique

---

## 🆚 Comparison with Other Techniques

| Technique | Space | rank1 Time | Notes |
|-----------|-------|------------|-------|
| Naive | O(1) | O(n) | Scan entire vector |
| Prefix Sum (This) | O(n) | O(1) | Best for small/medium |
| Jacobson | O(n/log²n) | O(1) | Best for large vectors |
| RRR | O(nH₀) | O(1) | Compressed, H₀ is entropy |

---

<div align="center">

**⚡ Fast, Simple, Effective ⚡**

*The foundation of succinct data structures*

</div>