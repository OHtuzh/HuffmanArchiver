class Node:
    def __init__(self, freq: int = None, data=None, left=None, right=None):
        self.__freq: int = freq
        self.__data: int = data
        self.__left: Node = left
        self.__right: Node = right
        self.parent: Node = None

    def get_data(self):
        return self.__data

    def get_frequency(self) -> int:
        return self.__freq

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right


def build_huffman_tree_and_table(frequency: dict) -> (Node, dict[str, str]):
    nodes: list[Node] = [Node(freq, ord(let)) for let, freq in sorted(frequency.items(), key=lambda o: o[1])]
    if len(nodes) == 1:
        return Node(nodes[0].get_frequency(), None, nodes[0]), {nodes[0].get_data(): '0'}

    leafs = nodes.copy()
    while len(nodes) > 1:
        new_node = Node(nodes[0].get_frequency() + nodes[1].get_frequency(), None, nodes[0], nodes[1])
        nodes[0].parent = nodes[1].parent = new_node
        nodes = nodes[2:]
        nodes.append(new_node)
        nodes.sort(key=lambda o: o.get_frequency())
    table = dict()
    for leaf in leafs:
        path = []
        tmp = leaf
        while tmp.parent is not None:
            if tmp == tmp.parent.get_left():
                path.append('0')
            else:
                path.append('1')
            tmp = tmp.parent
        table[leaf.get_data()] = ''.join(reversed(path))

    return nodes[0], table
