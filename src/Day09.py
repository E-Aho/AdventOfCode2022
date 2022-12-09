import numpy as np

DAY_NUM = "09"

up, down = np.array((0, 1)), np.array((0, -1))
left, right = np.array((-1, 0)), np.array((1, 0))


def perform_move(rope: list[np.array],  dir: np.array, visited: set):
    head = rope[0]
    head += dir
    for i in range(len(rope) - 1):
        h, t = rope[i], rope[i+1]
        if max(abs(h-t)) > 1:
            dif = h-t
            move = np.array(list(round(v/abs(v)) if abs(v) != 0 else 0 for v in dif))
            t += move

    visited.add(str(rope[-1]))


def main(data):
    visited_p1 = set()
    visited_p2 = set()
    direction_map = {
        "R": np.array((1, 0)),
        "L": np.array((-1, 0)),
        "U": np.array((0, 1)),
        "D": np.array((0, -1))
    }

    p1_rope = [np.array([0, 0]) for _ in range(2)]
    p2_rope = [np.array([0, 0]) for _ in range(10)]

    for row in data:
        direction, count = direction_map.get(row.split()[0]), int(row.split()[1])
        for _ in range(count):
            perform_move(p1_rope, direction, visited_p1)
            perform_move(p2_rope, direction, visited_p2)

    print(f"Part 1:{len(visited_p1)}")
    print(f"Part 2:{len(visited_p2)}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
