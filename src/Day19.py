import re

import numpy as np

DAY_NUM = "19"


class Robot:
    def __init__(self, takes: list, makes: list):
        self.takes = np.array(takes)
        self.makes = np.array(makes)


class RobotBlueprint:
    def __init__(self, blueprint: str):
        values = list(map(int, re.findall(r'\d+', blueprint)))
        self.name = values[0]
        b = values[1]
        c = values[2]
        d = values[3]
        e = values[4]
        f = values[5]
        g = values[6]

        # Define bots as NP arrays of takes and makes, where indexes are:
        # 0 = Geode
        # 1 = Obsidian
        # 2 = Clay
        # 3 = Ore
        self.bots = (
            Robot(takes=[0, 0, 0, b], makes=[0, 0, 0, 1]),  # Ore bot
            Robot(takes=[0, 0, 0, c], makes=[0, 0, 1, 0]),  # Clay bot
            Robot(takes=[0, 0, e, d], makes=[0, 1, 0, 0]),  # Obsidian bot
            Robot(takes=[0, g, 0, f], makes=[1, 0, 0, 0]),  # Geode bot
            Robot(takes=[0, 0, 0, 0], makes=[0, 0, 0, 0])   # Null robot
        )


def run_blueprint(blueprint: RobotBlueprint, time_limit: int) -> int:
    """For a given blueprint, calculates the best number of ore it can get"""

    def heuristic(state):
        """Basically, we care more about what we make than have, so append that
        after so if two states have the same amount in each, take one that makes
        most of 'higher value' material"""
        # NB: State = (have, make)
        return tuple(state[0] + state[1]) + tuple(state[1])

    def prune_queue(search_queue, pruned_queue_length: int = 1000):
        """Done to only search on relatively good options"""
        return sorted(
            search_queue,
            key=lambda s: heuristic(s),
            reverse=True
        )[:pruned_queue_length]

    # tracks what we have, and make, for each state in search
    # First = what we have, second = what we make each second
    states = [[np.array([0, 0, 0, 0]), np.array([0, 0, 0, 1])]]

    for _ in range(time_limit):
        # add in all robots we can make for a given blueprint in each unit time
        # then prune to only track 'good' options
        todo_queue = list()
        for have, make in states:
            for robot in blueprint.bots:
                if all(robot.takes <= have):
                    todo_queue.append((have + make - robot.takes, make + robot.makes))
        states = prune_queue(todo_queue)
    return max(have[0] for have, _ in states)


def main(data):
    blueprints = [RobotBlueprint(l) for l in data]
    part1 = 0
    part2 = 1
    for blueprint in blueprints:
        part1 += run_blueprint(blueprint, 24) * blueprint.name
        if blueprint.name < 4:
            part2 *= run_blueprint(blueprint, 32)

    print(f"Part 1: {part1}")  # 1150
    print(f"Part 2: {part2}")  # 37367


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
