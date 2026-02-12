# Z-Algorithm for Pattern Matching

## 📌 Overview

The **Z-algorithm** is a string-processing technique that allows you to quickly find:
* Occurrences of a **pattern** inside a **text**
* All **prefix matches** in a string

It computes a **Z-array** for a string:

> **Z[i]** = length of the longest substring starting at i which is also a prefix of the string

**Key Properties:**
* ⚡ **O(n) time complexity** - Linear time preprocessing
* 🔎 **O(n + m) pattern matching** - Faster than naive O(n × m)
* 💾 **O(n) space** - Linear space requirements
* 🎯 **Simple implementation** - Easy to understand and code

---

## 🔍 Example

```text
String: "abacaba"

Prefix matches:
```

| i | Substring starting at i | Z[i] | Explanation |
|---|------------------------|------|-------------|
| 0 | abacaba | 7 | Entire string matches itself |
| 1 | bacaba | 0 | 'b' ≠ 'a' (first char) |
| 2 | acaba | 1 | 'a' = 'a', but 'c' ≠ 'b' |
| 3 | caba | 0 | 'c' ≠ 'a' |
| 4 | aba | 3 | "aba" matches prefix "aba" |
| 5 | ba | 0 | 'b' ≠ 'a' |
| 6 | a | 1 | 'a' = 'a' (end of string) |

**So the Z-array is:**

```python
[7, 0, 1, 0, 3, 0, 1]
```

---

## 💡 Why Z-Algorithm is Useful

### Advantages:

* 🔎 **Pattern searching in O(n + m) time** (n = text length, m = pattern length)
* 🧩 **Find all occurrences** of a substring
* 🔁 **Find repetitions and borders** in strings
* ⚡ **Linear time** - optimal for string matching

Compared to **naive search (O(n × m))**, Z-algorithm is much faster.

---

## 🔢 How Z-Algorithm Works

### Core Idea:

1. **Initialize** Z[0] = n (entire string matches itself)
2. Keep a window **[L, R]** representing the rightmost segment that matches the prefix
3. For each position i:
   - **If i > R** → Outside the current window
     - Start matching from scratch
     - Update [L, R] if a longer prefix is found
   - **If i ≤ R** → Inside the window
     - Use previous Z-values to avoid redundant comparisons
     - Possibly extend the match beyond R

This gives **O(n) runtime** because each character is compared at most once outside the window.

---

## 🎨 Visual Example

```
String: "aabcaabxaaaz"
         0123456789...

Step-by-step Z-array computation:

i=0: Z[0] = 12 (entire string)
     [L,R] = [0,0]

i=1: i > R, so match from scratch
     "aabcaabxaaaz" vs "abcaabxaaaz"
      ^               ^
     Match: "a"
     Z[1] = 1, [L,R] = [1,1]

i=2: i > R, match from scratch
     "aabcaabxaaaz" vs "bcaabxaaaz"
      ^               ^
     No match
     Z[2] = 0, [L,R] = [1,1]

i=3: i > R, match from scratch
     "aabcaabxaaaz" vs "caabxaaaz"
      ^               ^
     No match
     Z[3] = 0, [L,R] = [1,1]

i=4: i > R, match from scratch
     "aabcaabxaaaz" vs "aabxaaaz"
      ^^^             ^^^
     Match: "aab"
     Z[4] = 3, [L,R] = [4,6]

...and so on
```

---

## 🧩 Pseudocode

```
Z[0] = n
L = R = 0

for i = 1 to n-1:
    if i > R:
        # Outside window - match from scratch
        L = R = i
        while R < n and S[R-L] == S[R]:
            R += 1
        Z[i] = R - L
        R -= 1
    else:
        # Inside window - use previous values
        k = i - L
        if Z[k] < R - i + 1:
            # Can copy directly
            Z[i] = Z[k]
        else:
            # Need to extend
            L = i
            while R < n and S[R-L] == S[R]:
                R += 1
            Z[i] = R - L
            R -= 1
```

---

## 💻 Python Implementation

```python
def z_algorithm(s):
    """
    Compute Z-array for string s.
    
    Z[i] = length of longest substring starting at i 
           which is also a prefix of s
    
    Args:
        s: Input string
    
    Returns:
        List of Z-values
    """
    n = len(s)
    Z = [0] * n
    Z[0] = n  # entire string matches itself
    
    L = R = 0
    for i in range(1, n):
        if i > R:
            # Case 1: i is outside the Z-box
            L = R = i
            while R < n and s[R-L] == s[R]:
                R += 1
            Z[i] = R - L
            R -= 1
        else:
            # Case 2: i is inside the Z-box
            k = i - L
            if Z[k] < R - i + 1:
                # Z[k] is entirely within Z-box
                Z[i] = Z[k]
            else:
                # Z[k] reaches or exceeds Z-box boundary
                L = i
                while R < n and s[R-L] == s[R]:
                    R += 1
                Z[i] = R - L
                R -= 1
    
    return Z
```

