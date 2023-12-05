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

    def apply_to(self, input_ranges):
        mapped_ranges = set()
        unmapped_ranges = set()

        for input_range in input_ranges:
            input_start = input_range[0]
            input_end = input_range[0] + input_range[1]
            source_start = self.source_start
            source_end = self.source_start + self.mapping_length
            overlap_range_start = max(input_start, source_start)
            overlap_range_end = min(input_end, source_end)
            overlap_range_length = overlap_range_end - overlap_range_start

            if overlap_range_length > 0:
                mapped_ranges.add((self.map(overlap_range_start), overlap_range_length))

                if input_start < source_start < input_end:
                    unmapped_ranges.add((input_start, source_start - input_start))

                if input_start < source_end < input_end:
                    unmapped_ranges.add((source_end, input_end - source_end))
            else:
                unmapped_ranges.add(input_range)

        return mapped_ranges, unmapped_ranges


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
    seeds = set()
    mappings = []

    map_from = map_to = ""

    for line in inputs:
        if seed_info := re.search('seeds: (.*)', line):
            seed_nums = [int(seed_string) for seed_string in seed_info.group(1).split()]

            for seed_index in range(0, int(len(seed_nums) / 2)):
                seeds.add((seed_nums[seed_index * 2], seed_nums[seed_index * 2 + 1]))

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


# This is effectively a brute force method.  Very inefficient.
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


def convert_seeds_to_locations(seeds, mappings):
    output_ranges = seeds
    map_from = "seed"

    while map_from != "location":
        input_ranges = output_ranges.copy()
        output_ranges = set()

        applicable_mappings = [m for m in mappings if m.map_from == map_from]
        next_map_from = applicable_mappings[0].map_to

        for mapping in applicable_mappings:
            mapped_ranges, input_ranges = mapping.apply_to(input_ranges)
            output_ranges.update(mapped_ranges)

        # Pass through any inputs that are not mapped
        output_ranges.update(input_ranges)

        map_from = next_map_from

    return output_ranges


def nearest(locations):
    nearest_location = float('inf')

    for location, _ in locations:
        if location < nearest_location:
            nearest_location = location

    return nearest_location


def part1(inputs):
    seeds, mappings = parse_input(inputs)
    seed_locations = determine_seed_locations(seeds, mappings)
    return seed_at_lowest_location(seed_locations)[0]


def part2(inputs):
    seeds, mappings = parse_input_with_seed_ranges(inputs)
    locations = convert_seeds_to_locations(seeds, mappings)
    return nearest(locations)
    # return lowest_location_with_seed(seeds, mappings)


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
