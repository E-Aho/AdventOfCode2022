DAY_NUM = "07"


def main(data):
    pass


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.replace("\n", "") for line in file.readlines()][0]
    main(cleaned_data)
