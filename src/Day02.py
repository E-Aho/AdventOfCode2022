DAY_NUM = "02"


def main(data):
    pass


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        data = [line.strip() for line in file.readlines()]
    main(data)
