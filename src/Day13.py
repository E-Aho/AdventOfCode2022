import ast

DAY_NUM = "13"


def parse_input(data: list[str]):
    packets = []
    pair = []
    for i in range(len(data)):
        row = data[i]
        if row == "":
            packets.append(pair)
            pair = []
        else:
            pair.append(ast.literal_eval(row))
    packets.append(pair)
    return packets

def compare_ints(left, right):
    if left == right:
        return
    elif left < right:
        return True
    else:
        return False

def compare_packets(left, right):
    i = 0
    len_l = len(left)
    len_r = len(right)
    while True:
        # Check if we've reached end, and return as expected for that
        if i == len_l and i == len_r:
            return
        elif i == len_l:
            return True
        elif i == len_r:
            return False

        l, r = left[i], right[i]
        if isinstance(l, list) and isinstance(r, list):
            if (val := compare_packets(l, r)) is not None:
                return val
        elif isinstance(l, int) and isinstance(r, int):
            if (val := compare_ints(l, r)) is not None:
                return val
        else:
            if not isinstance(l, list):
                l = [l]
            else:
                r = [r]
            if (val := compare_packets(l, r)) is not None:
                return val

        i += 1

def bubble_sort(packets: list):
    "Could optimize with better algorithm but this works for our use case"
    n = len(packets)
    for i in range(n):
        for j in range(0, n-i-1):
            if not compare_packets(packets[j], packets[j+1]):
                packets[j+1], packets[j] = packets[j], packets[j+1]
    return packets

def main(data):
    # parse input to structure
    packets = parse_input(data)
    packet_sorted = [compare_packets(*packet) for packet in packets]
    val = [i + 1 for i, v in enumerate(packet_sorted) if v is True]
    print(f"Part 1: {sum(val)}")

    # Part 2
    markers = [[[2]], [[6]]]
    all_packets = [item for pair in packets for item in pair]
    all_packets += markers

    sorted_packets = bubble_sort(all_packets)
    marker_positions = [i+1 for i, v in enumerate(sorted_packets) if v in markers]
    print(f"Part 2: {marker_positions[0] * marker_positions[1]}")



if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
