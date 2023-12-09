import math
import re
from functools import reduce

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True


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


def parse_race_table(inputs):
    time_strings = re.findall('\d+', inputs[0])
    distance_strings = re.findall('\d+', inputs[1])

    times = [eval(t) for t in time_strings]
    distances = [eval(d) for d in distance_strings]

    race_history = list(zip(times, distances))
    log(race_history)
    return race_history


def parse_race_table_single_race(inputs):
    race_length = int(''.join(list(filter(str.isdigit, inputs[0]))))
    record_distance = int(''.join(list(filter(str.isdigit, inputs[1]))))
    return race_length, record_distance


def calc_min_time_for_dist(distance, race_length):
    # distance = (race_length - time) * time    [speed = time]
    # 0 = time^2 - race_length * time + distance
    # Use the quadratic formula to solve for time:
    #    x = (-b +- sqrt(b^2 - 4ac)) / 2a
    # in our case:
    #    button_press_time = (race_length +- sqrt(race_length^2 - 4*distance)) / 2
    # because the 'b' (race_length) parameter is negative and the 'a' multiplier is 1

    discriminant = (race_length ** 2) - (4 * distance)

    if discriminant < 0:
        log(f"Distance {distance} can not be achieved over a race of {race_length} milliseconds (complex roots)")
        exit()

    time1 = int((race_length + math.sqrt(discriminant)) // 2)
    time2 = int((race_length - math.sqrt(discriminant)) // 2)

    if time1 < 0 or time2 < 0:
        log(f"Distance {distance} can not be achieved over a race of {race_length} milliseconds (negative result)")
        exit()

    return min(time1, time2)


def ways_to_beat(record_time, race_length):
    return (race_length // 2 - record_time) * 2 + race_length % 2 - 1


def aggregate(winning_button_press_times):
    return reduce((lambda x, y: x * y), winning_button_press_times)


def part1(inputs):
    ways_to_win = []
    race_history = parse_race_table(inputs)

    for race_length, record_distance in race_history:
        record_time = calc_min_time_for_dist(record_distance, race_length)
        ways_to_win.append(ways_to_beat(record_time, race_length))

    return aggregate(ways_to_win)


def part2(inputs):
    race_length, record_distance = parse_race_table_single_race(inputs)
    record_time = calc_min_time_for_dist(record_distance, race_length)
    return ways_to_beat(record_time, race_length)


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
