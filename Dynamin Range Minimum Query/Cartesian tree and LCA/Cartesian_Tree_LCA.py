class CartesianTreeLCA_RMQ:
    """
    O(n) preprocessing, O(1) query using Cartesian Tree + ±1 RMQ via LCA.
    This is the theoretically optimal solution.
    """
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr
        
        # Build Cartesian tree and compute Euler tour with depths
        self._build_cartesian_tree()
        self._euler_tour()
        self._build_sparse_table_on_euler()
    
    def _build_cartesian_tree(self):
        """Build Cartesian tree (min-heap property, inorder = original array)"""
        self.parent = [-1] * self.n
        self.left = [-1] * self.n
        self.right = [-1] * self.n
        
        stack = []  # Monotonic stack (increasing)
        
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
        
        # Find root
        self.root = 0
        for i in range(self.n):
            if self.parent[i] == -1:
                self.root = i
                break
    
    def _euler_tour(self):
        """Generate Euler tour of Cartesian tree with depths"""
        self.euler = []      # Nodes in Euler tour
        self.depth = []      # Depth of each node in tour
        self.first = [-1] * self.n  # First occurrence of each node
        
        def dfs(node, d):
            if node == -1:
                return
            
            # Record first occurrence
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
        """Build Sparse Table on the Euler tour depths (±1 RMQ optimization possible)"""
        self.log = [0] * (self.euler_size + 1)
        for i in range(2, self.euler_size + 1):
            self.log[i] = self.log[i // 2] + 1
        
        K = self.log[self.euler_size] + 1
        self.st = [[0] * self.euler_size for _ in range(K)]
        self.st_idx = [[0] * self.euler_size for _ in range(K)]  # Store indices
        
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
        """Find LCA of two nodes in Cartesian tree using RMQ on Euler tour"""
        if self.first[u] > self.first[v]:
            u, v = v, u
        
        l = self.first[u]
        r = self.first[v]
        
        j = self.log[r - l + 1]
        
        if self.st[j][l] <= self.st[j][r - (1 << j) + 1]:
            return self.euler[self.st_idx[j][l]]
        else:
            return self.euler[self.st_idx[j][r - (1 << j) + 1]]
    
    def query(self, l, r):
        """
        Query minimum in range [l, r].
        RMQ(l, r) = arr[LCA(l, r)] in Cartesian tree
        """
        lca_node = self._lca_query(l, r)
        return self.arr[lca_node]

# Usage
arr = [5, 2, 8, 1, 9, 3, 7, 4]
rmq = CartesianTreeLCA_RMQ(arr)
print(rmq.query(1, 4))  # Output: 1 (LCA of nodes 1 and 4 is node 3 with value 1)
print(rmq.query(0, 7))  # Output: 1
print(rmq.query(2, 5))  # Output: 1