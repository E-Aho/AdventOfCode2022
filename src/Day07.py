import abc
import math
from abc import ABC
from typing import Optional

DAY_NUM = "07"


class Node(ABC):
    def __init__(self, name: str, parent):
        self.name = name
        self.children = dict()
        self.parent = parent

    @abc.abstractmethod
    def get_size(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass


class File(Node):
    def __init__(self, name: str, parent: Node, size: int):
        super().__init__(name, parent)
        self.size = size

        self.name = name.split(".")[0]

    def get_size(self):
        return self.size

    def get_name(self):
        return self.parent.get_name() + f"/{self.name}.{self.type}"

    def __repr__(self):
        return self.name


class Dir(Node):
    def __init__(self, name: str, parent: Optional[Node]):
        super().__init__(name, parent)

    def subdirs(self) -> list[Node]:
        return [x for x in self.children.values() if isinstance(x, Dir)]

    def get_size(self):
        return sum([x.get_size() for x in self.children.values()])

    def get_name(self):
        return self.parent.get_name() + f"/{self.name}"

    def __repr__(self):
        return self.get_name()


class Root(Dir):
    def __init__(self):
        super().__init__("r:", None)

    def get_name(self):
        return "Root"


def parse_tree(rows):
    root_dir = Root()
    dir_map = {}
    current_dir = root_dir

    def cd(dir: str, current=current_dir):
        if dir == "..":
            return current.parent
        elif dir in current.children:
            return current.children[dir]
        print("Fallthrough!")

    def ls(rows: list[str], current: Dir):
        for row in rows:
            val, name = row.split(" ")
            if val == "dir":
                new_dir = Dir(name=name, parent=current)
                dir_map[new_dir.get_name()] = new_dir
                current.children[name] = new_dir
            else:  # It's a file
                current.children[name] = File(name, parent=current, size=int(val))

        return current

    i = 1
    while i < len(rows):
        row = rows[i]
        if row[0] == "$":
            operator = row.split(" ")[1]
            if operator == "cd":
                current_dir = cd(row.split(" ")[-1], current_dir)
                i += 1
            elif operator == "ls":
                found_rows = []
                i += 1
                while i < len(rows) and rows[i][0] != "$":
                    found_rows.append(rows[i])
                    i += 1
                current_dir = ls(found_rows, current_dir)

    return root_dir


def solve_p1(root: Dir):
    size_lim = 100000
    running_count = 0
    for subdir in root.subdirs():
        running_count += solve_p1(subdir)
    if (sz := root.get_size()) <= size_lim:
        running_count += sz
    return running_count

def solve_p2(root: Dir, space_needed: int=None):
    system_size = 70000000
    target = 30000000
    if space_needed is None:
        unused_space = system_size - root.get_size()
        space_needed = target - unused_space

    current_best = math.inf
    for subdir in root.subdirs():
        new_val = solve_p2(subdir, space_needed)
        if current_best > new_val > space_needed:
            current_best = new_val

    new_val = root.get_size()
    if current_best > new_val > space_needed:
        current_best = new_val
    return current_best

def main(data):
    tree = parse_tree(data)
    print(tree.get_size())
    print(f"Part 1: {solve_p1(tree)}")
    print(f"Part 2: {solve_p2(tree)}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
