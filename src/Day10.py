DAY_NUM = "10"


class CRTProgram:

    def __init__(self):
        self.cycle = 1
        self.register = {"X": 1}
        self.signal_strength = []
        self.x = self.register["X"]
        self.op_map = {
            "noop": self.noop,
            "addx": self.addx
        }

        self.screen = []

    def go(self, n):
        for _ in range(n):
            # Part 1:
            if self.cycle % 40 == 20:  # 20, 60, 100, etc
                self.signal_strength.append(self.cycle * self.register["X"])

            # Part 2:
            sprite_width = 1
            if abs((self.cycle - 1) % 40 - self.register["X"]) <= sprite_width:
                self.screen.append(1)
            else:
                self.screen.append(0)
            self.cycle += 1

    def noop(self, *args):
        self.go(1)

    def addx(self, val: int):
        self.go(2)
        self.register["X"] += val

    def perform_action(self, s: str):
        spl = s.split()
        op = spl[0]
        val = None
        if len(s.split()) > 1:
            val = int(s.split()[-1])
        self.op_map[op](val)

    def print_screen(self):
        _0 = " "
        _1 = "█"

        print_str = []
        for i in range(len(self.screen)):
            if i % 40 == 0:
                print_str.append("\n")
            if self.screen[i]:
                print_str.append(_1)
            else:
                print_str.append(_0)
        print("".join(print_str))

def main(data):
    crt = CRTProgram()
    for row in data:
        crt.perform_action(row)
    print(f"Part 1: {sum(crt.signal_strength)}")
    print(f"Part 2:")
    crt.print_screen()

if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
