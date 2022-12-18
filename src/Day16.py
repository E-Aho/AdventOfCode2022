import numpy as np
import re
from itertools import permutations


DAY_NUM = 16
STARTING_VALVE = "AA"


class Valve:
    def __init__(self, name: str, flow: int, connections: set[str]):
        self.name = name
        self.connections = connections
        self.flow = flow


def parse_data(data):
    valves = []
    for row in data:
        start, flow_rate, to = re.match(
            "Valve (\w{2}) has flow rate=(\d*); tunnel.*valve[s]*([\w+, ]*[\w+])",
            row).groups()
        valves.append(Valve(
            start,
            int(flow_rate),
            set(to.replace(" ", "").split(","))
        ))
    return valves


def get_adjacency_array(nodes: list[Valve]) -> np.ndarray:
    """Takes in a list of valves"""
    index_mapping = {n.name: i for i, n in enumerate(nodes)}
    adjacency = np.zeros((len(nodes), len(nodes)), dtype=int)
    for n in nodes:
        for t in n.connections:
            adjacency[index_mapping[n.name], index_mapping[t]] = 1
    return adjacency


def get_distance_array(adjacency: np.ndarray) -> np.ndarray:
    """Takes in adjacency matrix, returns integer time distances to different valves"""
    large_n = 10**4

    length = adjacency.shape[0]
    distances = np.where(adjacency, adjacency, large_n)
    d = np.diag([1] * length, 0)
    distances = np.where(d, 0, distances)

    for i, row in enumerate(distances):
        neighbours = np.where(row != large_n)[0]
        for n1, n2 in permutations(neighbours, 2):
            d = min(row[n1] + row[n2], distances[n1, n2])
            distances[n1, n2] = d
            distances[n2, n1] = d
    return distances.astype(int)


class Path:

    def __init__(self,
                 time: int,
                 initial_valve: int) -> None:
        self.time = time
        self.visited = [initial_valve]
        self.pressure = 0

    def copy(self):
        new_path = Path(time=self.time,
                        initial_valve=self.visited[0])
        new_path.visited = self.visited.copy()
        new_path.pressure = self.pressure
        return new_path


def complete_paths(valves: list[Valve], total_time, stopping=False):
    adjacency_array = get_adjacency_array(valves)
    distance_array = get_distance_array(adjacency_array)
    flows = np.array([v.flow for v in valves])
    valve_index = [i for i, v in enumerate(valves) if v.name == STARTING_VALVE][0]

    path = Path(total_time, valve_index)
    stack = [path]
    all_paths = []
    while stack:
        path = stack.pop(0)
        if stopping: all_paths.append(path)
        new_paths = []
        all_next_valves = [i for i, f in enumerate(flows) if
                           (i not in path.visited) and (f != 0)]
        valve_times = [distance_array[path.visited[-1]][v] + 1 for v in all_next_valves]
        for time, valve in zip(valve_times, all_next_valves):
            if path.time - time <= 0:
                continue
            extended_path = path.copy()
            extended_path.time -= time
            extended_path.visited.append(valve)
            extended_path.pressure += (path.time - time) * flows[valve]
            new_paths.append(extended_path)
        if new_paths:
            stack.extend(new_paths)
        else:
            if not stopping:
                all_paths.append(path)
    return all_paths


def max_pressure_dual_paths(paths):
    ranked_paths = sorted(paths, key=lambda x: x.pressure, reverse=True)
    max_p = 0
    j = 0
    for i, a in enumerate(ranked_paths):
        if i > j: continue
        x = set(tuple(a.visited[1:]))
        for j, b in enumerate(ranked_paths[i + 1:], i):
            if a.pressure + b.pressure <= max_p:
                break
            y = set(tuple(b.visited[1:]))
            if len(set.intersection(x, y)) == 0:
                if a.pressure + b.pressure > max_p:
                    max_p = a.pressure + b.pressure
    return max_p


def main(data: str):
    valves = parse_data(data)

    paths = complete_paths(valves, 30)
    p1 = max([p.pressure for p in paths])
    print(f"Part 1: {p1}")

    p2_paths = complete_paths(valves, 26, stopping=True)
    p2 = max_pressure_dual_paths(p2_paths)
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip() for line in file.readlines()]
    main(cleaned_data)
