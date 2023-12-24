from shapely import LineString, intersection

TESTING = False
PART = 1
OUTPUT_TO_CONSOLE = True

if PART == 1 and TESTING:
    TEST_SPACE = ((7, 7, 0), (27, 27, 0))
else:
    TEST_SPACE = ((200000000000000, 200000000000000, 0), (400000000000000, 400000000000000, 0))

X = 0
Y = 1
Z = 2

START = 0
END = 1


class Hailstone:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

        if PART == 1:
            self.position[Z] = 0
            self.velocity[Z] = 0

        self.time_in_test_space = self.calc_future_time_in_test_space()
        self.enters_test_space_in_future = self.time_in_test_space is not None

        if self.enters_test_space_in_future:
            self.path_through_test_space = self.calc_path_through_test_space()

    def __str__(self):
        return f"{tuple(self.position)} @ {tuple(self.velocity)}"

    def calc_future_time_in_test_space(self):
        if self.velocity[X] == 0:
            if overlaps((self.position[X], self.position[X]),
                        (TEST_SPACE[START][X], TEST_SPACE[END][X])):
                tx1 = float('-inf')
                tx2 = float('inf')
            else:
                return None
        else:
            tx1 = (TEST_SPACE[START][X] - self.position[X]) / (self.velocity[X])
            tx2 = (TEST_SPACE[END][X] - self.position[X]) / (self.velocity[X])

        tx_start = min(tx1, tx2)
        tx_end = max(tx1, tx2)

        if self.velocity[Y] == 0:
            if overlaps((self.position[Y], self.position[Y]),
                        (TEST_SPACE[START][Y], TEST_SPACE[END][Y])):
                ty1 = float('-inf')
                ty2 = float('inf')
            else:
                return None
        else:
            ty1 = (TEST_SPACE[START][Y] - self.position[Y]) / (self.velocity[Y])
            ty2 = (TEST_SPACE[END][Y] - self.position[Y]) / (self.velocity[Y])

        ty_start = min(ty1, ty2)
        ty_end = max(ty1, ty2)

        if self.velocity[Z] == 0:
            if overlaps((self.position[Z], self.position[Z]),
                        (TEST_SPACE[START][Z], TEST_SPACE[END][Z])):
                tz1 = float('-inf')
                tz2 = float('inf')
            else:
                return None
        else:
            tz1 = (TEST_SPACE[START][Z] - self.position[Z]) / (self.velocity[Z])
            tz2 = (TEST_SPACE[END][Z] - self.position[Z]) / (self.velocity[Z])

        tz_start = min(tz1, tz2)
        tz_end = max(tz1, tz2)

        start_time = max(0, tx_start, ty_start, tz_start)
        end_time = min(tx_end, ty_end, tz_end)

        if 0 <= end_time and start_time <= end_time:
            return start_time, end_time

        return None

    def calc_path_through_test_space(self):
        start_pos_x = self.position[X] + (self.velocity[X] * self.time_in_test_space[START])
        end_pos_x = self.position[X] + (self.velocity[X] * self.time_in_test_space[END])

        start_pos_y = self.position[Y] + (self.velocity[Y] * self.time_in_test_space[START])
        end_pos_y = self.position[Y] + (self.velocity[Y] * self.time_in_test_space[END])

        start_pos_z = self.position[Z] + (self.velocity[Z] * self.time_in_test_space[START])
        end_pos_z = self.position[Z] + (self.velocity[Z] * self.time_in_test_space[END])

        return LineString([(start_pos_x, start_pos_y, start_pos_z), (end_pos_x, end_pos_y, end_pos_z)])

    def intersects_in_2d_with(self, other_hailstone):
        return intersection(self.path_through_test_space, other_hailstone.path_through_test_space)


def log(message, end="\n"):
    if OUTPUT_TO_CONSOLE:
        print(message, end=end)


def read_tests(test_filename):
    tests = []
    inputs = []
    expected = ""

    file = open(test_filename, "r")

    for line in file:
        if line.lstrip().startswith("="):  # Line with equals sign at beginning or end means it is the expected output
            expected = line.split("=")[1].lstrip()
        elif line.rstrip().endswith("="):
            expected = line.split("=")[0].rstrip()
        elif not line.strip():  # Blank line means end of test specification
            tests.append((expected, inputs.copy()))
            inputs = []
        else:
            inputs.append(line.rstrip())

    return tests


def read_input(filename):
    file = open(filename, "r")
    lines = [line.rstrip() for line in file]
    return lines


def parse_input(inputs):
    hailstones = []

    for line in inputs:
        pos, vel = line.split(" @ ")
        position = list(map(int, pos.split(", ")))
        velocity = list(map(int, vel.split(", ")))
        hailstones.append(Hailstone(position, velocity))

    return hailstones


def overlaps(range_1, range_2):
    start1, end1 = range_1
    start2, end2 = range_2

    if start2 <= start1 <= end2 or start1 <= start2 <= end1:
        return True

    return False


def determine_potential_collisions(hailstones, test_space):
    log(f"Before temporal filtering: {len(hailstones)}")
    filtered_hailstones = []

    for hailstone in hailstones:
        if hailstone.enters_test_space_in_future:
            filtered_hailstones.append(hailstone)

    log(f"Before collision detection: {len(filtered_hailstones)}")
    future_potential_collisions = []

    for hailstone_num, hailstone1 in enumerate(filtered_hailstones):
        for hailstone2 in filtered_hailstones[hailstone_num + 1:]:
            if hailstone1.intersects_in_2d_with(hailstone2):
                future_potential_collisions.append((hailstone1, hailstone2))

    return future_potential_collisions


def part1(inputs):
    hailstones = parse_input(inputs)
    potential_collisions = determine_potential_collisions(hailstones, TEST_SPACE)
    return len(potential_collisions)


def part2(inputs):
    return


def run_tests():
    tests = read_tests("sample_input_part_" + str(PART) + ".txt")

    print(f"Test Results for Part {PART}")

    passed = failed = 0

    for expected, inputs in tests:
        actual = part1(inputs) if PART == 1 else part2(inputs)

        if expected == str(actual):
            passed += 1
            print(f"Passed: {inputs} -> {actual}\n")
        else:
            failed += 1
            print(f"Failed: {inputs} -> {actual}, expected {expected}\n")

    print(f"Passed: {passed}, Failed: {failed}")


def run_for_real():
    inputs = read_input("input.txt")

    print("Part 1: ", part1(inputs))

    if PART == 2:
        print("Part 2: ", part2(inputs))


if TESTING:
    run_tests()
else:
    run_for_real()
