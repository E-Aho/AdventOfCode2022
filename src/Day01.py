DAY_NUM = "01"


def main(data):
    # Part 1
    run_tots = [0]
    max_val = 0
    for val in data:
        if val != '':
            run_tots[-1] += int(val)
        else:
            if run_tots[-1] > max_val:
                max_val = run_tots[-1]
            run_tots.append(0)
    print(f"Part 1 solution: {max_val}")

    # Part 2:
    # Could do more optimally with a heap for the top N during run
    # But not at all limited by run time for this, below solution is fine

    s = sorted(run_tots, reverse=True)
    top_3 = sum(s[:3])
    print(f"Part 2 solution: {top_3}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        data = [line.strip() for line in file.readlines()]
    main(data)
