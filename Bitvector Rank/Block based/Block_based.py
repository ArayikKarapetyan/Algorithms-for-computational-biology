from math import log2


class RankStruct:
    def __init__(self, bitvector):
        self.B = bitvector
        self.n = len(bitvector)

        self.k = int(log2(self.n) // 2)
        self.l = self.k ** 2
        
        self.first = []
        self.second = []
        self.third = {}

        self._construct()
        self._compute_third()




    def _compute_third(self):


        for bit in range(2 ** self.k):
            ones_of_prefix = []

            c = 0

            for i in range(self.k):
                if bit & (1 << (self.k - i - 1)):
                    c += 1
                ones_of_prefix.append(c)
            self.third[bit] = ones_of_prefix
            


    def _construct(self):

# SuperBlock
        total_ones = 0
        for i in range(0, self.n, self.l):
            self.first.append(total_ones)
            block_ones = 0
            total_ones += sum(self.B[i: min(i + self.l, self.n)])
#           Block
            for j in range(i, min(i + self.l, self.n), self.k):
                self.second.append(block_ones)
                block_ones += sum(self.B[j: min(j + self.k, self.n)])

    def rank(self, i):

        first_id = i // self.l
        second_id = i // self.k


        start_for_third = second_id * self.k
        offset = i % self.k

        bits_to_decimal = sum([2 ** (self.k - j - 1) * self.B[start_for_third + j] for j in range(min(self.k, self.n - start_for_third))])

        return self.first[first_id] + self.second[second_id] + self.third[bits_to_decimal][offset]
            


# Sample bitvector of size 20
B = [1,0,1,1,0,1,0,0,1,1,1,0,0,1,0,1,0,0,1,1]

# Create RankStruct
rs = RankStruct(B)

# Print internal tables for inspection
print("Superblock sums (first):", rs.first)
print("Block sums (second):", rs.second)

# Print a few lookup examples from third table
print("\nSome entries from third (lookup) table:")
sample_bits = [0b10101, 0b11111, 0b00001]
for b in sample_bits:
    if b in rs.third:
        print(f"bits={bin(b)} -> {rs.third[b]}")

# Test rank queries
test_indices = [0, 5, 10, 15, 19]
print("\nRank queries:")
for i in test_indices:
    print(f"rank({i}) = {rs.rank(i)}")

# Optional: brute-force verification
def brute_rank(B, i):
    return sum(B[:i+1])

print("\nBrute-force verification:")
for i in test_indices:
    print(f"rank({i}) = {rs.rank(i)}, brute={brute_rank(B,i)}")




    
