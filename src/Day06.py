DAY_NUM = "06"


def main(data):
    # Part 1
    pass


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
