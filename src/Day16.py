DAY_NUM = "16"
import re


class Valve:
    def __init__(self, name: str, flow_rate: int = None, connected_to: set[str] = None):
        self.name = name
        self.flow_rate = flow_rate
        self.dist_map = {a: 1 for a in connected_to}

    def __repr__(self):
        return f"Node {self.name}: {self.flow_rate}, {self.dist_map.keys()}"


def get_nodes(data):
    valves = {}
    starting_node = "AA"
    for row in data:
        start, flow_rate, to = re.match(
            "Valve (\w{2}) has flow rate=(\d*); tunnel.*valve[s]*([\w+, ]*[\w+])",
            row).groups()
        # (start, int(flow_rate), to.replace(" ", "").split(",")))
        valves[start] = Valve(start,
                              int(flow_rate),
                              set(to.replace(" ", "").split(","))
                              )
    return {name: valve for name, valve in valves.items() if valve.flow_rate or
            name == starting_node}


def parse_map(nodes: list[Valve]):
    """For nodes with flow rates: We want to return distances to other nodes with
    flow rates. We can then delete all nodes with no flow rates. Must still preserve
    connectivity though"""
    for node_a in nodes:
        for node_b in nodes:
            if node_a != node_b and node_a.name in node_b.dist_map:
                distance = node_b.dist_map[node_a.name]
                for adjacent_node in node_a.dist_map:
                    if adjacent_node == node_b.name:
                        continue
                    if adjacent_node not in node_b.dist_map:
                        node_b.dist_map[adjacent_node] = distance + node_a.dist_map[adjacent_node]
                    else:
                        node_b.dist_map[adjacent_node] = min(
                            node_b.dist_map[adjacent_node],
                            distance + node_a.dist_map[adjacent_node]
                        )
    for node in nodes:
        if not node.flow_rate:
            for n in nodes:
                if node.name in n.dist_map:
                    del n.dist_map[node.name]

    return {node.name: node for node in nodes if node.flow_rate or
            node.name == "AA"}


def traverse_map(
        node_map: dict[str, Valve],
        current_node: str,
        visited: list[str] = None,
        time: int = 0,
        max_time: int = 30
) -> tuple[int, list[str]]:
    if not visited:
        visited = []

    if time >= max_time:
        return 0, visited

    print(current_node)
    node = node_map[current_node]
    score = node.flow_rate * (max_time - time)
    new_visited = visited.append(current_node)

    child_scores = max([
        traverse_map(
            node_map,
            adj,
            new_visited,
            time + node.dist_map[adj] + 1,
            max_time
        ) for adj in node.dist_map if adj not in visited
    ])

    return score + child_scores[0], [current_node] + child_scores[1]


def main(data):
    nodes = get_nodes(data).values()
    mapped_nodes = parse_map(nodes)
    score, _ = traverse_map(node_map=mapped_nodes, current_node="AA")
    print(f"Part 1: {score}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
