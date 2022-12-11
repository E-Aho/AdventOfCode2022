import math

import numpy as np

DAY_NUM = "11"


def parse_op(line: str):
    op_str = line.split(" ")[-2]
    val_str = line.split(" ")[-1]
    if val_str == "old":
        if op_str == "*":
            return lambda x: x ** 2
        elif op_str == "+":
            return lambda x: x * 2
        else:
            raise Exception(f"Op fallthrough for {line}")

    val = int(val_str)
    if op_str == "+":
        return lambda x: x + val
    elif op_str == "*":
        return lambda x: x * val
    else:
        raise Exception(f"Op fallthrough for {line}")


class Monkey:
    def __init__(self, lines: list):
        self.id = int(lines[0].split()[-1].replace(":", ""))
        self.items = [int(x) for x in lines[1].replace(" ", "").split(":")[1].split(
            ",")]
        self.op = parse_op(lines[2])
        self.test_val = int(lines[3].split(" ")[-1])
        self.test = lambda x: np.mod(x, self.test_val) == 0
        self.to_true = int(lines[4].split(" ")[-1])
        self.to_false = int(lines[5].split(" ")[-1])
        self.inspection_count = 0

    def do_inspections(self, max_factor: int = None):
        true_out, false_out = [], []
        while self.items:
            item = self.items.pop()
            self.inspection_count += 1
            if max_factor is None:
                worry = self.op(item) // 3
            else:
                # We don't care about the whole number, just the remainder

                # Therefore, we only need to track the worry, modulo the product of
                # all (unique) division checks.
                worry = self.op(item) % max_factor
            if self.test(worry):
                true_out.append(worry)
            else:
                false_out.append(worry)
        return true_out, false_out

    def __repr__(self):
        return str(self.id)


def get_monkeys(data: list[str]) -> list[Monkey]:
    running_rows = []
    monkeys = []
    for i in range(len(data)):
        if data[i] == "":
            monkeys.append(Monkey(running_rows))
            running_rows = []
        else:
            running_rows.append(data[i])
    monkeys.append(Monkey(running_rows))
    return monkeys


def operate(monkeys: list[Monkey], i: int, total_factor: int = None):
    monkey_i = monkeys[i]
    trues, falses = monkey_i.do_inspections(total_factor)
    monkeys[monkey_i.to_true].items += trues
    monkeys[monkey_i.to_false].items += falses


def complete_round(monkeys: list[Monkey], total_factor: int = None):
    for i in range(len(monkeys)):
        operate(monkeys, i, total_factor)


def main(data):
    monkeys = get_monkeys(data)
    for _ in range(20):
        complete_round(monkeys)
    inspection_counts = sorted([monkey.inspection_count for monkey in monkeys],
                               reverse=True)
    print(f"Part 1: {inspection_counts[0] * inspection_counts[1]}")

    # Part 2:
    monkeys = get_monkeys(data)
    total_factor = math.prod([monkey.test_val for monkey in monkeys])
    for _ in range(10000):
        complete_round(monkeys, total_factor)
    inspection_counts = sorted([monkey.inspection_count for monkey in monkeys],
                               reverse=True)
    print(f"Part 2: {inspection_counts[0] * inspection_counts[1]}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
