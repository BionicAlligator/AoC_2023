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


def create_lookup_table(race_length):
    time_vs_distance = {}

    for button_press_time in range(race_length + 1):
        speed = button_press_time
        run_time = race_length - button_press_time
        distance = speed * run_time
        time_vs_distance.update({button_press_time:distance})

    return time_vs_distance


def determine_winning_button_press_times(record_distance, time_vs_distance):
    winning_button_press_times = []

    for time, dist in time_vs_distance.items():
        if dist > record_distance:
            winning_button_press_times.append(time)

    return winning_button_press_times


def aggregate(winning_button_press_times):
    return reduce((lambda x, y: x * y), winning_button_press_times)


def count_winning_button_press_times(race_length, record_distance):
    num_winners = 0
    button_press_time = 1
    found_start_of_range = False
    found_end_of_range = False

    while not found_end_of_range:
        speed = button_press_time
        run_time = race_length - button_press_time
        distance = speed * run_time

        if distance > record_distance:
            found_start_of_range = True
            num_winners += 1
        else:
            if found_start_of_range:
                found_end_of_range = True

        button_press_time += 1

    return num_winners


def part1(inputs):
    ways_to_win = []
    race_history = parse_race_table(inputs)

    for race_length, record_distance in race_history:
        time_vs_distance = create_lookup_table(race_length)
        winning_button_press_times = determine_winning_button_press_times(record_distance, time_vs_distance)
        ways_to_win.append(len(winning_button_press_times))

    return aggregate(ways_to_win)


def part2(inputs):
    race_length, record_distance = parse_race_table_single_race(inputs)
    return count_winning_button_press_times(race_length, record_distance)


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
