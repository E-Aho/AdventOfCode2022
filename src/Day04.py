DAY_NUM = "04"


def main(data):
    part_1_count = 0
    part_2_count = 0
    for row in data:

        elf_1, elf_2 = (
            tuple(map(int, x.split("-")))
            for x in row.split(",")
        )

        vals_1 = set(range(elf_1[0], elf_1[1] + 1))
        vals_2 = set(range(elf_2[0], elf_2[1] + 1))

        # Part 1
        if vals_1.issubset(vals_2) or vals_2.issubset(vals_1):
            part_1_count += 1

        if len(vals_1.intersection(vals_2)) > 0:
            part_2_count += 1


    print(f"Part 1: {part_1_count}")
    print(f"Part 2: {part_2_count}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip() for line in file.readlines()]
    main(cleaned_data)
