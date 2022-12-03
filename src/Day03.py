DAY_NUM = "03"

def get_priority(char: str):
    if char.isupper():
        return ord(char) - 64 + 26   # ASCII code, A starts at 65
    return ord(char) - 96      # ASCII code, a starts at 97

def main(data):
    # Part 1
    running_tot = 0
    for rucksack in data:
        comp_1, comp_2 = rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]
        shared_item = set(comp_1).intersection(set(comp_2)).pop()
        running_tot += get_priority(shared_item)

    print(f"Part 1: {running_tot}")

    # Part 2
    running_tot = 0
    group = []
    for rucksack in data:
        group.append(rucksack)

        if len(group) < 3:
            continue

        shared_item = (
            set(group[0])
            .intersection(set(group[1]))
            .intersection(set(group[2]))
            .pop()
        )

        running_tot += get_priority(shared_item)
        group = []
    print(f"Part 2: {running_tot}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        data = [line.strip() for line in file.readlines()]
    main(data)
