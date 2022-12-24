DAY_NUM = "20"


def main(data):
    def solve(i: int, n: int):
        numbers = list([int(x) * i for x in data])
        indices = list(range(len(numbers)))
        for val in indices * n:
            indices.pop(j := indices.index(val))
            indices.insert((j + numbers[val]) % len(indices), val)
        index_0 = indices.index(numbers.index(0))
        return sum([numbers[indices[(index_0+x) % len(numbers)]] for x in [1000, 2000,
                                                                      3000]])

    print(f"Part 1: {solve(1, 1)}")
    print(f"Part 2: {solve(811589153, 10)}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
