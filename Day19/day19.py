import re

TESTING = False
PART = 1
OUTPUT_TO_CONSOLE = True


class Workflow:
    def __init__(self, name, rules, default):
        self.name = name
        self.rules = rules
        self.default = default

    def apply(self, part):
        for rule in self.rules:
            next_workflow = rule.apply(part)

            if next_workflow:
                return next_workflow

        return self.default


class Rule:
    def __init__(self, category, operator, threshold, next_workflow):
        self.category = category
        self.operator = operator
        self.threshold = threshold
        self.next_workflow = next_workflow

    def apply(self, part):
        if eval(part[self.category] + self.operator + self.threshold):
            return self.next_workflow

        return None


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
    workflows = {}
    parts = []

    workflow_section = True

    log("Workflows:")

    for line in inputs:
        if workflow_section:
            if line == "":
                workflow_section = False
                log("Parts:")
                continue

            workflow = re.match('^(.*?)\{(.*),(.*?)\}$', line)
            name, workflow_rules, default = workflow.groups()

            rules = []

            for rule_string in workflow_rules.split(","):
                rule = re.match('^([xmas])([<>])(\d+):(.*?)$', rule_string)

                category, operator, threshold, next_workflow = rule.groups()
                rules.append(Rule(category, operator, threshold, next_workflow))

            log(f"{name=} {rules=} {default=} ", end="")
            workflows.update({name: Workflow(name, rules, default)})
        else:
            line = line.strip("{}")

            ratings = {}

            for rating_string in line.split(","):
                category, value = rating_string.split("=")
                ratings.update({category: value})

            log(f"{ratings}")
            parts.append(ratings)

    return workflows, parts


def eliminate_passthroughs(workflows):
    passthrough_found = True
    passthroughs = []

    while passthrough_found:
        passthrough_found = False
        new_workflows = {}

        for name, workflow in workflows.items():
            for passthrough in passthroughs:
                if workflow.default == passthrough.name:
                    workflow.default = passthrough.default

            next_workflows = set()
            next_workflows.add(workflow.default)

            for rule in workflow.rules:
                for passthrough in passthroughs:
                    if rule.next_workflow == passthrough.name:
                        rule.next_workflow = passthrough.default

                next_workflows.add(rule.next_workflow)

            if len(next_workflows) == 1:
                passthrough_found = True
                log(f"{workflow.name} is passthrough -> {workflow.default}")
                passthroughs.append(workflow)
            else:
                new_workflows.update({workflow.name: workflow})

        workflows = new_workflows

    return workflows


def sort_parts(workflows, parts):
    accepted = []
    rejected = []

    for part in parts:
        workflow_name = 'in'

        while workflow_name not in ['A', 'R']:
            workflow_name = workflows[workflow_name].apply(part)

        if workflow_name == 'A':
            accepted.append(part)
        else:
            rejected.append(part)

    return accepted, rejected


def rating_totals(parts):
    rating_totals = []

    for part in parts:
        rating_total = 0

        for category, rating in part.items():
            rating_total += int(rating)

        rating_totals.append(rating_total)

    return rating_totals


def part1(inputs):
    workflows, parts = parse_input(inputs)
    workflows = eliminate_passthroughs(workflows)
    accepted, rejected = sort_parts(workflows, parts)
    return sum(rating_totals(accepted))


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
