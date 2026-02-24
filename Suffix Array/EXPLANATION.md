# Suffix Array — Prefix Doubling with Radix Sort (O(n log n))

---

## 📌 Goal

We want to build the **Suffix Array** of a string in:

**O(n log n)**

using:
- **Prefix Doubling**
- **Radix Sort** (Counting Sort twice per iteration)

---

## 🔎 What Is a Suffix Array?

For a string `s` of length `n`, the **suffix array** is an array of indices representing all suffixes of `s`, sorted lexicographically.

### Example:

```
s = "banana"
```

**Suffixes:**

| Index | Suffix  |
|-------|---------|
| 0 | banana |
| 1 | anana |
| 2 | nana |
| 3 | ana |
| 4 | na |
| 5 | a |

**Sorted:**

| Sorted Order | Index | Suffix |
|--------------|-------|--------|
| 1 | 5 | a |
| 2 | 3 | ana |
| 3 | 1 | anana |
| 4 | 0 | banana |
| 5 | 4 | na |
| 6 | 2 | nana |

**Suffix Array:**

```python
[5, 3, 1, 0, 4, 2]
```

---

## 🚀 Core Idea — Prefix Doubling

Instead of sorting full suffixes directly (too slow), we sort them by **progressively longer prefixes**.

We sort by:

1. First **1** character
2. First **2** characters
3. First **4** characters
4. First **8** characters
5. ...

Until prefix length ≥ n.

Each time we **double the prefix length**:

```
k → 2k
```

### Why This Works?

After log₂(n) iterations, we've compared prefixes of length ≥ n, which means we've compared entire suffixes!

---

## 🧠 Key Observation

If we already know:

```
rank[i] = rank of substring of length k starting at i
```

Then to compute rank for length `2k`, we only need:

```
(rank[i], rank[i + k])
```

So instead of **comparing strings**, we **compare integer pairs**.

This makes sorting efficient!

### Visual Example:

```
String: "banana"
k = 2 (comparing 2-character prefixes)

To sort suffix starting at i=1 ("anana"):
- First 2 chars: "an" → rank[1]
- Next 2 chars: "an" → rank[1+2] = rank[3]

So we compare pair (rank[1], rank[3])
```

---

## ⚡ Why Radix Sort?

### Comparison Sort Approach:

If we use comparison sort:

```
O(n log n) per iteration
× log n iterations
= O(n log² n)
```

### Radix Sort Approach:

But ranks are integers in range `[0, n-1]`.

So we can use **Counting Sort**, which runs in:

```
O(n)
```

Since we must sort by **two keys**:

```
(rank[i], rank[i + k])
```

We use:
1. Counting sort by **second key**
2. Counting sort by **first key**

Because counting sort is **stable**, this produces correct lexicographic ordering.

This gives:

```
O(n) per iteration × log n iterations = O(n log n)
```

---

## 🏗 Full Implementation

```python
def build_suffix_array(s):
    n = len(s)
    suffix_array = list(range(n))
    
    # Initial ranking by first character
    rank = [ord(c) for c in s]
    temp = [0] * n
    
    k = 1
    while k < n:
        
        # ----------- RADIX SORT START -----------
        
        max_rank = max(rank) + 1
        count = [0] * (max_rank + 1)
        new_sa = [0] * n
        
        # Sort by second key
        for i in range(n):
            second = rank[i + k] if i + k < n else 0
            count[second] += 1
        
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        
        for i in reversed(range(n)):
            idx = suffix_array[i]
            second = rank[idx + k] if idx + k < n else 0
            count[second] -= 1
            new_sa[count[second]] = idx
        
        suffix_array = new_sa[:]
        
        # Sort by first key
        count = [0] * (max_rank + 1)
        
        for i in range(n):
            count[rank[i]] += 1
        
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        
        for i in reversed(range(n)):
            idx = suffix_array[i]
            count[rank[idx]] -= 1
            new_sa[count[rank[idx]]] = idx
        
        suffix_array = new_sa[:]
        
        # ----------- RADIX SORT END -----------
        
        # Assign new ranks
        temp[suffix_array[0]] = 0
        
        for i in range(1, n):
            prev = suffix_array[i - 1]
            curr = suffix_array[i]
            
            prev_pair = (
                rank[prev],
                rank[prev + k] if prev + k < n else -1
            )
            
            curr_pair = (
                rank[curr],
                rank[curr + k] if curr + k < n else -1
            )
            
            temp[curr] = temp[prev] + (curr_pair != prev_pair)
        
        rank = temp[:]
        k *= 2
        
        if rank[suffix_array[-1]] == n - 1:
            break
    
    return suffix_array
```

---

## 🔍 Block-by-Block Code Explanation

