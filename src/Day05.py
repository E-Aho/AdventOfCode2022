from typing import List, Tuple

DAY_NUM = "05"


def parse_crates(
        crate_rows: list[str],
        stack_indexes: dict[int, int]
) -> list[list[str]]:
    stacks = [[] for _ in range(len(stack_indexes.keys()))]
    for r in range(len(crate_rows)-1, -1, -1):
        try:
            row = crate_rows[r]
            for stack, index in stack_indexes.items():
                crate = row[index]
                stacks[stack - 1].append(crate) if crate != " " else None
        except IndexError:  # column was not present there
            pass
    return stacks


def parse_instructions(instruction_rows: list[str]) -> list[tuple[int, ...]]:
    out = []
    for row in instruction_rows:
        out.append(
            tuple(int(x) for x in (
                row
                .replace("move ", "")
                .replace("from ", "")
                .replace("to ", "")
                .split()
            )))
    return out


def parse_input(input_rows: list[str]) -> tuple[list[list[str]], list[tuple[int, ...]]]:
    crate_rows = []
    instruction_rows = []
    stack_indexes = dict()

    done_all_crates = False
    for i in range(len(input_rows)):
        r = input_rows[i]

        if not r:
            pass
        elif r[1] == "1":
            done_all_crates = True
            stack_indexes = {int(j): i for i, j in enumerate(r) if j != " "}
        elif not done_all_crates:
            crate_rows.append(r)
        elif r[0] == "m":
            instruction_rows.append(r)

    crate_stacks = parse_crates(crate_rows, stack_indexes)
    instructions = parse_instructions(instruction_rows)
    return crate_stacks, instructions


def main(data):
    # Part 1
    stacks, instructions = parse_input(data)
    for (n, from_stack, to) in instructions:
        moved = []
        for _ in range(n):
            moved.append(stacks[from_stack-1].pop())     # pop n from top of new column
        stacks[to-1] += moved                            # add to new column
    print(f"Part 1: {''.join([x[-1] for x in stacks])}")

    # Part 2
    stacks, instructions = parse_input(data)
    for (n, from_stack, to) in instructions:
        moved = stacks[from_stack-1][-n:]                # grab top n from old stack
        del stacks[from_stack-1][-n:]                    # remove from old stack
        stacks[to-1] += moved                            # move to new stack
    print(f"Part 2: {''.join([x[-1] for x in stacks])}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
