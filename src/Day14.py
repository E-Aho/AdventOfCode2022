DAY_NUM = "14"


def main(data):
    pass


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip() for line in file.readlines()]
    main(cleaned_data)