---

## 🔎 Example Usage

### Basic Z-array Computation:

```python
text = "abacaba"
z = z_algorithm(text)
print(z)  # Output: [7, 0, 1, 0, 3, 0, 1]
```

### More Examples:

```python
# Example 1: Repeated pattern
print(z_algorithm("aaaaaa"))
# Output: [6, 5, 4, 3, 2, 1]

# Example 2: No matches
print(z_algorithm("abcdef"))
# Output: [6, 0, 0, 0, 0, 0]

# Example 3: Periodic string
print(z_algorithm("abababab"))
# Output: [8, 0, 6, 0, 4, 0, 2, 0]
```

---

## 🔍 Pattern Matching Using Z-Algorithm

To find all occurrences of a pattern P in text T:

```python
def find_pattern(text, pattern):
    """
    Find all occurrences of pattern in text.
    
    Args:
        text: Text to search in
        pattern: Pattern to find
    
    Returns:
        List of starting positions where pattern occurs
    """
    # Concatenate with separator
    s = pattern + "$" + text  # $ is a separator not in text
    Z = z_algorithm(s)
    m = len(pattern)
    
    occurrences = []
    for i in range(m + 1, len(s)):
        if Z[i] == m:
            occurrences.append(i - m - 1)  # match starts here
    
    return occurrences
```

### Example:

```python
text = "ababcababc"
pattern = "ab"
print(find_pattern(text, pattern))  
# Output: [0, 2, 5, 7]

# Verification:
# Position 0: "ab"abcababc
# Position 2: ab"ab"cababc
# Position 5: ababc"ab"abc
# Position 7: ababcab"ab"c
```

---

## 📊 Visual Pattern Matching

```
Pattern: "ab"
Text:    "ababcababc"

Combined: "ab$ababcababc"
          012345678901234

Z-array:  [13, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0]
                      ^     ^     ^     ^
                      |     |     |     |
                   Z=2   Z=2   Z=2   Z=2
                   (matches!)

Positions where Z[i] == len(pattern):
i=3: position in original text = 3 - 2 - 1 = 0 ✓
i=5: position in original text = 5 - 2 - 1 = 2 ✓
i=8: position in original text = 8 - 2 - 1 = 5 ✓
i=10: position in original text = 10 - 2 - 1 = 7 ✓
```

---

## ⏱️ Complexity

| Operation | Complexity |
|-----------|------------|
| Preprocess Z-array | O(n) |
| Query for pattern matches | O(n + m) |
| Space | O(n) |

### Why O(n)?

Each character is visited at most **twice**:
1. Once when R expands
2. Once when we copy from previous Z-values

Therefore, total comparisons ≤ 2n → **O(n)**

---

## 🎯 Use Cases

### 1. String Searching

```python
# Find all occurrences of a word in a document
text = "the cat in the hat sat on the mat"
pattern = "the"
positions = find_pattern(text, pattern)
print(positions)  # [0, 11, 24]
```

### 2. DNA Sequence Analysis

```python
# Find all occurrences of a gene sequence
dna = "ATCGATCGATCG"
gene = "ATCG"
positions = find_pattern(dna, gene)
print(positions)  # [0, 3, 6]
```

### 3. Detecting Repeated Patterns

```python
def find_period(s):
    """Find smallest period of string"""
    Z = z_algorithm(s)
    n = len(s)
    for i in range(1, n):
        if i + Z[i] == n:
            return i
    return n

print(find_period("abcabcabc"))  # Output: 3
```

### 4. Finding Borders in Strings

```python
def find_borders(s):
    """Find all border lengths (prefix = suffix)"""
    Z = z_algorithm(s)
    n = len(s)
    borders = []
    for i in range(1, n):
        if i + Z[i] == n:
            borders.append(Z[i])
    return borders

print(find_borders("abacaba"))  # Output: [1, 3]
```

---

## 🧪 Comprehensive Testing

