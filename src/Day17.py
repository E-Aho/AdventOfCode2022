from collections import deque

import numpy as np

DAY_NUM = "17"


class Rock:
    types = ["-", "+", "angle", "|", "square"]

    def __init__(self, pattern: str):
        self.rock = None
        if pattern == "-":
            self.rock = np.ones([4, 1])
        elif pattern == "|":
            self.rock = np.ones([1, 4])
        elif pattern == "+":
            self.rock = np.zeros([3, 3])
            self.rock[1, :] = 1
            self.rock[:, 1] = 1
        elif pattern == "angle":
            self.rock = np.zeros([3, 3])
            self.rock[2, :] = 1
            self.rock[:, 2] = 1
        elif pattern == "square":
            self.rock = np.ones([2, 2])
        else:
            print(f"BAD PATTERN: {pattern}")
            return
        self.rock = self.rock.astype(int)

    def dim(self):
        return self.rock.shape


class Chamber:
    def __init__(self, jet_pattern: str):
        self._chamber_height = 10**5
        self._chamber_width = 7
        self.spawn_dist = 3

        self.chamber = np.zeros(shape=(self._chamber_width, self._chamber_height))
        self.top_height = 0
        self.jet_pattern = jet_pattern
        self.jets = None

    def next_jet(self):
        if not self.jets:
            self.jets = deque(self.jet_pattern)
        return self.jets.popleft()

    def get_spawn_height(self, rock_height: int = 1):
        return self._chamber_height - (self.top_height + rock_height + self.spawn_dist)

    def add_rock(self, coordinate: tuple, rock: Rock):
        top_of_new_rock = self._chamber_height - (coordinate[1])
        self.chamber[
            coordinate[0]: coordinate[0] + rock.dim()[0],
            coordinate[1]: coordinate[1] + rock.dim()[1]
        ] = rock.rock
        self.top_height = max(self.top_height, top_of_new_rock)


    def drop_rock(self, rock: Rock):
        coordinate = self.spawn_point(rock_height=rock.dim()[1])

        while True:
            # perform jet move
            jet_move = -1 if self.next_jet() == "<" else 1
            next_coordinate = (coordinate[0] + jet_move, coordinate[1])
            # print("Push", coordinate, next_coordinate)

            if self.check_coordinate_valid(next_coordinate, rock):
                coordinate = next_coordinate

            # perform drop
            next_coordinate = (coordinate[0], coordinate[1] + 1)
            # print("Drop", coordinate, next_coordinate)

            if self.check_coordinate_valid(next_coordinate, rock):
                coordinate = next_coordinate
            else:
                self.add_rock(coordinate, rock)
                # self.print()
                return

    def check_coordinate_valid(self, coordinate: tuple, rock: Rock):
        x = coordinate[0] + rock.dim()[0]
        y = coordinate[1] - rock.dim()[1] + 1
        if coordinate[0] < 0:
            return False
        
        if x <= self._chamber_width and y < self._chamber_height:
            target = self.chamber[
                coordinate[0]: coordinate[0] + rock.dim()[0],
                coordinate[1]: coordinate[1] + rock.dim()[1]
             ]
            overlap = np.any(
                target + rock.rock >= 2
            )
            return not overlap
        return False


    def spawn_point(self, rock_height: int = 1):
        return 2, self.get_spawn_height(rock_height)

    def print(self):
        val_to_str_map = {
            0: ".",
            1: "@"
        }

        out_str = ""
        for r in range(self.get_spawn_height(), self._chamber_height):
            present_rocks = list(self.chamber[:, r])
            s = "".join([val_to_str_map.get(x) for x in present_rocks])
            out_str += s
            out_str += "\n"
        # print(out_str)


rocks = [
    Rock(t) for t in Rock.types
]


def main(data):
    chamber = Chamber(data[0])
    for _ in range(2022):
        rock = rocks[_ % 5]
        chamber.drop_rock(rock)
    print(chamber.top_height)


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
