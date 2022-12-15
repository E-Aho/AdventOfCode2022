from copy import copy

import numpy as np

DAY_NUM = "14"

BLOCK = "#"
SAND = "+"



class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

DOWN = Coordinate(0, 1)
UP = Coordinate(0, -1)
LEFT = Coordinate(-1, 0)
RIGHT = Coordinate(1, 0)
DOWN_LEFT = LEFT + DOWN
DOWN_RIGHT = RIGHT + DOWN

SOURCE = Coordinate(500, 0)

def coord_range(c1: Coordinate, c2: Coordinate) -> set[Coordinate]:
    def _range(i, j) -> range:
        ij = sorted((i, j))
        return range(ij[0], ij[1] + 1)  # inclusive range

    if c1.x == c2.x:
        return set(Coordinate(c1.x, y) for y in _range(c1.y, c2.y))
    return set(Coordinate(x, c1.y) for x in _range(c1.x, c2.x))


def parse_input(data: list[str]) -> tuple[tuple[Coordinate]]:
    rows = [row.replace(" ", "").split("->") for row in data]
    return (
        tuple(
            tuple(
                Coordinate(*(int(v) for v in point.split(",")))
                for point in row)
            for row in rows
        )
    )


def produce_map(block_sections: tuple[tuple[Coordinate]]) -> dict[Coordinate, str]:
    map = {}
    print(block_sections)
    for section in block_sections:
        for i in range(len(section) - 1):
            map.update({c: BLOCK for c in coord_range(section[i], section[i+1])})
    # print_map(map)
    return map


def pour_sand(map: dict, depth: int, has_floor: bool=False) -> bool:
    position = copy(SOURCE)

    while True:
        below = position + DOWN
        ll, lr = position + DOWN_LEFT, position + DOWN_RIGHT

        # Stopping conditions for falling sand
        if position.y > depth and not has_floor:
            return False  # Finish iter

        elif position.y == depth + 1:
            map[position] = SAND
            return True

        if position in map:  # Sand has clogged up at source, finish
            return False

        if below not in map:
            position = below
        elif ll not in map:
            position = ll
        elif lr not in map:
            position = lr
        else:
            # Finish falling
            map[position] = SAND
            return True


def fill_with_sand(map: dict, has_floor: bool = False):
    depth = max([v.y for v in map.keys()])
    sand_count = 0
    while pour_sand(map, depth, has_floor=has_floor):
        sand_count += 1
    return sand_count


def main(data):
    parsed = parse_input(data)
    map = produce_map(parsed)
    print_map(map)
    print(f"Part 1: {fill_with_sand(copy(map), has_floor=False)}")
    print(f"Part 2: {fill_with_sand(copy(map), has_floor=True)}")


def print_map(map: dict):
    """Utility function that prints out the simple maps to check everything is working ok"""
    out = ""
    y_range = range(*(min([p.y for p in map.keys()]), max([p.y for p in map.keys()]) + 1))
    x_range = range(*(min([p.x for p in map.keys()]), max([p.x for p in map.keys()]) + 1))
    for j in y_range:
        for i in x_range:
            if v := map.get(Coordinate(i, j)):
                out += v
            else:
                out += " "
        out += "\n"
    print(out)


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
