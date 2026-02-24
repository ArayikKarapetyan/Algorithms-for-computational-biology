def build_suffix_array(s):
    n = len(s)
    suffix_array = list(range(n))
    
    # Initial ranking by first character
    rank = [ord(c) for c in s]
    temp = [0] * n
    
    k = 1
    while k < n:
        
        # ----------- RADIX SORT START -----------
        
        # Sort by second key
        max_rank = max(rank) + 1
        count = [0] * (max_rank + 1)
        new_sa = [0] * n
        
        # Count occurrences of second key
        for i in range(n):
            second = rank[i + k] if i + k < n else 0
            count[second] += 1
        
        # Prefix sums
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        
        # Build sorted array (stable)
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
        
        # Stop early if all ranks are distinct
        if rank[suffix_array[-1]] == n - 1:
            break
    
    return suffix_array
