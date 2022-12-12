from collections import deque

DAY_NUM = "12"


def to_elev_map(data) -> tuple[dict, complex, complex]:
    out = {}
    start = ()
    end = ()
    for j in range(len(data)):
        row = data[j]
        for i in range(len(row)):
            char = row[i]
            if char == "S":
                start = complex(i, j)
                out[start] = 0
            elif char == "E":
                end = complex(i, j)
                out[end] = 25
            else:
                out[complex(i, j)] = (ord(char) - ord("a"))
    return out, start, end


def get_distance(map: dict, start: complex, end: complex) -> int:
    queue = deque([start])
    dist = {start: 0}
    while queue:
        coord = queue.popleft()
        queue.extend(
            new_points := [p for p in get_neighbors(coord, map) if p not in dist]
        )
        dist.update({p: dist[coord] + 1 for p in new_points})
        if end in dist:
            return dist[end]


def get_neighbors(coord: complex, map: dict) -> set[complex]:
    adjacent_coords = {(coord + delta) for delta in [1, 1j, -1, -1j]}
    valid_coords = {c for c in adjacent_coords if c in map}
    coords = {c for c in valid_coords if (map[c] - map[coord])
              <= 1 or map[c] < map[coord]}

    return coords


def main(data):
    print(data)
    map, start, end = to_elev_map(data)
    print(f"Part 1: {get_distance(map, start, end)}")

    # Obviously non-optimal, but this solves it in less than a second still
    possible_starts = {coord for coord, val in map.items() if val == 0}
    distances = [get_distance(map, x, end) for x in possible_starts]
    print(f"Part 2: {min([d for d in distances if d is not None])}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
