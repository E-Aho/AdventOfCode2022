import numpy as np

DAY_NUM = "14"

BLOCK = "#"
SAND = "+"

SOURCE = (500, 0)


def parse_input(data: list[str]) -> tuple[tuple[int]]:
    rows = [row.replace(" ", "").split("->") for row in data]
    return tuple(tuple
        (tuple(int(v) for v in x.split(",")) for x in row)
        for row in rows
    )


def produce_map(block_sections: tuple[tuple[int]]) -> dict[tuple, str]:
    map = {}
    print(block_sections)
    for section in block_sections:
        for i in range(len(section) - 1):
            start = section[i]
            end = section[i + 1]

            if end[1] < start[1] or end[0] < start[0]:
                start, end = end, start

            print(start, end)
            if start[0] == end[0]:
                new = {
                    (start[0], y): BLOCK
                    for y in range(start[1], end[1])
                    }
            else:
                new = {
                    (x, start[1]): BLOCK
                    for x in range(start[0], end[0])
                }
            map.update({**new, end: BLOCK, start: BLOCK})
            # breakpoint()

    return map

def pour_sand(map: dict, depth: int) -> bool:
    position = (500, 0)
    print_map(map)
    while True:
        below = (position[0], position[1] + 1)
        ll, lr = ((position[0] + dx, position[1] + 1) for dx in [1, -1])
        if position[1] > depth:
            print(position)
            return False  # Finish iter

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


def fill_with_sand(map: dict):
    depth = max([v[1] for v in map.keys()])
    sand_count = 0
    while pour_sand(map, depth):
        sand_count += 1
    print(sand_count)


def main(data):
    print(data)
    parsed = parse_input(data)
    map = produce_map(parsed)
    fill_with_sand(map)


def print_map(map: dict):
    out = ""
    for i in range(493, 503):
        for j in range(0, 10):
            if map.get((i, j)):
                out += map.get((i, j))
            else:
                out += "."
        out += "\n"
    print(out)



if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
