# Sparse Table for Range Minimum Query (RMQ)

## 📌 Overview

This implementation provides a **Sparse Table** data structure for solving the **static Range Minimum Query (RMQ)** problem.

It supports:
* 🔎 Query minimum in range `[l, r]`
* 🚀 Query time: **O(1)**
* 🏗 Preprocessing time: **O(n log n)**
* ❌ Does **NOT** support updates

This is one of the most powerful static RMQ solutions.

---

## 🧠 When Should You Use Sparse Table?

**Use it when:**
* The array does **not change**
* You need **many fast queries**
* You want **optimal query speed**

**If updates are required** → use **Segment Tree** instead.

---

## 💡 Core Idea

Sparse Table precomputes minimums for intervals of size:

```
1, 2, 4, 8, 16, 32, ...
```

That is:

```
2^0, 2^1, 2^2, 2^3, ...
```

Then any query `[l, r]` can be answered using **two overlapping power-of-two intervals**.

---

## 🔢 Structure of the Table

We build:

```
st[j][i]
```

**Meaning:**

```
Minimum of subarray starting at i
with length = 2^j
```

So:

```
st[0][i] → length = 1
st[1][i] → length = 2
st[2][i] → length = 4
st[3][i] → length = 8
```

---

## 🔍 Code Breakdown

### 1️⃣ Constructor

```python
def __init__(self, arr):
```

#### Step 1: Store size

```python
self.n = len(arr)
```

#### Step 2: Precompute logarithms

```python
self.log = [0] * (self.n + 1)

for i in range(2, self.n + 1):
    self.log[i] = self.log[i // 2] + 1
```

This computes:

```
log[i] = floor(log2(i))
```

**Example:**

```
i:      1 2 3 4 5 6 7 8
log[i]: 0 1 1 2 2 2 2 3
```

**Why?**  
To quickly determine largest power of 2 ≤ interval length.

**Time:** O(n)

#### Step 3: Allocate Sparse Table

```python
self.K = self.log[self.n] + 1
self.st = [[0] * self.n for _ in range(self.K)]
```

Where:

```
K = number of layers = floor(log2(n)) + 1
```

If n = 8:

```
K = 4
```

We create a 2D table:

```
Rows → powers of 2
Columns → starting index
```

#### Step 4: Initialize intervals of length 1

```python
for i in range(self.n):
    self.st[0][i] = arr[i]
```

So:

```
st[0] = original array
```

#### Step 5: Build larger intervals

```python
for j in range(1, self.K):
    for i in range(self.n - (1 << j) + 1):
        self.st[j][i] = min(
            self.st[j-1][i],
            self.st[j-1][i + (1 << (j-1))]
        )
```

**Explanation:**  
To compute interval of length `2^j`:  
Split it into two halves:

```
Left half:  length 2^(j-1)
Right half: length 2^(j-1)
```

So:

```
min(arr[i ... i+2^j-1])
=
min(
    min(arr[i ... i+2^(j-1)-1]),
    min(arr[i+2^(j-1) ... i+2^j-1])
)
```

This builds **bottom-up**.

**Preprocessing time:** O(n log n)

---

## 📊 Example Table Construction

For:

```python
arr = [5, 2, 8, 1, 9, 3, 7, 4]
```

### Level j = 0 (length = 1)

```
5  2  8  1  9  3  7  4
```

### Level j = 1 (length = 2)

```
min(5,2)=2
min(2,8)=2
min(8,1)=1
min(1,9)=1
min(9,3)=3
min(3,7)=3
min(7,4)=4
```

→

```
2  2  1  1  3  3  4
```

### Level j = 2 (length = 4)

```
min(2,1)=1
min(2,1)=1
min(1,3)=1
min(1,3)=1
min(3,4)=3
```

→

```
1  1  1  1  3
```

### Level j = 3 (length = 8)

```
min(1,3)=1
```

---

## 🔎 Query Operation

```python
def query(self, l, r):
```

**Goal:**

```
min(arr[l..r])
```

#### Step 1: Compute interval length

```python
length = r - l + 1
```

#### Step 2: Get largest power of 2 inside it

```python
j = self.log[length]
```

So:

```
2^j ≤ length
```

#### Step 3: Use two overlapping intervals

```python
return min(
    self.st[j][l],
    self.st[j][r - (1 << j) + 1]
)
```

This works because:  
**Minimum is idempotent:**

```
min(a, a) = a
```

So overlapping does **NOT** break correctness.

---

## 🧠 Why Overlapping Works?

We cover `[l, r]` using two intervals:

```
[l, l + 2^j - 1]
[r - 2^j + 1, r]
```

They may **overlap**, but that's fine because:

```
min(min(A), min(B)) = min(A ∪ B)
```

And duplicates do not change minimum.

### This is why Sparse Table works for:
* ✅ min
* ✅ max
* ✅ gcd

### But NOT for:
* ❌ sum

---

## 🧪 Example Queries

### Query 1

```python
rmq.query(1, 4)
```

Array slice:

```
[2, 8, 1, 9]
```

Minimum = `1`