### 1️⃣ Initialization

```python
n = len(s)
suffix_array = list(range(n))
rank = [ord(c) for c in s]
temp = [0] * n
k = 1
```

- `suffix_array` initially contains `[0, 1, 2, ..., n-1]`
- `rank[i]` stores rank of 1-character substring
- `k = 1` means we are sorting by prefixes of length 1

### Example:

```
s = "banana"
suffix_array = [0, 1, 2, 3, 4, 5]
rank = [98, 97, 110, 97, 110, 97]  # ord('b'), ord('a'), ...
k = 1
```

---

### 2️⃣ While Loop (Prefix Doubling)

```python
while k < n:
```

Each iteration:
- Sort by length `2k`
- Double `k`

---

### 3️⃣ Radix Sort — Second Key

```python
for i in range(n):
    second = rank[i + k] if i + k < n else 0
    count[second] += 1
```

We count how many times each **second key** appears.

If `i+k` exceeds string, we treat it as `0` (smallest possible rank).

#### Prefix Sum (Cumulative Count)

```python
for i in range(1, len(count)):
    count[i] += count[i - 1]
```

This transforms `count` array into **positions**.

#### Stable Placement

```python
for i in reversed(range(n)):
    idx = suffix_array[i]
    second = rank[idx + k] if idx + k < n else 0
    count[second] -= 1
    new_sa[count[second]] = idx
```

We iterate **backward** to preserve **stability**.

Now suffixes are sorted by **second key**.

---

### 4️⃣ Radix Sort — First Key

Same procedure, but using `rank[idx]`.

After this step:

> Suffixes are sorted by: `(rank[i], rank[i + k])`

---

### 5️⃣ Assign New Ranks

```python
temp[suffix_array[0]] = 0
```

First suffix gets rank 0.

#### Compare Adjacent Pairs

```python
prev_pair = (rank[prev], rank[prev+k])
curr_pair = (rank[curr], rank[curr+k])
```

If pairs differ → increase rank.

This assigns new **compressed ranks**.

---

### 6️⃣ Prepare for Next Iteration

```python
rank = temp[:]
k *= 2
```

We **double prefix size**.

---

### 7️⃣ Early Stop Optimization

```python
if rank[suffix_array[-1]] == n - 1:
    break
```

If ranks are already unique, sorting is complete.

---

## ⏱ Complexity Analysis

### Per iteration:

```
Counting sort → O(n)
```

### Number of iterations:

```
O(log n)
```

### Total:

```
O(n log n)
```

### Space:

```
O(n)
```

---

## 🎯 Why This Is Efficient

✅ **No string comparisons**  
✅ **No comparison-based sorting**  
✅ **Only integer sorting**  
✅ **Stable radix sort ensures correctness**  

---

## 📊 Step-by-Step Example

Let's build suffix array for `s = "banana"`:

### Initial State (k = 1):

```
suffix_array = [0, 1, 2, 3, 4, 5]
rank = [98, 97, 110, 97, 110, 97]  # ASCII values
```

After sorting by first character:

```
suffix_array = [1, 3, 5, 0, 2, 4]
rank = [2, 0, 3, 0, 3, 0]  # compressed ranks
```

Suffixes sorted by first char: `a, a, a, b, n, n`

---

### Iteration 1 (k = 2):

Comparing 2-character prefixes:

| Index | First 2 chars | Pair (rank[i], rank[i+2]) |
|-------|---------------|---------------------------|
| 1 | an | (0, 3) |
| 3 | an | (0, 0) |
| 5 | a | (0, -1) |
| 0 | ba | (2, 3) |
| 2 | na | (3, 3) |
| 4 | na | (3, 0) |

After radix sort:

```
suffix_array = [5, 3, 1, 0, 4, 2]
rank = [3, 2, 5, 1, 4, 0]
```

---

### Iteration 2 (k = 4):

Comparing 4-character prefixes:

All ranks become unique, so we're done!

**Final suffix array:** `[5, 3, 1, 0, 4, 2]`

---

## 🧪 Testing

```python
def test_suffix_array():
    # Test 1: Basic example
    s = "banana"
    sa = build_suffix_array(s)
    assert sa == [5, 3, 1, 0, 4, 2]
    
    # Verify: extract suffixes in order
    suffixes = [s[i:] for i in sa]
    assert suffixes == ['a', 'ana', 'anana', 'banana', 'na', 'nana']
    
    # Test 2: All same characters
    s = "aaaa"
    sa = build_suffix_array(s)
    assert sa == [3, 2, 1, 0]  # shortest to longest
    
    # Test 3: Reverse sorted
    s = "dcba"
    sa = build_suffix_array(s)
    assert sa == [3, 2, 1, 0]
    
    # Test 4: Already sorted
    s = "abcd"
    sa = build_suffix_array(s)
    assert sa == [0, 1, 2, 3]
    
    print("All tests passed! ✅")

test_suffix_array()
```

