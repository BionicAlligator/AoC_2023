from collections import deque

TESTING = False
PART = 1
OUTPUT_TO_CONSOLE = True

LOW = 0
HIGH = 1

MODULE_TYPES = {'%': "flip-flop", "&": "conjunction"}


class PulseTracker:
    def __init__(self):
        self.pulses = [0, 0]
        self.pulse_queue = deque()

    def transmit_pulse(self, source, destination, pulse):
        self.pulse_queue.append((source, destination, pulse))

    def process_transmissions(self):
        while self.pulse_queue:
            source, destination, pulse = self.pulse_queue.popleft()
            self.pulses[pulse] += 1
            destination.receive(source, pulse)

    def pulse_product(self):
        return self.pulses[0] * self.pulses[1]


class Module:
    def __init__(self, pulse_tracker, name, destination_module_names):
        self.pulse_tracker = pulse_tracker
        self.name = name
        self.destination_module_names = destination_module_names
        self.destination_modules = set()
        self.incoming = {}

    def receive(self, source, pulse):
        self.transmit(pulse)

    def transmit(self, pulse):
        for module in self.destination_modules:
            self.pulse_tracker.transmit_pulse(self, module, pulse)

        self.pulse_tracker.process_transmissions()

    def link(self, modules):
        for dest_name in self.destination_module_names:
            if dest_name in modules:
                module = modules[dest_name]
            else:
                module = Output(self.pulse_tracker, dest_name, [])

            self.destination_modules.add(module)
            module.connect(self)

    def connect(self, source):
        self.incoming.update({source: LOW})


class Output(Module):
    def __init__(self, pulse_tracker, name, destination_module_names):
        super().__init__(pulse_tracker, name, destination_module_names)

    def receive(self, source, pulse):
        pass

    def transmit(self, pulse):
        pass


class Button(Module):
    def __init__(self, pulse_tracker, name, destination_module_names):
        super().__init__(pulse_tracker, name, destination_module_names)

    def push(self):
        self.receive(self, LOW)


#   - Broadcaster (broadcaster)
#     Re-transmits received pulse to all downstream modules
class Broadcaster(Module):
    def __init__(self, pulse_tracker, name, destination_module_names):
        super().__init__(pulse_tracker, name, destination_module_names)


#   - FlipFlop (%)
#     Initially off
#     Toggles state when receives low pulse
#       When toggles on, sends high pulse
#       When toggles off, sends low pulse
class FlipFlop(Module):
    def __init__(self, pulse_tracker, name, destination_module_names):
        super().__init__(pulse_tracker, name, destination_module_names)
        self.state = LOW

    def receive(self, source, pulse):
        if pulse == LOW:
            if self.state == LOW:
                self.state = HIGH
                self.transmit(HIGH)
            else:
                self.state = LOW
                self.transmit(LOW)


#   - Conjunction (&)
#     Multiple inputs, tracks last pulse from each
#     All inputs initially low
#     When pulse is received:
#       If all inputs are high, sends low pulse
#       Else sends high pulse
class Conjunction(Module):
    def __init__(self, pulse_tracker, name, destination_module_names):
        super().__init__(pulse_tracker, name, destination_module_names)

    def receive(self, source, pulse):
        self.incoming.update({source: pulse})

        if all(val == HIGH for val in self.incoming.values()):
            self.transmit(LOW)
        else:
            self.transmit(HIGH)


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


def parse_input(inputs, pulse_tracker):
    modules = {}
    broadcaster = None

    for line in inputs:
        module_info, destinations = line.split(" -> ")

        module_type = "broadcaster" if module_info == "broadcaster" else MODULE_TYPES[module_info[0]]
        module_name = "broadcaster" if module_info == "broadcaster" else module_info[1:]
        destination_module_names = destinations.split(", ")

        match module_type:
            case "broadcaster":
                broadcaster = Broadcaster(pulse_tracker, module_name, destination_module_names)
                modules.update({module_name: broadcaster})

            case "flip-flop":
                modules.update({module_name: FlipFlop(pulse_tracker, module_name, destination_module_names)})

            case "conjunction":
                modules.update({module_name: Conjunction(pulse_tracker, module_name, destination_module_names)})

    for module in modules.values():
        module.link(modules)

    return modules, broadcaster


def part1(inputs):
    pulse_tracker = PulseTracker()
    modules, broadcaster = parse_input(inputs, pulse_tracker)
    button = Button(pulse_tracker, "button", ["broadcaster"])
    button.link(modules)

    for push in range(1000):
        button.push()

    return pulse_tracker.pulse_product()


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
