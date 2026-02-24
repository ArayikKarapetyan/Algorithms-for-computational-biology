import os
from graphviz import Digraph


class Node:
    def __init__(self, start_pos=None, length=None, suffix_id=None):
        self.children = {}
        self.id = None
        self.start_pos = start_pos
        self.length = length
        self.suffix_id = suffix_id  # only for leaves


class Edge:
    def __init__(self, start, end, dest):
        self.start = start
        self.end = end
        self.dest = dest


class SuffixTree:
    def __init__(self, text):
        self.text = text + "$"
        self.root = Node()
        self.node_count = 0
        self._build()

    def _build(self):
        n = len(self.text)
        for i in range(n):
            self._insert_suffix(i)

    def _insert_suffix(self, start_index):
        current = self.root
        i = start_index

        while i < len(self.text):
            char = self.text[i]

            if char not in current.children:
                leaf = Node(suffix_id=start_index)
                current.children[char] = Edge(i, len(self.text), leaf)
                return

            edge = current.children[char]
            label_start = edge.start
            label_end = edge.end

            j = 0
            while (label_start + j < label_end and
                   i + j < len(self.text) and
                   self.text[label_start + j] == self.text[i + j]):
                j += 1

            if label_start + j == label_end:
                current = edge.dest
                i += j
            else:
                # Split
                split_node = Node(start_pos=label_start, length=j)

                # Old continuation
                old_edge = Edge(label_start + j, label_end, edge.dest)
                split_node.children[self.text[label_start + j]] = old_edge

                # New leaf
                leaf = Node(suffix_id=start_index)
                new_edge = Edge(i + j, len(self.text), leaf)
                split_node.children[self.text[i + j]] = new_edge

                current.children[char] = Edge(label_start, label_start + j, split_node)
                return

    # ========================
    # Visualization
    # ========================

    def visualize(self, filename="suffix_tree"):
        dot = Digraph()
        dot.attr("node", shape="circle")

        self._assign_ids(self.root)
        self._add_nodes(dot, self.root)
        self._add_edges(dot, self.root)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, filename)

        dot.render(output_path, format="png", cleanup=True)
        print(f"Visualization saved as {output_path}.png")

    def _assign_ids(self, node):
        if node.id is None:
            node.id = str(self.node_count)
            self.node_count += 1
        for edge in node.children.values():
            self._assign_ids(edge.dest)

    def _add_nodes(self, dot, node):
        # Root
        if node == self.root:
            dot.node(node.id, "root", color="black")
        # Leaf
        elif node.suffix_id is not None:
            dot.node(
                node.id,
                f"<<b>{node.suffix_id}</b>>",
                color="black"
            )
        # Internal node
        else:
            label = f"({node.start_pos},{node.length})"
            dot.node(
                node.id,
                label,
                color="blue"
            )

        for edge in node.children.values():
            self._add_nodes(dot, edge.dest)

    def _add_edges(self, dot, node):
        for edge in node.children.values():
            label = self.text[edge.start:edge.end]
            dot.edge(node.id, edge.dest.id, label=label)
            self._add_edges(dot, edge.dest)


# =========================
# USE IT HERE
# =========================

T = "acgaaagtcaaagtccagagattcag"

tree = SuffixTree(T)
tree.visualize("suffix_tree_")
