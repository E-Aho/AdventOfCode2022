DAY_NUM = "05"


def main(data):
    # Part 1

    # Part 2
    pass


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip() for line in file.readlines()]
    main(cleaned_data)
