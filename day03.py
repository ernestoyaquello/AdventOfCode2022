import input

PROBLEM_NUMBER = 3

def execute(is_part_two):
    rucksack = [list(line) for line in input.read_lines(problem_number = PROBLEM_NUMBER)]
    return calculate_result(part_1(rucksack) if not is_part_two else part_2(rucksack))

def part_1(rucksack):
    return [(next(item for item in rucksack[0:len(rucksack)//2] if item in rucksack[len(rucksack)//2:len(rucksack)])) for rucksack in rucksack]

def part_2(rucksack):
    return [next(item for item in rucksack[index] if item in rucksack[index + 1] and item in rucksack[index + 2]) for index in range(0, len(rucksack), 3)]

def calculate_result(items):
    return sum(ord(item) - (96 if ord(item) >= 97 else 38) for item in items)

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))