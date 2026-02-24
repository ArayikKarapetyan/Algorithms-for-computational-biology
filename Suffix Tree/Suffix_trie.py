from graphviz import Digraph
import os

class TrieNode:
    def __init__(self):
        self.children = {}
        self.id = None  # unique id for visualization


class SuffixTrie:
    def __init__(self, text):
        self.text = text + "$"  # add terminal symbol
        self.root = TrieNode()
        self.node_count = 0
        self._build()

    def _build(self):
        n = len(self.text)
        for i in range(n):
            self._insert_suffix(self.text[i:])

    def _insert_suffix(self, suffix):
        node = self.root
        for char in suffix:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

    def visualize(self, filename="suffix_trie"):
        dot = Digraph()
        self._assign_ids(self.root)
        self._add_edges(dot, self.root)

        # Get directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, filename)

        dot.render(output_path, format="png", cleanup=True)
        print(f"Visualization saved as {output_path}.png")


    def _assign_ids(self, node):
        if node.id is None:
            node.id = str(self.node_count)
            self.node_count += 1

        for child in node.children.values():
            self._assign_ids(child)

    def _add_edges(self, dot, node):
        dot.node(node.id, node.id)

        for char, child in node.children.items():
            dot.node(child.id, child.id)
            dot.edge(node.id, child.id, label=char)
            self._add_edges(dot, child)


# =========================
# USE IT HERE
# =========================

T = "abaaba"

trie = SuffixTrie(T)
trie.visualize("suffix_trie")
