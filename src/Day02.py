from abc import ABC

DAY_NUM = "02"

ROCK = "rock"
PAPER = "paper"
SCISSOR = "scissors"


def convert_input(input_str: str) -> str:
    mapping = {
        "A": ROCK,
        "B": PAPER,
        "C": SCISSOR,
        "X": ROCK,
        "Y": PAPER,
        "Z": SCISSOR,
    }
    return mapping.get(input_str)


win_map = {
    ROCK: SCISSOR,
    SCISSOR: PAPER,
    PAPER: ROCK
}

lose_map = {
    ROCK: PAPER,
    SCISSOR: ROCK,
    PAPER: SCISSOR
}


class StrategyGuide(ABC):
    tie_score = 3
    win_score = 6
    lose_score = 0

    choice_score = {
        ROCK: 1,
        PAPER: 2,
        SCISSOR: 3
    }


class Part1StrategyGuide(StrategyGuide):

    def _did_win(self, opp, you) -> int:
        if opp == you:
            return self.tie_score
        elif win_map.get(you) == opp:
            return self.win_score
        else:
            return self.lose_score

    def eval(self, opponent: str, yours: str) -> int:

        win_score = self._did_win(opponent, yours)
        choice_score = self.choice_score.get(yours)
        return win_score + choice_score


class Part2StrategyGuide(StrategyGuide):

    def _did_win(self, yours) -> int:
        win_map = {
            "X": self.lose_score,
            "Y": self.tie_score,
            "Z": self.win_score
        }
        return win_map.get(yours)

    def _get_choice_score(self, opponent, yours) -> int:
        choice_map = {
            "X": lambda opp: win_map.get(opp),  # they must win -> you lose
            "Y": lambda opp: opp,
            "Z": lambda opp: lose_map.get(opp)  # they must lose -> you win
        }
        return self.choice_score.get(choice_map.get(yours)(opponent))

    def eval(self, opponent: str, yours: str) -> int:
        return self._get_choice_score(opponent, yours) + self._did_win(yours)


def main(data):
    # Part 1
    part_1_strategy = Part1StrategyGuide()
    tot = 0
    for opp, you in data:
        opp, you = convert_input(opp), convert_input(you)
        tot += part_1_strategy.eval(opp, you)
    print(f"Part 1: {tot}")

    part_2_strategy = Part2StrategyGuide()
    tot = 0
    for opp, you in data:
        opp = convert_input(opp)
        tot += part_2_strategy.eval(opp, you)
    print(f"Part 2: {tot}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        stipped_data = [line.strip().split() for line in file.readlines()]
    main(stipped_data)