### Query 2

```python
rmq.query(0, 7)
```

Whole array → minimum = `1`

---

## ⏱ Complexity

| Operation | Complexity |
|-----------|------------|
| Preprocess | O(n log n) |
| Query | O(1) |
| Update | ❌ Not supported |
| Space | O(n log n) |

---

## 📌 Comparison With Other RMQ Methods

| Structure | Query | Update | Best For |
|-----------|-------|--------|----------|
| Brute Force | O(n) | O(1) | Very small input |
| Segment Tree | O(log n) | O(log n) | Dynamic RMQ |
| Sparse Table | O(1) | ❌ | Static RMQ |
| Sqrt Decomposition | O(√n) | O(√n) | Simpler dynamic |

---

## 💻 Complete Implementation

```python
import math

class SparseTableRMQ:
    def __init__(self, arr):
        self.n = len(arr)
        self.log = [0] * (self.n + 1)
        
        # Precompute logarithms
        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1
        
        # Allocate sparse table
        self.K = self.log[self.n] + 1
        self.st = [[0] * self.n for _ in range(self.K)]
        
        # Initialize base layer (length = 1)
        for i in range(self.n):
            self.st[0][i] = arr[i]
        
        # Build larger intervals
        for j in range(1, self.K):
            for i in range(self.n - (1 << j) + 1):
                self.st[j][i] = min(self.st[j-1][i], 
                                   self.st[j-1][i + (1 << (j-1))])
    
    def query(self, l, r):
        """Query minimum in range [l, r] in O(1) time"""
        j = self.log[r - l + 1]
        return min(self.st[j][l], self.st[j][r - (1 << j) + 1])
```

---

## 🎯 Use Cases

Sparse Table is ideal for:

✅ **Static arrays** with many queries  
✅ **Competitive programming** problems  
✅ **Lowest Common Ancestor (LCA)** in trees  
✅ **Range GCD** queries  
✅ **Range MAX/MIN** queries  

---

## 🔄 Variations

### Range Maximum Query

```python
# Change min to max in build and query
self.st[j][i] = max(self.st[j-1][i], 
                    self.st[j-1][i + (1 << (j-1))])
```

### Range GCD Query

```python
import math

# Change min to gcd
self.st[j][i] = math.gcd(self.st[j-1][i], 
                          self.st[j-1][i + (1 << (j-1))])
```

---

## 🧮 Space Analysis

For array of size n:

```
Space = K × n
where K = floor(log2(n)) + 1
```

**Examples:**

| n | K | Space |
|---|---|-------|
| 10 | 4 | 40 integers |
| 100 | 7 | 700 integers |
| 1,000 | 10 | 10,000 integers |
| 10,000 | 14 | 140,000 integers |

For n = 10^6:
- K ≈ 20
- Space ≈ 20 MB (assuming 4-byte integers)

---

## 🎓 Key Properties

### Idempotent Operations

An operation ⊕ is **idempotent** if:

```
a ⊕ a = a
```

**Works with Sparse Table:**
- min(a, a) = a ✅
- max(a, a) = a ✅
- gcd(a, a) = a ✅

**Doesn't work:**
- a + a = 2a ❌
- a × a = a² ❌

---

## 📚 Learning Resources

* [CP-Algorithms: Sparse Table](https://cp-algorithms.com/data_structures/sparse-table.html)
* [Codeforces Tutorial](https://codeforces.com/blog/entry/22616)
* [TopCoder Tutorial](https://www.topcoder.com/thrive/articles/Range%20Minimum%20Query%20and%20Lowest%20Common%20Ancestor)

---

## 🧪 Testing

```python
# Create sparse table
arr = [5, 2, 8, 1, 9, 3, 7, 4]
rmq = SparseTableRMQ(arr)

# Test queries
assert rmq.query(0, 0) == 5
assert rmq.query(1, 4) == 1
assert rmq.query(0, 7) == 1
assert rmq.query(4, 6) == 3
assert rmq.query(2, 3) == 1

print("All tests passed! ✅")
```

---

## ⚡ Performance Tips

1. **Precompute logarithms** - Avoid repeated log calculations
2. **Use bit shifts** - `(1 << j)` is faster than `pow(2, j)`
3. **Cache-friendly** - Access st[j][i] sequentially when possible
4. **Consider memory** - For huge n, use Segment Tree (O(n) space)

---

## 🎯 When NOT to Use Sparse Table

❌ **Array is frequently updated**  
   → Use Segment Tree instead

❌ **Operation is not idempotent** (like sum)  
   → Use Segment Tree or Fenwick Tree

❌ **Memory is very limited**  
   → Use Sqrt Decomposition (O(n) space)

---

## ⭐ Key Takeaways

1. **Sparse Table** gives O(1) queries for static arrays
2. Works only for **idempotent operations**
3. Preprocessing takes **O(n log n)** time and space
4. Uses **overlapping intervals** - key insight!
5. Perfect for **competitive programming**

---

<div align="center">

**⚡ Fastest static RMQ solution! ⚡**

Made with ❤️ for algorithm enthusiasts

</div>