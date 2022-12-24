from copy import copy

DAY_NUM = "21"


class Monkey:
    def __init__(self, line: str = None, inverted: bool = False):
        if not "_line" in self.__dict__:
            self._line = line

        name, _val = self._line.split(": ")
        self.name = name
        val = _val.split()

        self.value = None
        self.depends_on = None
        self.op = None
        self.parent = None
        # self.op_str = None

        if len(val) == 1:  # Is a leaf
            self.value = int(val[0])
        else:
            self.op_str = val[1]
            self.depends_on = val[0], val[-1]
            self.op = parse_op(self.op_str, inverted)

    def get_value(self, tree):
        if not self.depends_on:
            return self.value

        monkey_a, monkey_b = tree[self.depends_on[0]], tree[self.depends_on[1]]
        value = int(self.op(monkey_a.get_value(tree), monkey_b.get_value(tree)))
        self.value = value
        return self.value


def parse_op(op_str: str, inv: bool = False):
    op_map = {
        "+": lambda x, y: x + y,
        "*": lambda x, y: x * y,
        "-": lambda x, y: x - y,
        "/": lambda x, y: x / y
    }

    inv_map = {
        "+": lambda x, y: x - y,
        "-": lambda x, y: x + y,
        "*": lambda x, y: x / y,
        "/": lambda x, y: x * y,
    }
    if inv:
        return inv_map[op_str]
    return op_map[op_str]  # raises exception if unsupported op found

def invert_tree(tree, start: str):
    curr_node = start

    def invert(current_node: str, parent_node: str, tree: dict):
        # a = b + c ->  c = a - b
        cousin = [x for x in tree[parent_node].depends_on if x != current_node][0]
        tree[current_node].depends_on = [cousin, parent_node]
        tree[current_node].parent = None
        tree[current_node].op = parse_op(tree[parent_node].op_str, inv=True)
        tree[current_node].value = None

    seen = set()
    while curr_node != "root":
        seen.add(curr_node)
        _parent = tree[curr_node].parent
        run = invert(curr_node, _parent, tree)
        curr_node = _parent

    tree["root"].op = None
    tree["root"].value = [tree[x].value for x in tree["root"].depends_on if x not in
                          seen][0]
    tree["root"].depends_on = None

def main(data):
    monkeys = [Monkey(line) for line in data]
    tree = {m.name: m for m in monkeys}
    for name, monkey in tree.items():
        if monkey.depends_on:
            for kid in monkey.depends_on:
                tree[kid].parent = name

    root = tree["root"]
    print(int(root.get_value(tree)))

    # Part 2
    humn = tree["humn"]
    inverted_tree = invert_tree(tree, "humn")
    print(humn.get_value(tree))


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}example.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
