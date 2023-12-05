import re

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True


class Mapping:
    def __init__(self, map_from, map_to, source_start, dest_start, mapping_length):
        self.map_from = map_from
        self.map_to = map_to
        self.source_start = source_start
        self.dest_start = dest_start
        self.mapping_length = mapping_length

    def covers(self, value):
        return value in range(self.source_start, self.source_start + self.mapping_length)

    def includes_mapping_to(self, value):
        return value in range(self.dest_start, self.dest_start + self.mapping_length)

    def map(self, value):
        return value + self.dest_start - self.source_start

    def reverse_map(self, value):
        return value + self.source_start - self.dest_start


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
        elif line.strip() == "END":  # "END" means end of test specification
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
    seeds = []
    mappings = []

    map_from = map_to = ""

    for line in inputs:
        if seed_info := re.search('seeds: (.*)', line):
            seeds = [int(seed_string) for seed_string in seed_info.group(1).split()]
            log(f"{seeds=}")
        elif mapping_init := re.search('(.*?)-to-(.*?) map', line):
            map_from = mapping_init.group(1)
            map_to = mapping_init.group(2)
            log(f"Mapping from {map_from} to {map_to}")
        elif mapping_spec := re.search('(\d+) (\d+) (\d+)', line):
            dest_start = (int)(mapping_spec.group(1))
            source_start = (int)(mapping_spec.group(2))
            mapping_length = (int)(mapping_spec.group(3))

            if mapping_length > 0:
                mappings.append(Mapping(map_from, map_to, source_start, dest_start, mapping_length))

    return seeds, mappings


def parse_input_with_seed_ranges(inputs):
    seeds = []
    mappings = []

    map_from = map_to = ""

    for line in inputs:
        if seed_info := re.search('seeds: (.*)', line):
            seed_nums = [int(seed_string) for seed_string in seed_info.group(1).split()]

            for seed_index in range(0, int(len(seed_nums) / 2)):
                seeds.append((seed_nums[seed_index * 2], seed_nums[seed_index * 2 + 1]))

            log(f"{seeds=}")
        elif mapping_init := re.search('(.*?)-to-(.*?) map', line):
            map_from = mapping_init.group(1)
            map_to = mapping_init.group(2)
            log(f"Mapping from {map_from} to {map_to}")
        elif mapping_spec := re.search('(\d+) (\d+) (\d+)', line):
            dest_start = int(mapping_spec.group(1))
            source_start = int(mapping_spec.group(2))
            mapping_length = int(mapping_spec.group(3))

            if mapping_length > 0:
                mappings.append(Mapping(map_from, map_to, source_start, dest_start, mapping_length))

    return seeds, mappings


def determine_seed_locations(seeds, mappings):
    seed_locations = []

    for seed in seeds:
        value = seed

        map_from = "seed"

        while not map_from == "location":
            new_map_from = ""
            new_value = value

            for mapping in mappings:
                if mapping.map_from == map_from:
                    new_map_from = mapping.map_to

                    if mapping.covers(value):
                        new_value = mapping.map(value)

            map_from = new_map_from
            value = new_value

        location = value

        seed_locations.append((location, seed))

    return seed_locations


def seed_at_lowest_location(seed_locations):
    nearest_seed = (float('inf'), -1)

    for location, seed in seed_locations:
        if location < nearest_seed[0]:
            nearest_seed = (location, seed)

    return nearest_seed


def is_seed(seeds, seed):
    for (start_seed, num_seeds) in seeds:
        if start_seed <= seed < start_seed + num_seeds:
            return True

    return False


def lowest_location_with_seed(seeds, mappings):
    seed_found = False
    location = -1

    while not seed_found:
        location += 1

        if not location % 1000:
            log(f"Checking location {location}")

        value = location
        reverse_map_from = "location"

        while not reverse_map_from == "seed":
            new_reverse_map_from = ""

            new_value = value

            for mapping in mappings:
                if mapping.map_to == reverse_map_from:
                    new_reverse_map_from = mapping.map_from

                    if mapping.includes_mapping_to(value):
                        new_value = mapping.reverse_map(value)

            reverse_map_from = new_reverse_map_from
            value = new_value

        seed = value

        seed_found = is_seed(seeds, seed)

    return location


# def all_mappings_are_seed_to_location(mappings):
#     for mapping in mappings:
#         if mapping.map_from != "seed" or mapping.map_to != "location":
#             return False
#
#     return True
#
#
# def is_overlap(mapping1, mapping2):
#     if (mapping1.dest_start + mapping1.mapping_length <= mapping2.source_start or
#             mapping1.dest_start >= mapping2.source_start + mapping2.mapping_length):
#         return False
#
#     return True
#
#
# def combine(mapping1, mapping2):
#     map_from = mapping1.map_from
#     map_to = mapping2.map_to
#     source_start =
#     dest_start =
#     mapping_length =
#     new_mapping = Mapping()
#     return new_mapping
#
#
# def collapse_mappings(mappings):
#     while not all_mappings_are_seed_to_location(mappings):
#         mapping1 = mappings.pop()
#
#         new_mappings = []
#
#         for mapping2 in mappings:
#             if mapping1.map_to == mapping2.map_from and is_overlap(mapping1, mapping2):
#                 new_mapping = combine(mapping1, mapping2)
#                 new_mappings.append(new_mapping)
#
#         mappings.append(new_mappings)
#
#     return mappings


def part1(inputs):
    seeds, mappings = parse_input(inputs)
    seed_locations = determine_seed_locations(seeds, mappings)
    return seed_at_lowest_location(seed_locations)[0]


def part2(inputs):
    seeds, mappings = parse_input_with_seed_ranges(inputs)
    return lowest_location_with_seed(seeds, mappings)


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
