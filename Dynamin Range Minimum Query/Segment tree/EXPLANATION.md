# Segment Tree for Range Minimum Query (RMQ)

## 📌 Overview

This implementation provides a Segment Tree data structure for solving the Range Minimum Query (RMQ) problem efficiently.

It supports:
* 🔎 Querying the minimum value in a range [l, r]
* 🔄 Updating a single element in the array

Both operations work in **O(log n)** time.

---

## 🧠 What Problem Does This Solve?

Given an array:

```python
arr = [5, 2, 8, 1, 9, 3, 7, 4]
```

We may want to:
* Find the minimum between indices `1` and `4`
* Update a value at a specific index
* Continue querying efficiently after updates

A normal approach would take:
* Query → O(n)
* Update → O(1)

But if we have many queries, this becomes slow.

A Segment Tree reduces:
* Query → **O(log n)**
* Update → **O(log n)**

---

## 🌳 What is a Segment Tree?

A Segment Tree is a binary tree where:
* Each **leaf** represents one element of the array
* Each **internal node** stores information about a segment (range)
* In this case → each node stores the **minimum** of its range

---

## 🔍 Code Breakdown

### 1️⃣ Constructor (`__init__`)

```python
def __init__(self, arr):
```

#### Step 1: Store array size

```python
self.n = len(arr)
```

#### Step 2: Find next power of 2

```python
self.size = 1
while self.size < self.n:
    self.size *= 2
```

**Why?**  
Segment trees work best when the number of leaves is a power of 2.

**Example:**
- If `n = 8`, already power of 2
- If `n = 5`, next power of 2 = 8

This makes the tree complete and easier to manage.

#### Step 3: Create tree array

```python
self.tree = [float('inf')] * (2 * self.size)
```

**Why `2 * size`?**  
Because:
* Leaves are stored from index `size` to `2*size - 1`
* Internal nodes are stored from `1` to `size - 1`

We initialize with `inf` because we are computing minimums.

#### Step 4: Fill leaves

```python
for i in range(self.n):
    self.tree[self.size + i] = arr[i]
```

We copy the original array into the leaf positions.

If `size = 8`, leaves start at index 8.

**Example layout:**

```
Level 0:                                         1
                                             (min = 1)
                                 ┌───────────────┴─────────────┐
Level 1:                         2                             3
                             (min = 2)                     (min = 3)
                        ┌────────┴────────┐           ┌────────┴────────┐
Level 2:                4                 5           6                 7
                    (min=2)           (min=1)      (min=3)           (min=4)
                   ┌────┴────┐       ┌────┴────┐ ┌────┴────┐       ┌────┴────┐
Level 3:           8         9      10        11 12        13      14        15
                  (5)       (2)     (8)      (1) (9)       (3)     (7)       (4)

Original Array Values:
Index:   0   1   2   3   4   5   6   7
Value:   5   2   8   1   9   3   7   4

```

#### Step 5: Build internal nodes

```python
for i in range(self.size - 1, 0, -1):
    self.tree[i] = min(self.tree[2*i], self.tree[2*i + 1])
```

Each parent stores:

```
min(left_child, right_child)
```

We build **bottom-up**.

**Time complexity:** O(n)

---

### 🔄 Update Operation

```python
def update(self, pos, value):
```

**Goal:** Change `arr[pos] = value`

#### Step 1: Move to leaf

```python
pos += self.size
self.tree[pos] = value
```

#### Step 2: Move upward and fix parents

```python
pos //= 2
while pos >= 1:
    self.tree[pos] = min(self.tree[2*pos], self.tree[2*pos + 1])
    pos //= 2
```

We recompute minimum values going up to the root.

**Why O(log n)?**  
Because the height of the tree is `log n`.

---

### 🔎 Query Operation

```python
def query(self, l, r):
```

**Goal:** Find minimum in range `[l, r]`

#### Step 1: Shift to leaf positions

```python
l += self.size
r += self.size
```

#### Step 2: Process while `l <= r`

```python
while l <= r:
```

We move both pointers upward.

#### Important Trick

**If `l` is a right child:**

```python
if l % 2 == 1:
    res = min(res, self.tree[l])
    l += 1
```

Because:
* This segment is fully inside range
* We take it and move right

**If `r` is a left child:**

```python
if r % 2 == 0:
    res = min(res, self.tree[r])
    r -= 1
```

Because:
* This segment is fully inside range
* We take it and move left

Then move both upward:

```python
l //= 2
r //= 2
```

This shrinks the range toward root.

**Why O(log n)?**  
Each level reduces the segment size by half.  
Tree height = `log n`.

---

## 🧪 Example Execution

### Initial Setup

```python
arr = [5, 2, 8, 1, 9, 3, 7, 4]
rmq = SegmentTreeRMQ(arr)

print(rmq.query(1, 4))  # Output: 1
```

Range `[1, 4]` → elements:

```
[2, 8, 1, 9]
```

Minimum = `1`

### Update

```python
rmq.update(3, 10)
```

Now array becomes:

```
[5, 2, 8, 10, 9, 3, 7, 4]
```

### Query again

```python
print(rmq.query(1, 4))  # Output: 2
```

Range `[1, 4]` → `[2, 8, 10, 9]`  
Minimum = `2`

---

## ⏱ Time Complexity

| Operation | Complexity |
|-----------|------------|
| Build | O(n) |
| Update | O(log n) |
| Query | O(log n) |
| Space | O(n) |

---

## 💻 Complete Implementation

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

## 🎯 Use Cases

This Segment Tree implementation is ideal for:

✅ **Competitive Programming** - Fast RMQ with updates  
✅ **Real-time Systems** - Dynamic data with range queries  
✅ **Database Indexing** - Range aggregation queries  
✅ **Computational Geometry** - Range searching problems  
✅ **Stock Market Analysis** - Finding min/max in time windows  

---

## 🔄 Extensions

The same structure can be easily modified for:

* **Range Maximum Query** - Change `min` to `max`
* **Range Sum Query** - Change `min` to `+`
* **Range GCD/LCM** - Apply appropriate operations
* **Lazy Propagation** - For range updates

---

## 📚 Related Data Structures

| Structure | Query | Update | Static/Dynamic |
|-----------|-------|--------|----------------|
| Segment Tree | O(log n) | O(log n) | Dynamic |
| Sparse Table | O(1) | ❌ | Static only |
| Fenwick Tree | O(log n) | O(log n) | Dynamic (prefix only) |
| Sqrt Decomposition | O(√n) | O(√n) | Dynamic |

---

## 🎓 Learning Resources

* [CP-Algorithms: Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html)
* [Codeforces Tutorial](https://codeforces.com/blog/entry/18051)
* [HackerEarth Guide](https://www.hackerearth.com/practice/data-structures/advanced-data-structures/segment-trees/tutorial/)

---

## ⭐ Key Takeaways

1. **Segment Trees** provide O(log n) queries and updates
2. **Tree size** is always a power of 2 for simplicity
3. **Bottom-up building** is more efficient than recursive
4. **Non-recursive queries** avoid stack overhead
5. **Space complexity** is linear (4n in worst case)

---

<div align="center">

Made with ❤️ for efficient range queries

</div>