```python
def test_z_algorithm():
    # Test 1: Basic example
    assert z_algorithm("abacaba") == [7, 0, 1, 0, 3, 0, 1]
    
    # Test 2: All same characters
    assert z_algorithm("aaaaa") == [5, 4, 3, 2, 1]
    
    # Test 3: No matches
    assert z_algorithm("abcde") == [5, 0, 0, 0, 0]
    
    # Test 4: Pattern matching
    assert find_pattern("ababcababc", "ab") == [0, 2, 5, 7]
    
    # Test 5: Single character
    assert z_algorithm("a") == [1]
    
    # Test 6: Two characters
    assert z_algorithm("aa") == [2, 1]
    
    print("All tests passed! ✅")

test_z_algorithm()
```

---

## 🔄 Variations and Extensions

### 1. Case-Insensitive Matching

```python
def find_pattern_case_insensitive(text, pattern):
    return find_pattern(text.lower(), pattern.lower())
```

### 2. Multiple Patterns

```python
def find_multiple_patterns(text, patterns):
    results = {}
    for pattern in patterns:
        results[pattern] = find_pattern(text, pattern)
    return results
```

### 3. Find Longest Repeated Substring

```python
def longest_repeated_substring(s):
    n = len(s)
    max_len = 0
    max_pos = 0
    
    for i in range(n):
        Z = z_algorithm(s[i:])
        for j in range(1, len(Z)):
            if Z[j] > max_len:
                max_len = Z[j]
                max_pos = i
    
    return s[max_pos:max_pos + max_len]
```

---

## 🧮 Mathematical Analysis

### Correctness

**Invariant:** At the start of iteration i:
- Z[j] is correctly computed for all j < i
- [L, R] is the rightmost Z-box (where s[L..R] matches s[0..R-L])

**Two cases:**
1. **i > R:** No information available, must compare explicitly
2. **i ≤ R:** Can use Z[i-L] as a starting point

### Amortized Analysis

**Claim:** Each character is compared at most twice.

**Proof:**
- When R increases, characters at positions ≤ R are compared
- R never decreases (except by 1 at line `R -= 1`, but it was just increased)
- Total R increases ≤ n
- Therefore, total comparisons ≤ 2n

---

## 🆚 Comparison with Other Algorithms

| Algorithm | Preprocessing | Matching | Space | Notes |
|-----------|--------------|----------|-------|-------|
| Naive | O(1) | O(n×m) | O(1) | Simple but slow |
| Z-Algorithm | O(m) | O(n+m) | O(n+m) | Fast, simple |
| KMP | O(m) | O(n+m) | O(m) | Similar speed |
| Boyer-Moore | O(m+σ) | O(n+m) | O(m+σ) | Best average case |
| Aho-Corasick | O(Σm) | O(n+z) | O(Σm) | Multiple patterns |

Where:
- n = text length
- m = pattern length
- σ = alphabet size
- z = number of matches

---

## 💡 Implementation Tips

### 1. Off-by-one Errors

Be careful with:
```python
R -= 1  # After extending R
```

This is because R points to the last matching character, not one past it.

### 2. Separator Choice

Choose a separator that doesn't appear in text or pattern:
```python
s = pattern + "$" + text  # $ not in alphabet
```

### 3. Edge Cases

Handle:
- Empty string
- Single character
- Pattern longer than text

---

## 📚 Further Reading

* [CP-Algorithms: Z-function](https://cp-algorithms.com/string/z-function.html)
* [Gusfield, D. (1997). "Algorithms on Strings, Trees and Sequences"](https://www.cambridge.org/core/books/algorithms-on-strings-trees-and-sequences/F0B095049C7E6EF5356F0A26686C20D3)
* [Codeforces Z-Algorithm Tutorial](https://codeforces.com/blog/entry/3107)

---

## 🔑 Key Takeaways

1. **Z-array** stores prefix match lengths for each position
2. **O(n) time** using the Z-box optimization
3. **Pattern matching** via concatenation with separator
4. **Simpler than KMP** with similar performance
5. **Versatile** - many string problems can use Z-algorithm

---

## 🏆 Competitive Programming Template

```python
def z_algorithm(s):
    n = len(s)
    Z = [0] * n
    Z[0] = n
    L = R = 0
    for i in range(1, n):
        if i > R:
            L = R = i
            while R < n and s[R-L] == s[R]:
                R += 1
            Z[i] = R - L
            R -= 1
        else:
            k = i - L
            if Z[k] < R - i + 1:
                Z[i] = Z[k]
            else:
                L = i
                while R < n and s[R-L] == s[R]:
                    R += 1
                Z[i] = R - L
                R -= 1
    return Z

def find_pattern(text, pattern):
    s = pattern + "$" + text
    Z = z_algorithm(s)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(s)) if Z[i] == m]
```

---

<div align="center">

**⚡ Linear Time String Matching ⚡**

*Simple, efficient, and elegant*

</div>