DAY_NUM = "06"


def main(data):
    def solve(seq_len):
        # could optimize this for sure, but it works fine for this scale
        # if we're looking at significantly larger sequences,
        # would need to adjust strategy

        for i in range(len(data)):
            packet = data[i: i + seq_len]
            if len(set(packet)) == seq_len:
                return i + seq_len

    print(f"Part 1: {solve(4)}")
    print(f"Part 2: {solve(14)}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.replace("\n", "") for line in file.readlines()][0]
    main(cleaned_data)
