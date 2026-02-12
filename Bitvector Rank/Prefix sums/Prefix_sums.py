class BitVectorRank:
    def __init__(self, bit_vector):
        self.bit_vector = bit_vector
        self.n = len(bit_vector)
        # Precompute rank1 up to each position
        self.rank1_prefix = [0] * (self.n + 1)  # rank1_prefix[0] = 0
        for i in range(1, self.n + 1):
            self.rank1_prefix[i] = self.rank1_prefix[i - 1] + bit_vector[i - 1]

    def rank1(self, i):
        """Number of 1s in the first i bits (1-indexed)"""
        return self.rank1_prefix[i]

    def rank0(self, i):
        """Number of 0s in the first i bits (1-indexed)"""
        return i - self.rank1_prefix[i]
