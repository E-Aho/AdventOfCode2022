DAY_NUM = "18"


def adjacent_cubes(cube: tuple[int, ...]):
    x, y, z = cube
    return {
        (x+1, y, z),
        (x-1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1)
    }


def main(data):
    cubes = {tuple(int(v) for v in x.split(",")) for x in data}

    def part_1():
        p1_count = 0
        seen_cubes = set()
        for cube in cubes:
            p1_count += 6
            for adjacent_cube in adjacent_cubes(cube):
                if adjacent_cube in seen_cubes:
                    p1_count -= 2
            seen_cubes.add(cube)
        return p1_count

    def part_2():
        # Flood fill
        min_x = min(x for x, _, _ in cubes)
        max_x = max(x for x, _, _ in cubes)
        min_y = min(y for _, y, _ in cubes)
        max_y = max(y for _, y, _ in cubes)
        min_z = min(z for _, _, z in cubes)
        max_z = max(z for _, _, z in cubes)

        x_range = range(min_x -1, max_x + 2)
        y_range = range(min_y -1, max_y + 2)
        z_range = range(min_z -1, max_z + 2)

        outer_air = {(min_x-1, min_y-1, min_z-1)}
        queue = [(min_x-1, min_y-1, min_z-1)]

        while queue:
            x, y, z = queue.pop()
            if (
                    x not in x_range or
                    y not in y_range or
                    z not in z_range
            ):
                continue

            new_air = adjacent_cubes((x, y, z)) - outer_air - cubes
            outer_air.update(new_air)
            queue.extend(new_air)

        return sum(len((adjacent_cubes((x, y, z)) & outer_air) - cubes) for x, y,
                                                                          z in cubes)
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    with open(f"data/Day{DAY_NUM}.txt", "r") as file:
        cleaned_data = [line.strip().replace("\n", "") for line in file.readlines()]
    main(cleaned_data)