---

## 🎯 Applications

### 1. Pattern Matching

Find all occurrences of a pattern in O(m log n) using binary search on suffix array.

```python
def find_pattern(text, pattern, suffix_array):
    """Find all occurrences of pattern in text"""
    n = len(text)
    m = len(pattern)
    
    # Binary search for first occurrence
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        if text[suffix_array[mid]:suffix_array[mid]+m] < pattern:
            left = mid + 1
        else:
            right = mid
    
    start = left
    
    # Binary search for last occurrence
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        if text[suffix_array[mid]:suffix_array[mid]+m] <= pattern:
            left = mid + 1
        else:
            right = mid
    
    end = left
    
    return [suffix_array[i] for i in range(start, end)]
```

### 2. Longest Common Substring

Find longest common substring of two strings.

### 3. Burrows-Wheeler Transform

Used in data compression (bzip2).

### 4. DNA Sequence Analysis

Find repeated patterns in genomes.

---

## 🔄 Optimizations

### 1. In-place Radix Sort

Reduce space by modifying arrays in-place.

### 2. Sentinel Character

Add '$' at end to avoid special cases.

```python
s = s + '$'
```

### 3. Cache-Friendly Implementation

Optimize memory access patterns.

---

## 🆚 Comparison with Other Methods

| Method | Time | Space | Difficulty |
|--------|------|-------|------------|
| Naive | O(n² log n) | O(n) | Easy |
| Prefix Doubling (comparison sort) | O(n log² n) | O(n) | Medium |
| Prefix Doubling (radix sort) | O(n log n) | O(n) | Medium |
| SA-IS | O(n) | O(n) | Hard |
| DC3/Skew | O(n) | O(n) | Hard |

---

## 💡 Key Insights

### 1. Prefix Doubling

By doubling prefix length each iteration, we only need **log n iterations**.

### 2. Integer Comparison

Converting string comparison to integer pair comparison is the key optimization.

### 3. Stable Sorting

Radix sort's stability is crucial for correctness.

### 4. Rank Compression

After each iteration, we compress ranks to avoid overflow and maintain O(n) range.

---

## 🧮 Mathematical Analysis

### Correctness Proof

**Claim:** After k iterations, suffixes are sorted by their first 2^k characters.

**Base case:** k=0, sorted by first 1 character (ASCII values).

**Inductive step:** 
- Assume true for k
- In iteration k+1, we sort by pairs (rank[i], rank[i+2^k])
- rank[i] represents first 2^k chars
- rank[i+2^k] represents next 2^k chars
- Together they represent first 2^(k+1) chars ✓

### Time Complexity

```
Iterations: log₂(n)
Each iteration: 
  - Radix sort: O(n)
  - Rank update: O(n)
Total: O(n log n)
```

---

## 📚 Further Reading

* [Manber, U., & Myers, G. (1993). "Suffix arrays: A new method for on-line string searches"](https://dl.acm.org/doi/10.1137/0222058)
* [CP-Algorithms: Suffix Array](https://cp-algorithms.com/string/suffix-array.html)
* [Competitive Programmer's Handbook - Chapter 26](https://cses.fi/book/book.pdf)

---

## 🔑 Key Takeaways

1. **Prefix Doubling** reduces iterations to O(log n)
2. **Radix Sort** makes each iteration O(n)
3. **Rank compression** keeps values in range [0, n-1]
4. **Stable sorting** is essential for correctness
5. **Total complexity:** O(n log n) time, O(n) space

---

## 🏆 Competitive Programming Template

```python
def build_suffix_array(s):
    n = len(s)
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0] * n
    k = 1
    
    while k < n:
        # Radix sort by second key
        sa.sort(key=lambda i: (rank[i], rank[i+k] if i+k < n else -1))
        
        # Update ranks
        tmp[sa[0]] = 0
        for i in range(1, n):
            prev = (rank[sa[i-1]], rank[sa[i-1]+k] if sa[i-1]+k < n else -1)
            curr = (rank[sa[i]], rank[sa[i]+k] if sa[i]+k < n else -1)
            tmp[sa[i]] = tmp[sa[i-1]] + (prev != curr)
        
        rank = tmp[:]
        k *= 2
        
        if rank[sa[-1]] == n - 1:
            break
    
    return sa
```

**Note:** This template uses Python's built-in sort (O(n log n)) for simplicity. For true O(n log n), use the radix sort version above.

---

<div align="center">

**⚡ O(n log n) Suffix Array Construction ⚡**

*Efficient prefix doubling with radix sort*

</div>