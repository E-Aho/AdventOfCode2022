import re
from src.Day14 import Coordinate

DAY_NUM = "15"


def manhattan_distance(c1: Coordinate, c2: Coordinate) -> int:
    return abs(c1.y - c2.y) + abs(c1.x - c2.x)


def get_coords(row: str):
    ints = [int(x) for x in re.findall(r"-*[0-9]+", row)]
    return Coordinate(ints[0], ints[1]), Coordinate(ints[2], ints[3])


def calculate_possible_beacons(sensors: list[tuple[Coordinate, Coordinate]], target_y: int):
    """Non optimal solution, but fast enough"""
    non_beacons = set()
    beacons = set()
    for sensor_pair in sensors:
        sensor, nearest_beacon = sensor_pair
        if sensor.y == target_y:
            non_beacons.add(sensor.x)
        if nearest_beacon.y == target_y:
            beacons.add(nearest_beacon.y)

        distance_from_row = abs(sensor.y - target_y)
        distance_from_beacon = manhattan_distance(sensor, nearest_beacon)
        if (d := distance_from_beacon - distance_from_row) > 0:
            possible_x = set(range(sensor.x - d, sensor.x + d+1))
            non_beacons.update(possible_x)
    non_beacons -= beacons
    return len(non_beacons)


def find_distress_beacon(sensor_pairs: [list[tuple[Coordinate, Coordinate]]], limit: int) -> Coordinate:
    """Finds the beacon in an efficient manner (Could not do this with naive method)"""
    # Only one point exists that is outside all beacons
    # Therefore, beacon should be adjacent to boundaries of at least two sensors
    #   Calculate lines that define outside boundary of each sensor's "seen" area
    #   Find intersection of lines
    #       NB: If point happened to lie in corner of boundary, would need to include corners of "intersections"
    #   Find intersection which has manhattan distance outside of radius of all points

    a_grads, b_grads = set(), set()
    radii = {}
    sensors = [s[0] for s in sensor_pairs]

    for sensor, beacon in sensor_pairs:
        r = manhattan_distance(sensor, beacon)
        radii[sensor] = r

        a_grads.add(sensor.y - sensor.x - (r+1))
        a_grads.add(sensor.y - sensor.x + (r+1))
        b_grads.add(sensor.x + sensor.y + (r+1))
        b_grads.add(sensor.x + sensor.y - (r+1))

    for a in a_grads:
        for b in b_grads:
            intersection = Coordinate((b-a)//2, (a+b)//2)
            if 0 < intersection.x < limit and 0 < intersection.y < limit:
                if all(manhattan_distance(intersection, sensor) > radii[sensor] for sensor in sensors):
                    return intersection  # Found Beacon!


def main(data):
    sensors = []
    for row in data:
        sensors.append(get_coords(row))
    print(f"Part 1: {calculate_possible_beacons(sensors, target_y=10)}")
    distress_beacon = find_distress_beacon(sensors, limit=4000000)
    print(f"Part 2: {distress_beacon.x * 4000000 + distress_beacon.y}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
