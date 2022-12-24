from collections import deque

DAY_NUM = "17"


class Rock:
    types = ["-", "+", "angle", "|", "square"]

    # x+ is real+, y+ is j+

    def __init__(self, pattern: str):
        self.rock = None
        self.height = 0

        if pattern == "-":
            self.rock = (0, 1, 2, 3)
            self.height = 0

        elif pattern == "|":
            self.rock = (0, 0 + 1j, 0 + 2j, 0 + 3j)
            self.height = 3

        elif pattern == "+":
            self.rock = (1, 0 + 1j, 1 + 1j, 2 + 1j, 1 + 2j)
            self.height = 2

        elif pattern == "angle":
            self.rock = (0, 1, 2, 2 + 1j, 2 + 2j)
            self.height = 2

        elif pattern == "square":
            self.rock = (0, 0 + 1j, 1, 1 + 1j)
            self.height = 1

        else:
            print(f"BAD PATTERN: {pattern}")
            return


rocks = [
    Rock(t) for t in Rock.types
]


class Chamber:
    def __init__(self, jet_pattern: str):
        self._chamber_width = 7
        self.spawn_dist = 3

        self.chamber = set()
        self.cache = {}
        self.jet_pattern = jet_pattern
        self.top_height = 0

        self.jets_index = 0
        self.rock_index = 0

    def get_spawn_height(self):
        return complex(2, self.top_height + 4)

    def check_valid(self, coordinate: complex) -> bool:
        return (0 <= coordinate.real < 7
                and coordinate.imag > 0
                and coordinate not in self.chamber)

    def check_rock_valid(
            self,
            coordinate: complex,
            direction: complex,
            rock: Rock
    ) -> bool:
        return all(self.check_valid(
            coordinate + direction + r
        ) for r in rock.rock)

    def print(self, height: int = 10):
        """Prints the chamber up to a given height"""
        val_to_str_map = {
            False: ".",
            True: "@"
        }
        out_str = ""
        for h in range(height, 0, -1):
            row = []
            for x in range(7):
                row.append(complex(x, h) in self.chamber)
            s = "".join([val_to_str_map.get(x) for x in row])
            out_str += s
            out_str += "\n"
        print(out_str)

    def reset(self):
        self.chamber = set()
        self.cache = {}
        self.top_height = 0

        self.jets_index = 0
        self.rock_index = 0

    def get_jet(self):
        jet = self.jet_pattern[self.jets_index]
        self.jets_index = (self.jets_index + 1) % len(self.jet_pattern)
        if jet == "<":
            return -1
        else:
            return 1

    def drop_rock(self, position: complex):
        rock = rocks[self.rock_index]
        self.rock_index = (self.rock_index + 1) % len(rocks)
        while True:
            jet = self.get_jet()

            if self.check_rock_valid(position, jet, rock):  # push via jet rock
                position += jet
            if self.check_rock_valid(position, -1j, rock):  # move rock down if it can
                position += -1j
            else:  # rock can't move down, finish moving
                self.chamber.update({position + r for r in rock.rock})
                self.top_height = max(self.top_height, int(position.imag + rock.height))
                return

    def drop_n_rocks(self, count: int) -> int:
        for step in range(count):
            pos = complex(2, self.top_height + 4)

            hash_key = self.rock_index, self.jets_index
            if hash_key in self.cache:
                # Turns out just using rock and jet indexes is enough! No need for
                # caching chamber status
                cached_step, cached_top = self.cache[hash_key]
                div, mod = divmod(count - step, step - cached_step)
                if mod == 0:
                    self.top_height = (
                            self.top_height + (self.top_height - cached_top) * div
                    )
                    return self.top_height
            else:
                self.cache[hash_key] = step, self.top_height
            self.drop_rock(pos)
        return self.top_height


def main(data):
    chamber = Chamber(data[0])
    print(f"Part 1: {chamber.drop_n_rocks(2022)}")
    chamber.reset()
    print(f"Part 2: {chamber.drop_n_rocks(int(1e12))}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
