import numpy as np

DAY_NUM = "08"


def is_visible_in_direction(h: int, trees_in_direction: list[int]) -> bool:
    return h > max(trees_in_direction)


def get_score(h: int, directions: list[list[int]]):
    # Possibly a way to optimise this by caching already seen increasing sequences
    # However, even as is, main input runs in less than half a second, so is optimised enough for this use case
    def visible_in_direction(trees: list[int]):
        if len(trees) <= 1:    # shortcut in case near edges
            return len(trees)
        v = 1
        while v < len(trees):   # iterate across until we see a tree that blocks us
            if trees[v-1] < h:
                v += 1
            else:
                return v
        return v

    return np.prod([visible_in_direction(trees) for trees in directions])


def main(data):
    forest = np.array(data)
    n = len(data)
    visible_count = 4*(n-1)
    best_score = 0

    # check right from left, up from down, etc
    for i in range(1, n-1):
        for j in range(1, n-1):

            # Part 1
            h = forest[i][j]
            if (
                is_visible_in_direction(h, forest[i, :j]) or    # down
                is_visible_in_direction(h, forest[i, j+1:]) or  # up
                is_visible_in_direction(h, forest[:i, j]) or    # left
                is_visible_in_direction(h, forest[i+1:, j])     # right
            ):
                visible_count += 1

            # Part 2: get visibility in each direction
            # need to flip two directions to make the orders right (n=0 is adjacent to our tree)
            score = get_score(h, [
                np.flip(forest[i, :j]),
                forest[i, j + 1:],
                np.flip(forest[:i, j]),
                forest[i+1:, j]
            ])

            if score > best_score:
                best_score = score

    print(f"Part 1: {visible_count}")
    print(f"Part 2: {best_score}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [list(map(int, [*line.replace("\n", "")])) for line in file.readlines()]
    main(cleaned_data)
